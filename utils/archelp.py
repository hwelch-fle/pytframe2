import arcpy
import os
import shutil
import json

from enum import Enum

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

class Parameter(arcpy.Parameter):
    def __init__(self, name: str=None, displayName: str=None, datatype: str=None, parameterType: str=None, direction: str=None, controlCLSID: str=None, category: str=None, **kwargs) -> None:
        super().__init__(name, displayName, datatype, parameterType, direction, controlCLSID **kwargs)
        return

class Parameters(object):
    """ Parameters class to store the parameters of a tool """
    def __init__(self, parameters: list) -> None:
        self._parameters = parameters
        for parameter in parameters:
            self.__dict__[parameter.name] = parameter
        return
    
    def __iter__(self):
        for _, value in self._parameters.items():
            yield value
        return
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
def sanitize_filename(filename: str) -> str:
    """ Sanitize a filename """
    return "".join([char for char in filename if char.isalnum() or char in [" ", "_", "-"]])

def message(message: str, severity: str = "info") -> None:
    """ Print a message """
    match severity.lower():
        case "info":
            arcpy.AddMessage(message)
            print(f"info: {message}")
        case "warning":
            arcpy.AddWarning(message)
            print(f"warning: {message}")
        case "error":
            arcpy.AddError(message)
            print(f"error: {message}")
    return
        