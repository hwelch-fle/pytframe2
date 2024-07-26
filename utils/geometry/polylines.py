import arcpy
from arcpy import Point, Multipoint, Array, Polyline, Polygon

from functools import reduce

def reverse_array(array: arcpy.Array) -> arcpy.Array:
    """ Reverse the order of an arcpy.Array """
    return arcpy.Array(array[::-1])

def merge_polylines(polylines: list[arcpy.Polyline]) -> arcpy.Polyline:
    """ Merge a list of polylines into a single polyline """
    return reduce(lambda combined, next: combined.union(next), polylines)

def explode_polyline(polyline: arcpy.Polyline) -> list[arcpy.Polyline]:
    """ Explode a polyline into its parts """
    if not polyline.isMultipart:
        return [polyline]
    return [arcpy.Polyline(part, polyline.spatialReference) for part in polyline]

def flip_polyline(polyline: arcpy.Polyline, reverse_parts: bool = False) -> arcpy.Polyline:
    """ Flips all segments of a polyline and optionally reverses part order
    
    Parameters
    ----------
    polyline : arcpy.Polyline
        The polyline to flip
    reverse_parts : bool, optional
        Reverse the order of the parts in the polyline, by default False
    
    Returns
    -------
    arcpy.Polyline
        The flipped polyline
    """    
    if not polyline.isMultipart:
        return arcpy.Polyline(reverse_array(polyline[0]), polyline.spatialReference)
    return merge_polylines(
        [
            flip_polyline(arcpy.Polyline(part, polyline.spatialReference))
            for part in polyline
        ][::reverse_parts and -1 or 1] # Some python magic to convert a boolean to forward or reverse slice step 
        )