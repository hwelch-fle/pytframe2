from dataclasses import dataclass
from typing import Literal, TypeAlias, Optional

from arcpy import Geometry

SpatialRelationship: TypeAlias = Literal[
    'INTERSECTS', 
    'ENVELOPE_INTERSECTS', 
    'INDEX_INTERSECTS', 
    'TOUCHES', 
    'CROSSES', 
    'WITHIN', 
    'CONTAINS',
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
            sequence = [f"'{elem}'" for elem in sequence]
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