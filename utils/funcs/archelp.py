import arcpy
import builtins
from pprint import pformat
import time
import functools
from functools import wraps, reduce, partial
import sys
import pip
import os
import shutil
import json
from pathlib import Path
from typing import Literal, Any, Generator
from enum import Enum

# Trick for avoiding circular imports (models uses print function defined here)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from datamodel.models import FeatureClass


class controlCLSID(Enum):
    """ See [Parameter Controls](https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/parameter-controls.htm)
        documentation for more information on parameter controls.
    """
    EXCLUDE_INTERSECT_AND_UNION = '{15F0D1C1-F783-49BC-8D16-619B8E92F668}'
    SLIDER_RANGE = '{C8C46E43-3D27-4485-9B38-A49F3AC588D9}'
    LARGE_NUMBER = '{7A47E79C-9734-4167-9698-BFB00F43AE41}'
    COMPOSITE_SWITCH = '{BEDF969C-20D2-4C41-96DA-32408CA72BF6}'
    MULTILINE = '{E5456E51-0C41-4797-9EE4-5269820C6F0E}'
    MULTIVALUE_CHECKBOX = '{172840BF-D385-4F83-80E8-2AC3B79EB0E0}'
    MULTIVALUE_CHECK_ALL = '{38C34610-C7F7-11D5-A693-0008C711C8C1}'
    FEATURE_LAYER_CREATE = '{60061247-BCA8-473E-A7AF-A2026DDE1C2D}'
    HORIZONTAL_VALUE_TABLE = '{1AA9A769-D3F3-4EB0-85CB-CC07C79313C8}'
    SINGLE_VALUE_TABLE = '{1A1CA7EC-A47A-4187-A15C-6EDBA4FE0CF7}'

class Parameters(list):
    """ Parameters class that replaces the list of parameters in the tool functions
        with an object that can be access the parameters by name, index, or attribute.
    
        USAGE
            You still need tool functions to return a list of parameters as the parameters list
            is rebuilt each time it is passed beteween the tool functions. That list can be immediately
            converted to a Parameters object at the beginning of the function.
        >>> def execute(self, parameters: list[arcpy.Parameter]) -> None:
        >>>     parameters = Parameters(parameters)
        >>>     paramA = parameters.paramA.value
        or
        >>>     paramA = parameters['paramA'].value
        or
        >>>     paramA = parameters[0].value
        Assuming that paramA is the first parameter in the list of parameters
    """
      
    def __init__(self, parameters: list[arcpy.Parameter]) -> None:
        self.__dict__.update({parameter.name: parameter for parameter in parameters})
        return
    
    def __iter__(self) -> Generator[arcpy.Parameter, None, None]:
        for value in self.__dict__.values():
            yield value
        return
    
    def __len__(self) -> int:
        return len(self.__dict__)
    
    def __getitem__(self, key) -> arcpy.Parameter:
        if isinstance(key, int):
            return list(self)[key]
        return self.__dict__[key]
    
    def __setitem__(self, key, value) -> None:
        if isinstance(key, int):
            self.__dict__[list(self.__dict__)[key]] = value
        self.__dict__[key] = value
        return
    
    def __getattr__(self, name: str) -> arcpy.Parameter:
        if name in self.__dict__:
            return self.__dict__[name]
        return super().__getattribute__(name)
    
    def append(self, parameter: arcpy.Parameter) -> None:
        if not isinstance(parameter, arcpy.Parameter):
            raise TypeError(f"Parameter must be of type arcpy.Parameter, not {type(parameter)}")
        self.__dict__[parameter.name] = parameter
    
    def extend(self, parameters: list[arcpy.Parameter]) -> None:
        for parameter in parameters:
            self.append(parameter)
    
    def __repr__(self) -> str:
        return str(list(self.__dict__.values()))
    
def sanitize_filename(filename: str) -> str:
    """ Sanitize a filename """
    return "".join([char for char in filename if char.isalnum() or char in [' ', '_', '-']])

def print(*values: object,
          sep: str = " ",
          end: str = "\n",
          file = None,
          flush: bool = False,
          severity: Literal['INFO', 'WARNING', 'ERROR'] = None):
    """ Print a message to the ArcGIS Pro message queue and stdout
    set severity to 'WARNING' or 'ERROR' to print to the ArcGIS Pro message queue with the appropriate severity
    """

    # Print the message to stdout
    builtins.print(*values, sep=sep, end=end, file=file, flush=flush)
    
    end = "" if end == '\n' else end
    message = f"{sep.join(map(str, values))}{end}"
    # Print the message to the ArcGIS Pro message queue with the appropriate severity
    match severity:
        case "WARNING":
            arcpy.AddWarning(f"{message}")
        case "ERROR":
            arcpy.AddError(f"{message}")
        case _:
            arcpy.AddMessage(f"{message}")
    return

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
    :param polyline: arcpy.Polyline
        The polyline to flip
    :param reverse_parts: bool, optional
        Reverse the order of the parts in the polyline, by default False
    :return: arcpy.Polyline
        The flipped polyline
    """   
    if not polyline.isMultipart:
        return arcpy.Polyline(reverse_array(polyline[0]), polyline.spatialReference)
    return merge_polylines(
        [
            flip_polyline(part)
            for part in explode_polyline(polyline)
        ][::reverse_parts and -1 or 1] # Some python magic to convert a boolean to forward or reverse slice step 
        )

def polyline_from_pointgeo(pointgeos: list[arcpy.PointGeometry], spatial_reference: arcpy.SpatialReference=None) -> arcpy.Polyline:
    """Creates a polyline from a list of point geometries
    @pointgeo: An ordered list of point geometries to create the polyline from
    @spatial_reference: The spatial reference of the polyline (default: None)
    @return: The polyline
    """
    if any(pointgeo.isMultipart for pointgeo in pointgeos):
        raise ValueError("Multipart PointGeometries can not be converted to a Polyline")
    return arcpy.Polyline((point.centroid for point in pointgeos), spatial_reference=spatial_reference)

def split_polyline(polyline: arcpy.Polyline, points: list[arcpy.PointGeometry]) -> list[arcpy.Polyline]:
    """
    Split a polyline at points and yield the segments
    """
    # Order the points
    points = sorted(points, key=lambda point: polyline.measureOnLine(point))
    
    last_measure = 0
    segments = []
    for point in points:
        measure = polyline.measureOnLine(point)
        if last_measure == measure: continue # Skip first
        
        segments.append(polyline.segmentAlongLine(last_measure, measure))
        last_measure = measure
    return segments

def find_route(edges: list[arcpy.Polyline], root: arcpy.PointGeometry, target: arcpy.PointGeometry,*,
               max_depth: int = -1,
               _route: list[arcpy.Polyline] | None = None) -> arcpy.Polyline | None:
    """ 
    Finds the shortest path between two points in a list of polylines.
    
    This function is a recursive depth-first search algorithm that finds the 
    shortest path between two points. As such, it is not the most efficient
    algorithm for large networks. 
    
    Best used on networks with 10-20 edges.
    
    :param edges: List of polylines (Polyline)
    :param root: Starting point (PointGeometry)
    :param target: Ending point (PointGeometry)
    :param max_depth: Maximum depth of the recursion (int) (default: -1)
    
    :return: Shortest path between start and end (Polyline) or None
    """
    if max_depth == 0:
        raise RecursionError(f"Max depth of {max_depth} reached")
    
    if _route is None:
        _route = []
        # Immediately return None if the root or target are not on any edge
        if not any(edge.touches(root) for edge in edges):
            return None
        if not any(edge.touches(target) for edge in edges):
            return None
        
    # Base condition
    if root == target:
        return merge_polylines(_route)
    
    # Next branches
    adjacent_edges = \
        [
            edge 
            for edge in edges 
            if edge.touches(root) and not any(edge == routed for routed in _route)
        ]
        
    # Remove the next edges from the list of edges to prevent backtracking
    edges = [edge for edge in edges if not any(edge == adj for adj in adjacent_edges)]
    for edge in adjacent_edges:
        # Convert the edge extremities to PointGeometry objects
        first, last = arcpy.PointGeometry(edge.firstPoint, edge.spatialReference), arcpy.PointGeometry(edge.lastPoint, edge.spatialReference)
        # Get the next root
        next_root = first if not first == root else last
        # Recursively find the route for each edge
        route_found = find_route(edges, next_root, target, _route=_route + [edge], max_depth=max_depth - 1)
        # When the route is found, return it
        if route_found:
            return route_found

def find_route_bfs(edges: list[arcpy.Polyline], 
                   root: arcpy.PointGeometry, 
                   target: arcpy.PointGeometry) -> arcpy.Polyline | None:
    """ 
    Finds a path between two points in a list of polylines using a breadth-first search algorithm. 
    
    :param edges: List of polylines (Polyline)
    :param root: Starting point (PointGeometry)
    :param target: Ending point (PointGeometry)
    
    :return: Shortest path between start and end (Polyline) or None
    """
    # Create an edge dictionary
    edge_dict = {idx: edge for idx, edge in enumerate(edges)}
    
    # Create visited set
    visited = set()
    
    # Create a queue to store the root edges
    queue = [[idx] for idx, edge in edge_dict.items() if edge.touches(root)]
    
    while queue:
        # Get the next route
        route = queue.pop(0)
        # Get the last edge in the route
        last_edge = edge_dict[route[-1]]
        # Get the last point of the last edge
        last_point = arcpy.PointGeometry(last_edge.lastPoint, last_edge.spatialReference)
        # If the last point is the target, return the route
        if last_point == target:
            return merge_polylines([edge_dict[idx] for idx in route])
        # If the last point is not the target, add the last point to the visited set
        visited.add(last_point)
        # Get the next edges
        next_edges = [idx for idx, edge in edge_dict.items() if idx not in visited and edge.touches(last_point)]
        # Add the next edges to the queue
        queue.extend([route + [idx] for idx in next_edges])
        
    return None

def to_feature_units(features: "FeatureClass", linear_units: str) -> float:
    """ Synchronize the linear unit of a feature class with a linear unit string
    :param features: The feature class to synchronize
    :param linear_unit: The linear unit string to synchronize with
    :return: The converted linear unit
    """
    # Get the value and unit of the linear unit string
    distance, unit = linear_units.split()
    distance = float(distance)
    
    # Get the linear unit of the feature class
    feature_unit = features.describe.spatialReference.linearUnitName
    
    if feature_unit == unit: return 1
    
    # Get the conversion factor
    conversion_factor = arcpy.LinearUnitConversionFactor(unit, feature_unit)
    return distance*conversion_factor

def perf_timer(func: callable, label: str=None) -> callable:
    """ Decorator for timing the execution of a function """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{label}: {func.__name__} executed in {end-start:.4f} seconds")
        return result
    return wrapper

from datamodel.models import FeatureClass