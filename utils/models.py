import arcpy
import os
from typing import Any, Generator

from time import time

from typing import overload

from utils.archelp import message

ALL_FIELDS = object()

class DescribeModel:
    """ Base object for models """
        
    def __init__(self, featurepath: os.PathLike):
        self.featurepath = featurepath
        desc = self._validate()
                
        # Set General Properties
        self.describe: Any = desc
        self.basename: str = desc.baseName
        self.workspace: os.PathLike = desc.path
        self.name: str = desc.name
        self.catalogpath: os.PathLike = desc.catalogPath
        self.extension: str = desc.extension
        self.type: str = desc.dataType
        return
    
    def update(self):
        """ Update the Describe object """
        updates = self.__class__(self.featurepath)
        self.__dict__.update(updates.__dict__)
        return
    
    def _validate(self):
        """ Validate the featurepath and return the Describe object """
        if arcpy.Exists(self.featurepath):
            # Get Describe object
            desc = arcpy.Describe(self.featurepath)
            # Raise TypeError if the datatype is not the expected datatype
            if desc.dataType != type(self).__name__ and type(self).__name__ != "Describe Model":
                raise TypeError(f"{desc.baseName} is {desc.dataType}, must be {type(self).__name__}")
            return desc
        
        raise FileNotFoundError(f"{self.featurepath} does not exist")
    
    def __repr__(self):
        return f"<{type(self).__name__}: {self.basename} @ {hex(id(self))}>"
    
    def __str__(self):
        return f"{type(self).__name__}: {self.basename}"

class Table(DescribeModel):
    """ Wrapper for basic Table operations """
    def __init__(self, tablepath: os.PathLike, cached: bool = True):
        super().__init__(tablepath)
        
        self._query: str = None
        self.fields: list[arcpy.Field] = self.describe.fields
        self.fieldnames: list[str] = [field.name for field in self.fields]
        if hasattr(self.describe, "shapeFieldName"):
            shape_idx = self.fieldnames.index(self.describe.shapeFieldName)
            self.fieldnames[shape_idx] = "SHAPE@"   # Default to include full shape
        self.indexes: list[arcpy.Index] = self.describe.indexes
        self.OIDField: str = self.describe.OIDFieldName
        self.OIDs = [row[0] for row in arcpy.da.SearchCursor(self.featurepath, [self.OIDField])]
        self.cursor_tokens: list[str] = \
            [
                "CREATED@",
                "CREATOR@",
                "EDITED@",
                "EDITOR@",
                "GLOBALID@",
                "OID@",
                "SUBTYPE@",
            ]
        self.cache: Cache[str, dict] | None = Cache(self) if cached else None
        self.record_count: int = len(self.cache) if self.cache else self.describe.rowCount
        self._total_count: int = self.record_count
        return
    
    def _validate_fields(self, fields: list[str]) -> bool:
        """ Validate field list for cursors """
        if fields != ["*"] and not all([field in self.fieldnames + self.cursor_tokens for field in fields]):
            return False
        return True
    
    @property
    def row_template(self) -> dict[str, Any]:
        """ Get a template for a row """
        return dict(zip(self.fieldnames, [None for _ in range(len(self.fieldnames))]))
    
    @property
    def query(self) -> str:
        """ Get the query string """
        return self._query
    
    @query.setter
    def query(self, query_string: str):
        """ Set the query string """
        try:
            with arcpy.da.SearchCursor(self.featurepath, [self.OIDField], where_clause=query_string) as cur:
                cur.fields
        except Exception as e:
            message(f"Invalid query string ({query_string})", "warning")
        self._query = query_string
        self.record_count = len([i for i in self])
        return
    
    @query.deleter
    def query(self):
        """ Delete the query string """
        self._query = None
        self.cache.invalidate()
        self.record_count = self._total_count
        return
    
    def get_rows(self, fields: list[str] = ALL_FIELDS, as_dict: bool = False, **kwargs) -> Generator[list | dict, None, None]:
        """ Get rows from a table 
        fields: list of fields to return
        as_dict: return rows as dict if True
        kwargs: See arcpy.da.SearchCursor for kwargs
        """
        if fields == ALL_FIELDS or fields == ["*"]:
            fields = self.fieldnames
        if not self._validate_fields(fields):
            raise ValueError(f"Fields must be in {self.fieldnames + self.cursor_tokens}")
        
        if hasattr(self, "cache") and self.cache and self.cache.valid:
            for _, v in self.cache.items():
                yield v if as_dict else list(v.values())
        
        with arcpy.da.SearchCursor(self.featurepath, fields, where_clause=self.query, **kwargs) as cursor:
            for row in cursor:
                if as_dict:
                    yield dict(zip(fields, row))
                else:
                    if len(fields) == 1: yield row[0]
                    else: yield row
    
    def _update_rows_cache(self, key: str, values: dict[str, dict[str, Any]], **kwargs) -> int:
        """ Internal Method for updating rows in cache """
        if not values:
            raise ValueError("Values must be provided")
        if not self._validate_fields(list(values.keys()) + [key]):
            raise ValueError(f"Fields must be in {self.fieldnames + self.cursor_tokens}")
        update_count = 0
        for k, v in values.items():
            idx = self._get_index(k)
            self.cache[idx].update(v)
            self.cache.edits['updates'].append(self.cache[idx])
            update_count += 1
        return update_count
                    
    def update_rows(self, key: str, values: dict[str, dict[str, Any]], **kwargs) -> int:
        """ Update rows in table
        key: field to use as key for update (must be in fields)
        values: dict of key value pairs to update [fieldname/token: value]
        kwargs: See arcpy.da.UpdateCursor for kwargs
        return: number of rows updated
        """
        if not values:
            raise ValueError("Values must be provided")
        fields = list(next(iter(values.values())).keys()) # Get fields from first value
        if not self._validate_fields(fields + [key]):
            raise ValueError(f"Fields must be in {self.fieldnames + self.cursor_tokens}")
        for val in values.values():
            if list(val.keys()) != fields:
                raise ValueError(f"Fields must match for all values in values dict")
        
        if 'where_clause' in kwargs:
            query = self._join_queries(kwargs['where_clause'])
            del kwargs['where_clause']
        else:
            query = self.query
        
        update_count = 0
        with arcpy.da.UpdateCursor(self.featurepath, fields, where_clause=query, **kwargs) as cursor:
            for row in cursor:
                row_dict = dict(zip(fields, row))
                row_key = row_dict[key]
                if row_key in values.keys():
                    new_row = values[row_dict[key]]
                    if not all([f in fields for f in new_row.keys()]):
                        raise ValueError(f"Row {row_dict[key]} has invalid fields {new_row.keys()}")
                    cursor.updateRow(list(new_row.values()))
                    self.cache[self._get_index(row_dict[key])].update(new_row)
                    update_count += 1
        return update_count
    
    def _insert_rows_cache(self, values: dict[str, Any], **kwargs) -> int:
        """ Internal Method for writing inserts to cache """
        if not values:
            raise ValueError("Values must be provided")
        fields = list(values.keys())
        if not self._validate_fields(fields):
            raise ValueError(f"Fields must be in {self.fieldnames + self.cursor_tokens}")
        
        for row in values:
            self.cache[len(self.cache)] = row
            self.cache.edits['inserts'].append(row)
        self.record_count += len(values)
        self._total_count += len(values)
        return len(values)
    
    def insert_rows(self, values: list[dict[Any, dict[str, Any]]], **kwargs) -> int:
        """ Insert rows into table
        fields: list of fields to insert
        values: list of dicts with key value pairs to insert [field: value]
        return: number of rows inserted
        """
        if not values:
            raise ValueError("Values must be provided")
        fields = list(values[0].keys())
        if not self._validate_fields(fields):
            raise ValueError(f"Fields must be in {self.fieldnames + self.cursor_tokens}")
        
        if self.cache:
            return self._insert_rows_cache(values)
        
        insert_count = 0
        with arcpy.da.InsertCursor(self.featurepath, fields, **kwargs) as cursor:
            for value in values:
                cursor.insertRow([value[field] for field in fields])
                insert_count += 1
        self.record_count += insert_count
        self._total_count += insert_count
        return insert_count
    
    def _delete_rows_cache(self, values: list[Any], **kwargs) -> int:
        """ Internal Method for deleting rows from cache """
        if not values:
            raise ValueError("Values must be provided")
        delete_count = 0
        for value in values:
            self.cache.pop(self._get_index(value))
            delete_count += 1
        self.record_count -= delete_count
        self._total_count -= delete_count
        return delete_count
    
    def delete_rows(self, values: list[int], **kwargs) -> int:
        """ Delete rows from table
        values: list of ObjectIDs to delete
        kwargs: See arcpy.da.UpdateCursor for kwargs
        return: number of rows deleted
        """
        if not values:
            raise ValueError("Values must be provided")
        
        if self.cache:
            return self._delete_rows_cache(self.OIDField, values)
        
        delete_count = 0
        with arcpy.da.UpdateCursor(self.featurepath, [self.OIDField], **kwargs) as cursor:
            for row in cursor:
                if row[0] in values:
                    cursor.deleteRow()
                    delete_count += 1
        self.record_count -= delete_count
        self._total_count -= delete_count
        return delete_count
    
    def add_field(self, field_name: str, **kwargs) -> None:
        """ Add a field to the table 
        field_name: name of the field to add
        kwargs: See arcpy.management.AddField for kwargs
        """
        arcpy.management.AddField(self.featurepath, field_name, **kwargs)
        self.update()
        return
    
    def delete_fields(self, field_names: list[str]) -> None:
        """ Delete a field from the table 
        field_name: name of the field to delete
        """
        arcpy.management.DeleteField(self.featurepath, field_names)
        self.update()
        return
    
    def commit(self) -> None:
        """ Commit changes to the table """
        self.cache.commit()
        return
    
    def _join_queries(self, queries: str | list[str], join_type: str = "AND") -> str:
        """ Join queries with a join type
        queries: list of queries to join
        join_type: join type (AND/OR)
        return: joined query string
        """
        if isinstance(queries, str):
            queries = [queries]
        if self.query and self.query not in queries:
            queries.append(self.query)
        return f" {join_type} ".join(queries)
    
    def _get_index(self, key: int) -> int:
        """ Get the index of a key in the cache """
        if not self.cache:
            raise CacheError("Cache not found")
        for idx, row in self.cache.items():
            if row[self.OIDField] == key:
                return idx
        raise CacheError(f"Key {key} not found in cache")
    
    def __iter__(self):
        yield from self.get_rows(self.fieldnames, as_dict=True)
        
    def __len__(self):
        if hasattr(self, "record_count"):
            return self.record_count
        elif hasattr(self, "cache") and self.cache:
            return len(self.cache)
        return len([i for i in self])
    
    def __getitem__(self, idx: int | str):
        if isinstance(idx, int):
            if idx >= self.record_count or idx < -self.record_count-1:
                raise IndexError(f"Index {idx} out of range")
            if not self.cache:
                self.cache.rebuild()
            return self.cache[idx if idx >= 0 else self.record_count + idx]
        
        elif isinstance(idx, str) and idx in self.fieldnames + self.cursor_tokens:
            print("Got String")
            return [v for v in self.get_rows([idx])]
        
        elif isinstance(idx, list) and all([isinstance(f, str) for f in idx]):
            if set(idx).issubset(self.fieldnames + self.cursor_tokens):
                return self.get_rows(idx)
        
        raise KeyError(f"{idx} not in {self.fieldnames + self.cursor_tokens}")
    
    def __setitem__(self, key: int | str, value: list | Any):
        if isinstance(key, int) and len(value) == len(self.fieldnames):
            print("Int")
            self.update_rows(self.OIDField, {key: dict(zip(self.fieldnames, value))})
            return
        
        if isinstance(key, str) and key in self.fieldnames + self.cursor_tokens:
            print("String")
            with arcpy.da.UpdateCursor(self.featurepath, [key], where_clause=self.query) as cursor:
                for row in cursor:
                    row[0] = value
                    cursor.updateRow(row)
            return
        raise ValueError(f"{key} not in {self.fieldnames + self.cursor_tokens} or index is out of range")
    
    def __delitem__(self, idx: int | str | list[str]):
        if isinstance(idx, int):
            self.delete_rows(self.OIDField, self[idx][self.OIDField])
            return
        if isinstance(idx, str) and idx in self.fieldnames:
            self.delete_fields([idx])
            self.update()
            return
        if isinstance(idx, list):
            if all([field in self.fieldnames for field in idx]):
                self.delete_fields(idx)
                return
            else:
                raise ValueError(f"{idx} not subset of {self.fieldnames}")
        raise KeyError(f"{idx} not in {self.fieldnames + self.cursor_tokens}")

class FeatureClass(Table):
    """ Wrapper for basic FeatureClass operations """    
    def __init__(self, shppath: os.PathLike, **kwargs):
        super().__init__(shppath, **kwargs)
        self.spatialReference: arcpy.SpatialReference = self.describe.spatialReference
        self.shapeType: str = self.describe.shapeType
        self.cursor_tokens.extend(
            [
                "SHAPE@XY",
                "SHAPE@TRUECENTROID",
                "SHAPE@X",
                "SHAPE@Y",
                "SHAPE@Z",
                "SHAPE@M",
                "SHAPE@JSON",
                "SHAPE@WKB",
                "SHAPE@WKT",
                "SHAPE@",
                "SHAPE@AREA",
                "SHAPE@LENGTH",
            ]
        )
      
class ShapeFile(FeatureClass):
    """ Wraper for basic Shapefile operations"""
    
class Dataset(DescribeModel):
    """ Wrapper for basic Dataset operations """
    
class GeoDatabase(DescribeModel):
    """ Wrapper for basic GeoDatabase operations """
    
class Schema:
    """ Wrapper for simple Schema operations with GeoDatabases"""

    def __init__(self, gdb: os.PathLike):
        self.gdb = gdb
        if not arcpy.Exists(self.gdb):
            raise FileNotFoundError(f"{self.gdb} does not exist")
        self.describe = arcpy.Describe(gdb)
        self.name = self.describe.name
        self.path = self.describe.catalogPath
        self.datasets: dict[str: Any] = \
            {
                ds.name: ds 
                for ds in self.describe.children 
                if ds.dataType == "FeatureDataset"
            }
        self.tables: dict[str: list[str]] = \
            {
                table.name: table.fields 
                for table in self.describe.children 
                if table.dataType == "Table"
            }
        self.featureclasses: dict[str: list[str]] = \
            {
                fc.name: fc.fields 
                for fc in self.describe.children
                if fc.dataType == "FeatureClass"
            }
        for dataset in self.datasets.values():
            self.tables.update(
                {
                    f'{dataset.name}->{table.name}': table.fields 
                    for table in dataset.children 
                    if table.dataType == "Table"
                }
            )
            self.featureclasses.update(
                {
                    f'{dataset.name}->{fc.name}': fc.fields 
                    for fc in dataset.children 
                    if fc.dataType == "FeatureClass"
                }
            )
        self.domain_names: list[str] = self.describe.domains
        self._comparator_set = set(self.featureclasses.keys()).union(set(self.tables.keys()))
        return
    
    def __repr__(self):
        return f"<Schema: {self.name} @ {hex(id(self))}>"
    
    def __str__(self):
        return f"Schema: {self.name}\nDatasets: {list(self.datasets.keys())}\nTables: {list(self.tables.keys())}\nFeatureClasses: {list(self.featureclasses.keys())}\nDomains: {self.domain_names}"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Schema):
            return self._comparator_set - other._comparator_set == set() and other._comparator_set - self._comparator_set == set()
        raise ValueError(f"Cannot compare Schema to {type(other)}")
    
    def __and__(self, other: object) -> set[str]:
        """ Overload the & operator to return the intersection of two Schemas Table anf FC names"""
        if isinstance(other, Schema):
            return self._comparator_set & other._comparator_set
        raise ValueError(f"Cannot compare Schema to {type(other)}")
    
    def __or__(self, other: object) -> set[str]:
        """ Overload the | operator to return the union of two Schemas Table and FC names"""
        if isinstance(other, Schema):
            return self._comparator_set | other._comparator_set
        raise ValueError(f"Cannot compare Schema to {type(other)}")
    
    def __sub__(self, other: object) -> set[str]:
        """ Overload the - operator to return the difference of two Schemas Table and FC names"""
        if isinstance(other, Schema):
            return self._comparator_set - other._comparator_set
        raise ValueError(f"Cannot compare Schema to {type(other)}")


class CacheError(Exception):
    """ Custom Exception for Cache """
    pass
    
class Cache(dict):
    """ Cache object that allows for invalidation and updating """
    
    def __init__(self, table: Table) -> None:
        super().__init__({row[table.OIDField]: row for row in table})
        self.valid: bool = True
        self.table: Table = table
        self.edits: dict = \
            {
                "inserts": [],
                "updates": [],
                "deletes": [],
            }
        return
    
    def invalidate(self) -> None:
        """ Invalidate the cache """
        self.valid = False
        return
    
    def commit(self) -> None:
        """ Commit changes to the cache """
        self.table.insert_rows(self.edits['inserts'])
        self.table.update_rows(self.table.OIDField, self.edits['updates'])
        self.table.delete_rows(self.edits['deletes'])
        self.edits = \
            {
                "inserts": [],
                "updates": [],
                "deletes": [],
            }
        return
    
    def rebuild(self) -> None:
        """ Rebuild the cache """
        self.clear()
        self.update({row[self.table.OIDField]: row for row in self.table})
        self.valid = True
        return
    
    def __setitem__(self, key: Any, value: Any) -> None:
        super().__setitem__(key, value)
        print("Cache hit")
        self.edits['updates'].append(value)
    
    def __bool__(self) -> bool:
        return self.valid


if __name__ == "__main__":
    p = ShapeFile(r"C:\Users\asimov\Desktop\Parcels\nc_union_parcels_pt.shp")