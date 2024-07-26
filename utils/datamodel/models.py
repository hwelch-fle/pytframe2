from types import UnionType
import arcpy
import os

import arcpy.typing.describe as typdesc
from arcpy.mp import ArcGISProject
from arcpy.da import SearchCursor, UpdateCursor, InsertCursor, Editor
from typing import overload, Any, Generator, Iterable, Mapping, Self
from funcs.archelp import print

class SQLError(Exception): ...

class DescribeModel:
    """ Base object for models """
        
    def __init__(self, path: os.PathLike):
        self.path = path
        desc = self._validate()    
        self._describe: typdesc.base.Base = desc
        self.basename: str = desc.baseName
        self.workspace: os.PathLike = desc.path
        self.name: str = desc.name
        self.catalogpath: os.PathLike = desc.catalogPath
        self.extension: str = desc.extension
        self.type: str = desc.dataType
        return
    
    def update(self):
        """ Update the Describe object """
        self.__dict__.update(self.__class__(self.path).__dict__)
        return
    
    def _validate(self):
        """ Validate the featurepath and return the Describe object """
        if arcpy.Exists(self.path):
            # Get Describe object
            desc = arcpy.Describe(self.path)
            # Raise TypeError if the datatype is not the expected datatype
            if desc.dataType != type(self).__name__ and type(self).__name__ != "Describe Model":
                raise TypeError(f"{desc.baseName} is {desc.dataType}, must be {type(self).__name__}")
            return desc
        
        raise FileNotFoundError(f"{self.path} does not exist")
    
    def __repr__(self):
        return f"<{str(self)} @ {hex(id(self))}>"
    
    def __str__(self):
        return f"{type(self).__name__}: {self.basename} - {self.path}"

class Table(DescribeModel):
    """ Wrapper for basic Table operations """
    
    ALL_FIELDS = object()
    
    def __init__(self, path: os.PathLike):
        super().__init__(path)
        self._describe: typdesc.Table = self._describe
        self._query: str = None
        self._spatial_filter: arcpy.Geometry = None
        self.fields: dict[str, arcpy.Field] = {field.name: field for field in arcpy.ListFields(self.path)}
        self.fieldnames: list[str] = list(self.fields.keys())
        self.OIDField: str = self._describe.OIDFieldName
        self.cursor_tokens: list[str] = \
            [
                "CREATED@",
                "CREATOR@",
                "EDITED@",
                "EDITOR@",
                "GLOBALID@",
                "OID@",
                "SUBTYPE@",
                "*"
            ]
        self.valid_fields = self.fieldnames + self.cursor_tokens
        self.queried: bool = False
        self._queried_count: int = 0
        self._updated: bool = False
        self.record_count: int = int(arcpy.management.GetCount(self.path).getOutput(0))
        self._oid_set: set[int] = set(self[self.OIDField])
        self.editor: Editor = self._get_editor() # sets a valid workspace
        self._iter = None
        return
    
    @property
    def query(self) -> str:
        """ Get the query string """
        return self._query
    
    @query.setter
    def query(self, query_string: str):
        """ Set the query string """
        if not query_string: del self.query
        try:
            with self.search_cursor(where_clause=query_string) as cur: cur.fields
        except Exception as e: print(f"Invalid query string ({query_string})\n{e}", "warning")
        self._query = query_string
        self._updated = True
        self.queried = True
        self._queried_count = len(self)
        self._oid_set = set(self[self.OIDField])
        return
    
    @query.deleter
    def query(self):
        """ Delete the query string """
        self._query = None
        self.queried = False
        self._oid_set = set(self[self.OIDField])
        return

    @property
    def spatial_filter(self) -> arcpy.Geometry:
        """ Get the query string """
        return self._spatial_filter
    
    @spatial_filter.setter
    def spatial_filter(self, filter_shape: arcpy.Geometry):
        """ Set the query string """
        if not filter_shape: del self._spatial_filter
        try:
            with self.search_cursor(spatial_filter=filter_shape) as cur:
                cur.fields
        except Exception as e:
            print(f"Invalid spatial filter ({filter_shape})\n{e}", "warning")
        self._spatial_filter = filter_shape
        self._updated = True
        self.queried = True
        self._queried_count = len(self)
        self._oid_set = set(self[self.OIDField])
        return
    
    @spatial_filter.deleter
    def spatial_filter(self):
        """ Delete the query string """
        self._spatial_filter = None
        self.queried = False
        self._oid_set = set(self[self.OIDField])
        return
    
    @property
    def describe(self) -> 'typdesc.Table':
        """ Get the describe object """
        self._describe = arcpy.Describe(self.path)
        return self._describe
    
    @describe.setter
    def describe(self, _):
        raise AttributeError("Describe object is read-only")
    
    @describe.deleter
    def describe(self):
        raise AttributeError("Describe object is read-only")
    
    # This query handling is kinda messy
    # TODO: Create a QueryManager class that handles query operations
    
    def _handle_queries(self, kwargs):
        if 'where_clause' in kwargs and self.query:
            return f"({self.query}) AND ({kwargs['where_clause']})"
        elif 'where_clause' in kwargs:
            return kwargs['where_clause']
        return self.query
    
    def _handle_spatial_filter(self, kwargs):
        if self.spatial_filter and 'spatial_filter' in kwargs and self.spatial_filter.type == kwargs['spatial_filter'].type:
            return self.spatial_filter.union(kwargs['spatial_filter'])
        elif 'spatial_filter' in kwargs:
            return kwargs['spatial_filter']
        return self.spatial_filter
        
    def _validate_fields(self, fields: list[str]) -> bool:
        """ Validate field list for cursors """
        if fields not in (["*"] , Table.ALL_FIELDS) and not all(field in self.valid_fields for field in fields):
            return False
        return True
    
    def _get_editor(self) -> Editor:
        """ Get the editor of the table (walks up the directory tree until it finds a valid workspace)"""
        valid_workspace = False
        while not valid_workspace:
            try:
                with Editor(self.workspace):
                    valid_workspace = True
            except RuntimeError:
                self.workspace = os.path.dirname(self.workspace)
        return Editor(self.workspace)
    
    def _cursor(self, cur_type: str, fields: list[str]=ALL_FIELDS, **kwargs) -> UpdateCursor | SearchCursor | InsertCursor:
        """ Internal cursor method to get cursor type
        """
        if fields is Table.ALL_FIELDS or fields == ["*"]: 
            fields = self.fieldnames
            
        if not self._validate_fields(fields): 
            raise ValueError(f"Fields must be in {self.valid_fields}")
        
        kwargs['where_clause'] = self._handle_queries(kwargs)
        kwargs['spatial_filter'] = self._handle_spatial_filter(kwargs)
        
        if cur_type == "search": 
            return SearchCursor(self.path, fields, **kwargs)
        
        if cur_type == "update":
            self._updated = True
            return UpdateCursor(self.path, fields, **kwargs)
        
        if cur_type == "insert":
            # InsertCursor only supports datum_transformation and explicit kwargs
            kwargs = {k:v for k, v in kwargs.items() if k in ['datum_transformation', 'explicit']}
            self._updated = True
            return InsertCursor(self.path, fields, **kwargs)
        
        raise ValueError(f"Invalid cursor type {cur_type}")
    
    def __iter__(self) -> Generator[dict[str, Any], None, None]:
        yield from as_dict(self.search_cursor())
    
    def __len__(self) -> int:
        if self.queried: 
            return self._queried_count
        
        if not self._updated:
            return self.record_count
        
        self._updated = False
        self.record_count = int(arcpy.management.GetCount(self.path).getOutput(0))
        return self.record_count
    
    def __getitem__(self, idx: int | str | Iterable[int] | Iterable[str]) -> Any:
        # When retreiving a single object by OID, a generator is returned and next must be called
        # e.g. 
        # >>> table[1] -> <generator object Table...>
        # >>> next(table[1]) -> {field: value}
        # This allows a reference to the object to be stored before using it
        if isinstance(idx, int):
            if not idx in self._oid_set:
                raise KeyError(f"{idx} not a valid OID")
            #yield from as_dict(self.search_cursor(where_clause=f"{self.OIDField} = {idx}"))
            return next(as_dict(self.search_cursor(where_clause=f"{self.OIDField} = {idx}")))

        if isinstance(idx, str):
            if idx not in self.fieldnames:
                raise KeyError(f"{idx} not in {self.valid_fields}")
            yield from (value[idx] for value in as_dict(self.search_cursor([idx])))
            return
        
        if isinstance(idx, Iterable) and all(field in self.valid_fields for field in idx):
            yield from as_dict(self.search_cursor(idx))
            return
            
        if isinstance(idx, Iterable) and all(isinstance(oid, int) for oid in idx):
            yield from as_dict(self.search_cursor(where_clause=f"{self.OIDField} IN ({','.join(str(i) for i in idx)})"))
            return
        
        raise ValueError(f"{idx} is invalid, either pass field, OID, or list of fields or list of OIDs ({self.valid_fields})")
     
    def __setitem__(self, idx: int | str | Iterable[str], val: Mapping[str, Any] | Any) -> None:
        
        if (idx in self._oid_set) and isinstance(val, Mapping) and all(field in val.keys() for field in self.fieldnames):
            with self.editor:
                with self.update_cursor(list(val.keys()), where_clause=f"{self.OIDField} = {idx}") as cursor:
                    for _ in cursor: cursor.updateRow([val[field] for field in cursor.fields])
            return
        
        if isinstance(idx, str) and idx in self.valid_fields:
            with self.editor:
                with self.update_cursor([idx]) as cursor:
                    for _ in cursor: cursor.updateRow([val])
            return
        
        if isinstance(idx, Iterable) and all(field in self.valid_fields for field in idx):
            with self.editor:
                with self.update_cursor(idx) as cursor:
                    for _ in cursor: cursor.updateRow(val)
            return
        
        raise ValueError(f"{idx} not in {self.valid_fields} or index is out of range")
    
    def __delitem__(self, idx: int | str | Iterable[str] | Iterable[int]) -> str:
        if isinstance(idx, int):
            with self.editor:
                with self.update_cursor(where_clause=f"{self.OIDField} = {idx}") as cursor:
                    for _ in cursor: cursor.deleteRow()
            return
        
        if isinstance(idx, str) and idx in self.fieldnames:
            self.delete_field(idx)
            return
        
        if isinstance(idx, Iterable) and all(field in self.fieldnames for field in idx):
            for field in idx:
                self.delete_field(field, _update=False)
            return
         
        if isinstance(idx, Iterable) and all(oid in self._oid_set for oid in idx):
            with self.editor:
                with self.update_cursor(where_clause=f"{self.OIDField} IN ({','.join(idx)})") as cursor:
                    for _ in cursor: cursor.deleteRow()
            return
        
        raise KeyError(f"{idx} not in {self.valid_fields}")
    
    def __or__(self, other: Self) -> list[str]:
        """ Set style override that gives the union of two tables fields """
        return list(set(self.fieldnames) | set(other.fieldnames))
    
    def __and__(self, other: Self) -> list[str]:
        """ Set style override that gives the intersection of two tables fields """
        return list(set(self.fieldnames) & set(other.fieldnames))
    
    def __eq__(self, other: Self) -> bool:
        """ Override the equality operator to compare fieldnames """
        return self.fieldnames == other.fieldnames
    
    def __sub__(self, other: Self) -> list[str]:
        """ Set style override that gives the difference of two tables fields """
        return list(set(self.fieldnames) - set(other.fieldnames))
        
    def _clause(self, prefix: str | None, postfix: str | None, field: str = None) -> Generator[dict[str, Any], None, None]:
        if field and not field in self.valid_fields: 
            raise ValueError(f"{field} not in {self.valid_fields}")
        if (prefix and ";" in prefix) or (postfix and ";" in postfix): 
            raise SQLError("SQL Injection detected")
        try:
            yield from as_dict(self.search_cursor(sql_clause=(prefix, postfix)))
        except RuntimeError as sql_error:
            raise SQLError(f"""Invalid SQL Clause ({prefix} {postfix})\
                    \nMake sure your databse supports TOP, ORDER BY and DISTINCT\
                    \nTOP requres a SQL Server database (try using slices or range instead)\
                    \nORDER BY and DISTINCT require at least file geodatabase\
                    \n{sql_error}""", "warning")
    
    def _sort(self, field: str, reverse: bool, top: int = None) -> Generator[dict[str, Any], None, None]:
        # Prevent SQL Injection and top values of 0 (0 evaluates to False)
        if top and not isinstance(top, int):
            raise ValueError("top must be an integer greater than 0")
        yield from self._clause(
            prefix= f"TOP {top}" if top else None,
            postfix=f"ORDER BY {field} {'DESC' if reverse else 'ASC'}",
            field=field)
    
    def dsort(self, field: str, top: int = None):
        yield from self._sort(field, reverse=True, top=top)
    
    def asort(self, field: str, top: int = None):
        yield from self._sort(field, reverse=False, top=top)
    
    def group_by(self, field: str, top: int = None) -> Generator[dict[str, Any], None, None]:
        # Prevent SQL Injection and top values of 0 (0 evaluates to False)
        if top and not isinstance(top, int):
            raise ValueError("top must be an integer") # Prevent SQL Injection
        yield from self._clause(
            prefix=f"TOP {top}" if top else None, 
            postfix=f"GROUP BY {field}", 
            field=field)
    
    def distinct(self, field: str) -> Generator[dict[str, Any], None, None]:
        yield from self._clause(
            prefix=f"DISTINCT {field}", 
            postfix=None, 
            field=field)
    
    def update_cursor(self, fields: list[str]=ALL_FIELDS, **kwargs) -> UpdateCursor:
        """ Get an update cursor for the table
        fields: list of fields to update
        kwargs: See UpdateCursor for kwargs
        return: update cursor
        """
        return self._cursor("update", fields, **kwargs)
    
    def search_cursor(self, fields: list[str]=ALL_FIELDS, **kwargs) -> SearchCursor:
        """ Get a search cursor for the table
        fields: list of fields to return
        kwargs: See SearchCursor for kwargs
        return: search cursor
        """
        return self._cursor("search", fields, **kwargs)
    
    def insert_cursor(self, fields: list[str]=ALL_FIELDS, **kwargs) -> InsertCursor:
        """ Get an insert cursor for the table
        fields: list of fields to insert
        kwargs: See InsertCursor for kwargs
        return: insert cursor
        """
        return self._cursor("insert", fields, **kwargs)
    
    def add_field(self, field_name: str, **kwargs) -> None:
        """ Add a field to the table 
        field_name: name of the field to add
        kwargs: See arcpy.management.AddField for kwargs
        """
        arcpy.management.AddField(self.path, field_name, **kwargs)
        self.fieldnames.append(field_name)
        self.fields[field_name], *_ = arcpy.ListFields(self.path, field_name)
        return
    
    def delete_field(self, field_name: str, _update=True) -> None:
        """ Delete a field from the table 
        field_name: name of the field to delete
        """
        arcpy.management.DeleteField(self.path, field_name)
        self.fieldnames.remove(field_name)
        self.fields.pop(field_name)
        return
    
    def to_json(self, **kwargs) -> str:
        """ returns a json string of the Table/Features
        """
        out_file = arcpy.conversion.FeaturesToJSON(
            in_features=self.path, 
            format_json=True, 
            **kwargs)[0]
        json_string = open(out_file, 'rt').read()
        os.remove(out_file)
        return json_string
    
    def to_geo_json(self, **kwargs) -> str:
        """  returns a geojson string of the Table/Features
        """
        return self.to_json(geoJSON=True, **kwargs)
    
class FeatureClass(Table):
    """ Wrapper for basic FeatureClass operations """    
    def __init__(self, path: os.PathLike):
        super().__init__(path)
        self._describe: typdesc.FeatureClass = self._describe
        self.spatialReference: arcpy.SpatialReference = self._describe.spatialReference
        self.shapeType: str = self._describe.shapeType
        self.cursor_tokens.extend(
            [
                "SHAPE@",
                "SHAPE@XY",
                "SHAPE@TRUECENTROID",
                "SHAPE@X",
                "SHAPE@Y",
                "SHAPE@Z",
                "SHAPE@M",
                "SHAPE@JSON",
                "SHAPE@WKB",
                "SHAPE@WKT",
                "SHAPE@AREA",
                "SHAPE@LENGTH",
            ]
        )
        self.valid_fields = self.fieldnames + self.cursor_tokens
        self.fieldnames[self.fieldnames.index(self._describe.shapeFieldName)] = "SHAPE@"
      
class ShapeFile(FeatureClass):
    def __init__(self, path: os.PathLike):
        super().__init__(path)
        self._describe: typdesc.ShapeFile = self._describe
        return

class FeatureDataset(DescribeModel):
    def __init__(self, path: os.PathLike):
        super().__init__(path)
        self._describe: typdesc.base.Dataset = self._describe
        return

ALL = object()

class Workspace(DescribeModel):
    
    def __init__(self, path: os.PathLike, *,
                 dataset_filter: list[str]=ALL,
                 featureclass_filter: list[str]=ALL,
                 table_filter: list[str]=ALL):
        super().__init__(path)
        self._describe: typdesc.Workspace = self._describe
        
        self.dataset_filter = dataset_filter
        self.featureclass_filter = featureclass_filter
        self.table_filter = table_filter
        arcpy.env.workspace = self.path
        self.datasets: dict[str, FeatureDataset] = \
            {
                ds: os.path.join(self.path, ds)
                for ds in arcpy.ListDatasets()
                if dataset_filter == ALL or (dataset_filter and ds in dataset_filter)
            }
        self.featureclasses: dict[str, FeatureClass] = \
            {
                fc: os.path.join(self.path, fc)
                for fc in arcpy.ListFeatureClasses()
                if featureclass_filter == ALL or (featureclass_filter and fc in featureclass_filter)
            }
        for ds in self.datasets.keys():
            self.featureclasses.update(
                {
                    f"{ds}/{fc}": os.path.join(self.path, ds, fc)
                    for fc in arcpy.ListFeatureClasses(feature_dataset=ds)
                    if featureclass_filter == ALL or (featureclass_filter and fc in featureclass_filter)
                }
            )
        self.tables: dict[str, Table] = \
            {
                tbl: os.path.join(self.path, tbl)
                for tbl in arcpy.ListTables()
                if table_filter == ALL or (table_filter and tbl in table_filter)
            }
        return
    
    def __len__(self) -> int:
        return len(self.featureclasses) + len(self.tables) + len(self.datasets)
    
    def __str__(self) -> str:
        return f"{type(self).__name__}: {self.path}"

    def __repr__(self) -> str:
        return f"""<{str(self)} @ {hex(id(self))}>
    \tFeatureClasses:{list(self.featureclasses.keys())}
    \tTables:{list(self.tables.keys())}
    \tDatasets:{list(self.datasets.keys())}"""
    
    def __getitem__(self, idx: str) -> FeatureClass | Table | FeatureDataset:
        # Doing some lazy loading here to prevent initializing all the children
        # This distributes the ~ 5 seconds of initialization time across the
        # number of children in the workspace and only initializes the child
        # when it is first accessed.
        if idx in self.featureclasses:
            if not isinstance(self.featureclasses[idx], FeatureClass):
                self.featureclasses[idx] = FeatureClass(self.featureclasses[idx])
            return self.featureclasses[idx]
        if idx in self.tables:
            if not isinstance(self.tables[idx], Table):
                self.tables[idx] = Table(self.tables[idx])
            return self.tables[idx]
        if idx in self.datasets:
            if not isinstance(self.datasets[idx], FeatureDataset):
                self.datasets[idx] = FeatureDataset(self.datasets[idx])
            return self.datasets[idx]
        raise KeyError(f"{idx} not in {self.featureclasses.keys()} or {self.tables.keys()} or {self.datasets.keys()}")
    
    def __eq__(self, other: Self) -> bool:
        """ Override the equality operator to compare children """
        return (*self.featureclasses, *self.tables) == (*other.featureclasses, *other.tables)
    
    def __or__(self, other: Self) -> list[str]:
        """ Set style override that gives the union of two workspaces children """
        return list(set([*self.featureclasses, *self.tables]) | set([*other.featureclasses, *other.tables]))
    
    def __and__(self, other: Self) -> list[str]:
        """ Set style override that gives the intersection of two workspaces children """
        return list(set([*self.featureclasses, *self.tables]) & set([*other.featureclasses, *other.tables]))
    
    def __sub__(self, other: Self) -> list[str]:
        """ Set style override that gives the difference of two workspaces children """
        return list(set([*self.featureclasses, *self.tables]) - set([*other.featureclasses, *other.tables]))

def as_dict(cursor: SearchCursor | UpdateCursor) -> Generator[dict[str, Any], None, None]:
    """Convert a search cursor or update cursor to an iterable dictionary generator
    This allows for each row operation to be done using fieldnames as keys.
    
    Arguments:
        cursor: search cursor or update cursor.
        
    Yields:
        dictionary of the cursor row.
    
    NOTE: This function will not overwrite the cursor object
    if used in a context manager and iterating through the yielded
    dictionaries will progress the cursor as if you were iterating
    through the cursor object itself.
    
    usage:
    >>> with table.search_cursor() as cursor:
    >>>     for row in as_dict(cursor):
    >>>         print(row)
    ------------------------------------------------
    >>> with table.update_cursor() as cursor:
    >>>     for row in as_dict(cursor):
    >>>        row["field"] = "new value"
    >>>        cursor.updateRow(list(row.values()))
        
    """
    yield from ( dict(zip(cursor.fields, row)) for row in cursor )

if __name__ == "__main__":
    pass