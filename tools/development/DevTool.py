from typing import Any
from arcpy.arcobjects import Parameter
from utils.datamodel.tool import Tool
from utils.datamodel.models import FeatureClass
from utils.funcs.archelp import print

class DevTool(Tool):
    def __init__(self):
        super().__init__()
        
        self.category = "Test"
        self.label = "Dev Tool"
        self.alias = self.label.replace(" ", "")
        self.description = "Placeholder tool for development tools"
        return
    def execute(self, parameters: list[Parameter], messages: list[Any]) -> None:
        print("Hello World!")
        return