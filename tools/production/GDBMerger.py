import arcpy
from arcpy import Parameter

from utils.datamodel.tool import Tool
from utils.datamodel.models import Table, Workspace
import utils.funcs.archelp as archelp
from utils.funcs.archelp import print, Parameters

class GDBMerger(Tool):
    def __init__(self):
        super().__init__()
        
        self.category = "Utilities"
        self.label = "GDB Merger"
        self.alias = self.label.replace(" ", "")
        self.description = "Merges multiple file geodatabases into a single file geodatabase."
        return

    def getParameterInfo(self) -> list[Parameter]:
        input_gdbs = Parameter(
            displayName="Input Geodatabases",
            name="input_gdbs",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input",
            multiValue=True,
        )
        
        target_gdb = Parameter(
            displayName="Target Geodatabase",
            name="target_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input",
        )
        
        # Do not attempt to merge any database that does not match the target schema
        strict_merge = Parameter(
            displayName="Strict Merge",
            name="strict_merge",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input",
        ) 
        strict_merge.value = False
        
        features_to_merge = Parameter(
            displayName="Features to Merge",
            name="features_to_merge",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            multiValue=True,
        )
        features_to_merge.filter.type = "ValueList"
        
        tables_to_merge = Parameter(
            displayName="Tables to Merge",
            name="tables_to_merge",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
            multiValue=True,
        )
        tables_to_merge.filter.type = "ValueList"
        
        return [input_gdbs, target_gdb, strict_merge, features_to_merge, tables_to_merge]
    
    def updateParameters(self, parameters: list[Parameter]) -> None:
        parameters = Parameters(parameters)
        if parameters.target_gdb.value and parameters.target_gdb.altered:
            wsp = Workspace(parameters.target_gdb.valueAsText)
            parameters.features_to_merge.filter.list = list(wsp.featureclasses)
            parameters.tables_to_merge.filter.list = list(wsp.tables)
        return
    
    def execute(self, parameters: list[Parameter], messages: list[object]) -> None:
        parameters = Parameters(parameters)
        if not parameters.features_to_merge.values and not parameters.tables_to_merge.values:
            print("No features or tables selected to merge", severity="ERROR")
            return
        
        arcpy.SetProgressor("step", "Reading Target Schema", 0, 1, 1)
        features_to_merge = None
        tables_to_merge = None
        if parameters.features_to_merge.values:
            features_to_merge: list[str] = [str(v).split('/')[-1] for v in parameters.features_to_merge.values]
        if parameters.tables_to_merge.values:
            tables_to_merge: list[str] = [str(v) for v in parameters.tables_to_merge.values]
            
        input_gdbs: list[object] = parameters.input_gdbs.values
        target_gdb: Workspace = Workspace(parameters.target_gdb.valueAsText, 
                                          featureclass_filter=features_to_merge, 
                                          table_filter=tables_to_merge)
        strict_merge: bool = parameters.strict_merge.value
        arcpy.ResetProgressor()
        
        for gdb_idx, input_gdb in enumerate(input_gdbs, start=1):
            arcpy.SetProgressor("step", "Reading Next Input Schema", gdb_idx, len(input_gdbs), 1)
            input_gdb = Workspace(arcpy.Describe(input_gdb).catalogPath, 
                                  featureclass_filter=features_to_merge, 
                                  table_filter=tables_to_merge)
            
            # Abide by strict merge rules on a per-geodatabase basis
            if not (target_gdb == input_gdb) and strict_merge:
                strict_merge_warning(input_gdb, target_gdb)
                continue
            
            print(f"Merging {input_gdb.name} into {target_gdb.name}")
            to_merge = input_gdb & target_gdb
            for tbl_idx, table in enumerate(to_merge, start=1):
                source: Table = input_gdb[table]
                target: Table = target_gdb[table]
                
                if len(source) == 0:
                    print(f"\t{source.name} has no rows to merge! ⛔")
                    continue
                
                print(f"\t{source.name} {tbl_idx}/{len(to_merge)}: {len(source)} rows")
                
                # Abide by strict merge rules on a per-table basis
                if not source == target and strict_merge:
                    strict_merge_warning(source, target)
                    continue
                
                matching_fields = source & target
                # Append rows from source to target
                arcpy.SetProgressorLabel(f"Appending {source.name} to {target.name}")
                try:
                    merge_tables(source, target, matching_fields)
                except Exception as e:
                    print(f"\t\t{source.name} failed to merge: {e}", severity="ERROR")
                    continue
                print(f"\t\t{source.name} merged successfully ✔️ ({len(source)} rows)")
            arcpy.SetProgressorPosition()
        return

def merge_tables(source: Table, target: Table, matching_fields: list[str]):
    # Start an edit session on the target table
    with target.editor:
        # Get the target table's insert cursor
        with target.insert_cursor(matching_fields) as cursor:
            # Get the source table's search cursor
            with source.search_cursor(matching_fields) as rows:
                # Append each row from the source table to the target table
                for row_idx, row in enumerate(rows, start=1):
                    cursor.insertRow(row)
                    arcpy.SetProgressorLabel(f"Appending {source.name} to {target.name} ({row_idx}/{len(source)})")
    return

def strict_merge_warning(source: Table | Workspace, target: Table | Workspace):
    missing = target - source
    additional = source - target
    print(f"\t\t{source.name} does not match target schema", severity="WARNING")
    if missing:
        print(f"\t\t\tMissing from {source.name}:\n{missing}", severity="WARNING")
    if additional:
        print(f"\t\t\tAdditional in {source.name}:\n{additional}", severity="WARNING")