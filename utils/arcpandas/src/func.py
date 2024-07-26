from arcpy.da import SearchCursor, UpdateCursor

from typing import Any, Generator


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