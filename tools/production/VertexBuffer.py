import arcpy

from utils.datamodel.tool import Tool
import utils.funcs.archelp as archelp
import utils.datamodel.models as models

class VertexBuffer(Tool):
    
    def __init__(self) -> None:
        super().__init__()
        self.label = "Vertex Buffer"
        self.description = "Buffers features by a distance around each vertex of the feature geometry."
        self.category = "Production"
        return
    
    def getParameterInfo(self) -> list:
        
        features = arcpy.Parameter(
            displayName="Input Features",
            name="features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )
        
        distance = arcpy.Parameter(
            displayName="Distance",
            name="distance",
            datatype="GPLinearUnit",
            parameterType="Required",
            direction="Input"
        )
        distance.value = "10 Meters"
        
        suffix = arcpy.Parameter(
            displayName="Suffix",
            name="suffix",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        suffix.value = "_10_Meter_Buffers"
        
        per_vertex = arcpy.Parameter(
            displayName="Per Vertex",
            name="per_vertex",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input"
        )
        
        return [features, distance, suffix, per_vertex]
    
    def updateParameters(self, parameters: list) -> None:
        params = archelp.Parameters(parameters)
        
        if params.distance.valueAsText == "":
            params.suffix.value = ""
        else:
            params.suffix.value = \
                f"_{archelp.sanitize_filename(params.distance.valueAsText).replace(' ' , '_')}{'_Vertex_' if params.per_vertex.value else '_'}Buffers"
            
        return
    
    def execute(self, parameters:list, messages:list) -> None:
        
        params = archelp.Parameters(parameters)
        
        per_vertex = params.per_vertex.value
                
        selection = params.features.value.getSelectionSet()
        if not selection:
            selection = None
        definition_query = params.features.value.definitionQuery
        if not definition_query:
            definition_query = None
        
        features: models.FeatureClass = models.FeatureClass(arcpy.Describe(params.features.valueAsText).catalogPath)

        if selection and definition_query:
            ids = [str(i) for i in selection]
            selection_query = f"{features.OIDField} IN ({','.join(ids)})"
            query = f"{definition_query} AND {selection_query}"
        elif selection:
            ids = [str(i) for i in selection]
            query = f"{features.OIDField} IN ({','.join(ids)})"
        elif definition_query:
            query = definition_query
        else:
            query = None
                    
        feature_units = features.spatialReference.linearUnitName.replace("_", "")
        
        distance, units = params.distance.valueAsText.split(" ")
        distance = float(distance)
        conversion = arcpy.LinearUnitConversionFactor(units, feature_units)
        
        suffix = params.suffix.valueAsText
        
        buffers: list[arcpy.Polygon] = []
        
        total = len(features)
        index = 0
        arcpy.SetProgressor("step", "Buffering Features", index, total, 1)
        for feature in features.get_rows(["SHAPE@"], where_clause=query):
            index += 1
            try:
                feature: arcpy.Geometry = feature[0]
                if per_vertex and features.shapeType != "PointGeometry":
                    for part in feature:
                        for point in part:
                            point = arcpy.PointGeometry(point, spatial_reference=features.spatialReference)
                            buffer = point.buffer(distance*conversion)
                            buffers.append(buffer)
                else:
                    buffer = feature.buffer(distance*conversion)
                    buffers.append(buffer)
            except Exception as e:
                arcpy.AddWarning(f"Error buffering feature: {e}\n{feature.JSON}")
            arcpy.SetProgressorPosition()
            arcpy.SetProgressorLabel(f"Buffering Features {index}/{total}")
            
        arcpy.CopyFeatures_management(buffers, f"{features.path}{suffix}")
        
        return