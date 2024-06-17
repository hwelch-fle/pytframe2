import arcpy

from utils.tool import Tool
import utils.archelp as archelp
import utils.models as models

from utils.archelp import message

class DatabaseMerger(Tool):
    
    def __init__(self) -> None:
        super().__init__()
        self.label = "Database Merger"
        self.description = "Merges databases with identical schemas."
        self.category = "Utilities"
        
        self.sources: dict[str, models.Schema] = {}
        self.target: models.Schema = None
        return
    
    def getParameterInfo(self) -> list:
        
        target = arcpy.Parameter(
            displayName="Target Database",
            name="target",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )
        target.value = self.default_gdb
        self._fake_memory(targ=models.Schema(self.default_gdb))
        
        sources = arcpy.Parameter(
            displayName="Source Databases",
            name="sources",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input",
            multiValue=True
        )
        
        ignore_schema_mismatch = arcpy.Parameter(
            displayName="Ignore Schema Mismatch",
            name="ignore_schema_mismatch",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )
        ignore_schema_mismatch.value = False
        
        inner_append = arcpy.Parameter(
            displayName="Inner Append",
            name="inner_append",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )
        inner_append.value = False
        
        return [target, sources, ignore_schema_mismatch, inner_append]
    
    def updateParameters(self, parameters: list) -> None:
        
        params = archelp.Parameters(parameters)
        
        cur_srcs, cur_targ = self._fake_memory()
        
        if params.ignore_schema_mismatch.value:
            params.sources.clearMessage()
            return
        
        if not params.sources.values or not params.target.value:
            return
        
        for source in params.sources.values:
            if source not in cur_srcs:
                self._fake_memory(src=models.Schema(source))
        
        if not cur_targ or params.target.value != cur_targ.path:
            self._fake_memory(targ=models.Schema(params.target.value))
        return
    
    def updateMessages(self, parameters: list) -> None:
        
        params = archelp.Parameters(parameters)
        
        cur_srcs, cur_targ = self._fake_memory()
        
        if params.target.value and params.sources.values:
            warning = []
            error = []
            source_paths = []
            for source_schema in cur_srcs.values():
                if not cur_targ == source_schema:
                    if cur_targ.path == source_schema.path:
                        error.append(f"{source_schema.path} and {cur_targ.path} are the same database\n--------------------------------\n")
                    missing_from_target = source_schema - cur_targ
                    missing_from_source = cur_targ - source_schema
                    src_msg = f"Missing from source:\n\t\t{missing_from_source}"
                    targ_msg = f"Missing from target:\n\t\t{missing_from_target}"
                    warning.append(f"Schema mismatch:\n\t{targ_msg if targ_msg else ''}\n\t{src_msg if src_msg else ''}\n--------------------------------\n")
                if source_schema.path in source_paths:
                    error.append(f"Duplicate source database: {source_schema.path}\n--------------------------------\n")
                source_paths.append(source_schema.path)
            if warning:
                params.sources.setWarningMessage(''.join(warning))
            if error:
                params.sources.setErrorMessage(''.join(error))
            if not warning and not error:
                params.sources.clearMessage()
        return
    
    def execute(self, parameters:list, messages:list) -> None:
        params = archelp.Parameters(parameters)
        cur_srcs, cur_targ = self._fake_memory()
        message(f"Target: {cur_targ}")
        message(f"Sources: {str(cur_srcs)}")
        
        return

    # This is disgusting, don't do this
    def _fake_memory(self, src: models.Schema=None, targ:models.Schema=None, 
                     sources: dict[str:models.Schema]={}, target:list[models.Schema]=[None]) -> tuple[dict[str, models.Schema], models.Schema]:
        if src:
            sources[src.path] = src
        if targ:
            target[0] = targ
        return (sources, target[0])