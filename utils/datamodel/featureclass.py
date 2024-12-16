from os import PathLike
from dataclasses import dataclass
from contextlib import contextmanager
from typing import Literal, TypeAlias, Optional, Generator, Self

from arcpy import Describe
import arcpy.typing.describe as dtype
from arcpy.da import Editor, SearchCursor, UpdateCursor, InsertCursor, ListSubtypes

from funcs.archelp import as_dict
from datamodel.queries import SpatialQuery, SQLQuery

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

ShapeTokens: TypeAlias = Literal[
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

@dataclass
class FeatureClass:
    path: PathLike
    where_clause: Optional[SQLQuery] = None
    spatial_filter: Optional[SpatialQuery] = None
    search_fields: list[str] = None
    dictionary_mode: bool = False
    
    def __post_init__(self):
        self.describe: dtype.FeatureClass = Describe(self.path)    
        self.editor: Editor = Editor(self.describe.workspace.catalogPath)
        self.field_names = [field.name for field in self.describe.fields]
        self.count: int = None
        self.subtypes: dict = {}
        self.subtype_field: str = None
        
        for code, info in ListSubtypes(self.path).items():
            if not self.subtype_field:
                self.subtype_field = info['SubtypeField']
            self.subtypes[code] = info['Name']
        
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
        with self.search() as cursor:
            for row in as_dict(cursor) if self.dictionary_mode else cursor:
                yield row
    
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
    def query(self, where_clause: SQLQuery=None, spatial_filter: SpatialQuery=None) -> Generator[Self, None, None]:
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
    def fields(self, search_fields: list[str]=None) -> Generator[Self, None, None]:
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