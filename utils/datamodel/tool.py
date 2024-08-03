import arcpy
import os
import pathlib
from pathlib import Path

from typing import Any
from abc import ABC

class Tool(ABC):
    
    # Set up a cache for the initialized values
    # An expensive initialization will massively slow down large toolboxes
    # because the init is called for every tool in the toolbox on load and every
    # time the tool opened.
    # 
    # When using the Tool cache, make sure that all initiliazation values are
    # immutable or will not change during the life of the toolbox.
    # Things like the project, named databases, etc. 
    # are good candidates for caching in the base tool class
    # Avoid caching things like the current map, layers, etc.
    # in the base class as they may change during the life of the toolbox
    # These values should be initiliazed in the tool subclasses only when they
    # are needed.
    init_cache: dict[str, Any] = {}
    
    """
    Base class for all tools that use python objects to build parameters
    """
    def __init__(self, *, invalidate_cache=False) -> None:
        """
        Base initializer for all tools
        
        @param invalidate_cache: If True, the cache will be invalidated and the
                                    tool will be re-initialized
        """
        # If a tool has already been initialized, use the cache
        if Tool.init_cache and not invalidate_cache:
            self.__dict__.update(Tool.init_cache)
            return
        
        # Tool parameters
        self.label = "Tool"
        self.description = "Base class for all tools"
        self.canRunInBackground = False
        self.category = "Unassigned"
        
        # Project variables
        self.project = arcpy.mp.ArcGISProject("CURRENT")
        self.project_location = self.project.homeFolder
        self.project_name = Path(self.project.filePath).stem
        
        # Database variables
        self.default_gdb = self.project.defaultGeodatabase
        self.databases = self.project.databases
        
        # Cache after first initialization
        Tool.init_cache = self.__dict__
        return
    
    def getParameterInfo(self) -> list[arcpy.Parameter]: ...
    def isLicensed(self) -> bool: return True
    def updateParameters(self, parameters: list[arcpy.Parameter]) -> None: ...
    def updateMessages(self, parameters: list[arcpy.Parameter]) -> None: ...
    def execute(self, parameters: list[arcpy.Parameter], messages:list[Any]) -> None: ...
    def postExecute(self, parameters: list[arcpy.Parameter]) -> None: ...
    