from os import PathLike
from dataclasses import dataclass
from contextlib import contextmanager
from functools import reduce, wraps
from typing import Literal, TypeAlias, Optional, Generator

from arcpy import Describe, Geometry
import arcpy.typing.describe as dtype
from arcpy.management import GetCount

from arcpy.da import Editor, SearchCursor, UpdateCursor, InsertCursor

SpatialRelationship: TypeAlias = \
    Literal[
        'INTERSECTS', 
        'ENVELOPE_INTERSECTS', 
        'INDEX_INTERSECTS', 
        'TOUCHES', 
        'CROSSES', 
        'WITHIN', 
        'CONTAINS',
        ]

CursorTokens: TypeAlias = Literal[
        "CREATED@",
        "CREATOR@",
        "EDITED@",
        "EDITOR@",
        "GLOBALID@",
        "OID@",
        "SUBTYPE@",
        "*",
        ]

ShapeTokens: TypeAlias = \
Literal[
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

class BaseQuery: ...

@dataclass(slots=True, frozen=True)
class SpatialQuery(BaseQuery):
    spatial_filter: Optional[Geometry] = None
    spatial_relationship: SpatialRelationship = 'INTERSECTS'
    
    def __str__(self) -> str:
        return f"{self.spatial_relationship} {self.spatial_filter.type}"
    
    def __add__(self, other: 'SpatialQuery') -> 'SpatialQuery':
        """Intersection of two geometries"""
        return SpatialQuery(self.spatial_filter + other.spatial_filter, spatial_relationship=self.spatial_relationship)
    
    def __xor__(self, other: 'SpatialQuery') -> 'SpatialQuery':
        """Symmetric difference of two geometries"""
        return SpatialQuery(self.spatial_filter ^ other.spatial_filter, spatial_relationship=self.spatial_relationship)
    
    def __or__(self, other: 'SpatialQuery') -> 'SpatialQuery':
        """Union of two geometries"""
        return SpatialQuery(self.spatial_filter | other.spatial_filter, spatial_relationship=self.spatial_relationship)
    
    def __sub__(self, other: 'SpatialQuery') -> 'SpatialQuery':
        """Difference of two geometries"""
        return SpatialQuery(self.spatial_filter - other.spatial_filter, spatial_relationship=self.spatial_relationship)

    def __eq__(self, other: 'SpatialQuery') -> bool:
        """Equality of two geometries"""
        return self.spatial_filter == other.spatial_filter
    
    
@dataclass(slots=True, frozen=True)
class SQLQuery(BaseQuery):
    """Simplified interface for building and combining SQL queries using Python objects and builtins.
    
    Supports `+`, `-`, `|` operators and `-` negation.
    Example:
    ```py
    >>> skip_first = SQLQuery("ID <> 1")
    >>> older_than_thirty = SQLQuery("AGE > 30")
    >>> skip_first + older_than_thirty
    '(ID <> 1) AND (AGE > 30)'
    >>> skip_first | older_than_thirty
    '(ID <> 1) OR (AGE > 30)'
    >>> skip_first | -older_than_thirty
    '(ID <> 1) OR NOT (AGE > 30)'
    """
    # Set default Query to all rows
    where_clause: Optional[str] = None
    
    def __post_init__(self) -> None:
        if self.where_clause and ';' in self.where_clause:
            raise ValueError(';-; SQL Injection not allowed ;-;')
    
    def __str__(self):
        return self.where_clause
    
    def __repr__(self):
        return f"SQLQuery({self.where_clause})"
    
    def _combine(self, other: 'SQLQuery', operator: str) -> 'SQLQuery':
        return SQLQuery(f"{self.where_clause} {operator} {other}")
    
    def __add__(self, other: 'SQLQuery') -> 'SQLQuery':
        """ AND"""
        return self._combine(other, "AND")
    
    def __sub__(self, other: 'SQLQuery') -> 'SQLQuery':
        """ AND NOT """
        return self._combine(other, "AND NOT")
    
    def __or__(self, other: 'SQLQuery') -> 'SQLQuery':
        """ OR """
        return self._combine(other, "OR")
    
    def __neg__(self) -> 'SQLQuery':
        """ NOT """
        if self.where_clause.startswith("NOT"):
            return SQLQuery(self.where_clause[4:])
        return SQLQuery(f"NOT {self.where_clause}")
    
    # Constructor Functions
    def is_in(self, sequence: list[str], string_cast: bool=False) -> 'SQLQuery':
        """Builds a new `SQLQuery` with a stringifiable containment operation.
        
        Args:
            sequence: The sequence of strings to check against.
            string_cast: (Default: `False`) Switch for wrapping sequence elements in single quotes for query.
            
        Returns:
            `SQLQuery` object with the specified containment clause.
        
        Raises:
            None
        
        Note:
            This method is best used immediately upon creation of a new `SQLQuery` with the initialization being the column name.
            
        Example:
            ```py
            >>> SQLQuery('OBJECTID').is_in(['1','2','3','4'].__str__()
            "OBJECTID IN (1,2,3,4)"
            >>> SQLQuery('FEATURE_ID').is_in(['001','002','003','004'], string_cast=True).__str__()
            "FEATURE_ID IN ('001','002','003','004')"
            ```
        """
        
        # Cast inputs to string for join operation
        sequence = list(map(str, sequence))
        if string_cast:
            sequence = [f"'{l}'" for l in sequence]
        return SQLQuery(f"{self.where_clause} IN ({','.join(sequence)})")
    
    def is_like(self, like: str) -> 'SQLQuery':
        """Builds a new SQLQuery with a LIKE clause
        Args:
            like: The LIKE match string
            
        Returns:
            SQLQuery
            
        Raises:
            None
            
        Note:
            This method is best used immediately upon creation of a new SQLQuery with the initialization being the column name.
            The `starts_with`, `ends_with`, and `contains` methods all use this and will place the wildcards for you.
            
        Example:
            ```py
            >>> SQLQuery('FEATURE_NAME').is_like('MA%').__str__()
            "FEATURE_NAME LIKE 'MA%'"
            ```
        """
        return SQLQuery(f"{self.where_clause} LIKE '{like}'")
    
    def starts_with(self, start: str) -> 'SQLQuery':
        """`start`%"""
        return SQLQuery(f"{self.where_clause} LIKE '{start}%'")
    
    def ends_with(self, end: str) -> 'SQLQuery':
        """%`end`"""
        return SQLQuery(f"{self.where_clause} LIKE '%{end}'")
    
    def contains(self, match: str) -> 'SQLQuery':
        """%`match`%"""
        return SQLQuery(f"{self.where_clause} LIKE '%{match}%'")

def as_dict(cursor: SearchCursor | UpdateCursor) -> Generator[dict, None, None]:
    yield from (dict(zip(cursor.fields, row)) for row in cursor)

@dataclass
class FeatureClass:
    path: PathLike
    where_clause: Optional[SQLQuery] = None
    spatial_filter: Optional[SpatialQuery] = None
    search_fields: list[str] = None
    
    def __post_init__(self):
        self.describe: dtype.FeatureClass = Describe(self.path)    
        self.editor: Editor = Editor(self.describe.workspace.catalogPath)
        self.field_names = [field.name for field in self.describe.fields]
        self.count: int = None
        
        if not self.search_fields:
            self.search_fields: list[str] = ['*']
    
    def build_queries(self):
        sf = self.spatial_filter or SpatialQuery()
        sq = self.where_clause or SQLQuery()
        return {
            'spatial_filter': sf.spatial_filter,
            'spatial_relationship': sf.spatial_relationship,
            'where_clause': sq.where_clause,
        }
    
    def __len__(self) -> int:
        if not self.count:
            self.count = len(list(SearchCursor(self.path, ['OID@'], **self.build_queries())))
        return self.count
    
    def __iter__(self) -> Generator:
        yield from SearchCursor(self.path, self.search_fields, **self.build_queries())
    
    def __getitem__(self, idx) -> tuple:
        if isinstance(idx, slice):
            rows = list(self) # Cache rows to prevent multiple cursors being opened
            return [rows[i] for i in range(*idx.indices(len(self)))]
                
        if isinstance(idx, int):
            if idx < 0:
                idx += len(self)
            if idx < 0 or idx >= len(self):
                raise IndexError(f"Index {idx} out of range")
            for count, row in enumerate(self):
                if idx == count:
                    return row
            
    @contextmanager
    def query(self, where_clause: SQLQuery=None, spatial_filter: SpatialQuery=None) -> Generator['FeatureClass', None, None]:
        # Store original state and clear count
        _where_clause = self.where_clause
        _spatial_filter = self.spatial_filter
        self.count = None
        
        # Fallback to stored query if not provided
        if not where_clause:
            where_clause = _where_clause
        if not spatial_filter:
            spatial_filter = _spatial_filter
        
        try:
            # Yield mutated self
            self.where_clause = where_clause
            self.spatial_filter = spatial_filter
            yield self
            
        finally:
            # Restore state
            self.spatial_filter = _spatial_filter
            self.where_clause = _where_clause
            # Recalculate length to account for changes during context
            self.count = None
            self.count = len(self)
    
    @contextmanager
    def fields(self, search_fields: list[str]=None) -> Generator['FeatureClass', None, None]:
        # Store original state and clear count
        _search_fields = self.search_fields
        self.count = None
        
        # Fallback to stored fields if none provided
        if not search_fields:
            search_fields = self.search_fields
        
        try:
            # Yield mutated self
            self.search_fields = search_fields
            yield self
            
        finally:
            # Restore state
            self.search_fields = _search_fields
            # Recalculate length to account for changes during context
            self.count = None
            self.count = len(self)
    
    @contextmanager
    def search(self) -> Generator[SearchCursor, None, None]:
        with SearchCursor(self.path, self.search_fields, **self.build_queries()) as cursor:
            yield cursor
    
    @contextmanager
    def update(self) -> Generator[UpdateCursor, None, None]:
        with UpdateCursor(self.path, self.search_fields, **self.build_queries()) as cursor:
            yield cursor
    
    @contextmanager
    def insert(self) -> Generator[InsertCursor, None, None]:
        with InsertCursor(self.path, self.search_fields) as cursor:
            yield cursor

    def delete(self, im_sure: bool=False) -> Generator:
        if not im_sure:
            raise ValueError("Deleting rows has no undo, please make sure `im_sure=True`")
        with UpdateCursor(self.path, ['OID@'], **self.build_queries()) as cursor:
            for row in cursor:
                yield row # Yield each deleted row for user to inspect
                cursor.deleteRow()