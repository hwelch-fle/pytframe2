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
        self._memory_hack(targ=models.Schema(self.default_gdb))
        
        sources = arcpy.Parameter(
            displayName="Source Databases",
            name="sources",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input",
            multiValue=True
        )
        
        features = arcpy.Parameter(
            displayName="Feature Classes",
            name="features",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            multiValue=True
        )
        features.filter.type = "ValueList"
        targ = self._memory_hack()[1]
        features.filter.list = list(targ._comparator_set)
        
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
        
        return [target, sources, features, ignore_schema_mismatch, inner_append]
    
    def updateParameters(self, parameters: list) -> None:
        
        params = archelp.Parameters(parameters)
        
        cur_srcs, cur_targ = self._memory_hack()
        if not cur_targ or params.target.value != cur_targ.path:
            self._memory_hack(targ=models.Schema(params.target.value))
        cur_srcs, cur_targ = self._memory_hack()
        params.features.filter.list = sorted(list(cur_targ._comparator_set))
                
        if params.ignore_schema_mismatch.value:
            params.sources.clearMessage()
            return
        
        if not params.sources.values:
            return
        
        for source in params.sources.values:
            if source not in cur_srcs:
                self._memory_hack(src=models.Schema(source))        
        return
    
    def updateMessages(self, parameters: list) -> None:
        
        params = archelp.Parameters(parameters)
        
        cur_srcs, cur_targ = self._memory_hack()
        
        if params.target.value and params.sources.values:
            warning = []
            error = []
            source_paths = []
            for source_schema in cur_srcs.values():
                if not cur_targ == source_schema:
                    selected_features = set(params.features.values) if params.features.values else set()
                    missing_from_target = source_schema._comparator_set - selected_features
                    missing_from_source = selected_features - source_schema._comparator_set
                    src_msg = f"Missing from source:\n\t\t{missing_from_source}"
                    targ_msg = f"Missing from target:\n\t\t{missing_from_target}"
                    warning.append(f"Schema mismatch:\n\t{targ_msg if targ_msg else ''}\n\t{src_msg if src_msg else ''}\n--------------------------------\n")
            if source_schema.path in source_paths:
                error.append(f"Duplicate source database: {source_schema.path}\n--------------------------------\n")
                source_paths.append(source_schema.path)
            if cur_targ.path == source_schema.path:
                error.append(f"{source_schema.path} and {cur_targ.path} are the same database\n--------------------------------\n")
            if error:
                params.sources.setErrorMessage(''.join(error))
            if warning:
                params.sources.setWarningMessage(''.join(warning))
            if not warning and not error:
                params.sources.clearMessage()
        return
    
    def execute(self, parameters:list, messages:list) -> None:
        params = archelp.Parameters(parameters)
        
        ignore_schema_mismatch = params.ignore_schema_mismatch.value
        inner_append = params.inner_append.value
        
        sources, target = self._memory_hack()
        
        target_tables = target.tables
        target_feature_classes = target.featureclasses
        
        if not sources or not target:
            message("No databases to merge!", "error")
            return
        
        for source in sources.values():
            if not ignore_schema_mismatch and source != target:
                message(f"Schema mismatch between {source.path} and {target.path}!\nRun with ignore schema mishmatch flag to append matching tables", "error")
                return
            if inner_append:
                for table in source.tables:
                    if table not in target.tables:
                        continue
                    target.append_table(table)
        
        return

    # This is disgusting, don't do this. It relies on a bug in Python's initialization of default arguments to store state because
    # Python toolboxes don't actually update self. variables in updateParameters and updateMessages calls
    def _memory_hack(self, src: models.Schema=None, targ:models.Schema=None,
                     sources: dict[str:models.Schema]={}, target:list[models.Schema]=[None]) -> tuple[dict[str, models.Schema], models.Schema]:
        """ DO NOT EVER DO THIS """
        if src:
            sources[src.path] = src
        if targ:
            target[0] = targ
        return (sources, target[0])