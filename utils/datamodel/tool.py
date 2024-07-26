import arcpy
import os

from typing import Any
from abc import ABC

class Tool(ABC):
    """
    Base class for all tools that use python objects to build parameters
    """
    def __init__(self) -> None:
        """
        Tool Description
        """
        # Tool parameters
        self.label = "Tool"
        self.description = "Base class for all tools"
        self.canRunInBackground = False
        self.category = "Unassigned"
        
        # Project variables
        self.project = arcpy.mp.ArcGISProject("CURRENT")
        self.project_location = self.project.homeFolder
        self.project_name = os.path.basename(self.project_location)
        
        # Database variables
        self.default_gdb = self.project.defaultGeodatabase
        self.databases = self.project.databases
        return
    
    def getParameterInfo(self) -> list[arcpy.Parameter]: ...
    def isLicensed(self) -> bool: return True
    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None: ...
    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None: ...
    def execute(self, parameters: list[arcpy.Parameter], messages:list[Any]) -> None: ...
    def postExecute(self, parameters: list[arcpy.Parameter]) -> None: ...