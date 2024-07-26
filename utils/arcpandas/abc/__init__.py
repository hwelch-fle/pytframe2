# This code is taken from the arcpy typing module shipped with arcpy.
# It is used as the base structure for the package interfaces

from typing import Literal

from .base import *
from .gdb import *
from .nd import *
from .tn import *
from .un import *

DescribeDataTypes = Literal[
    "ArcInfoItem",
    "ArcInfoTable",
    "BIMFileWorkspace",
    "CadDrawingDataset",
    "CadFeatureClass",
    "CadastralFabric",
    "Coverage",
    "CoverageFeatureClass",
    "DbaseTable",
    "FeatureClass",
    "FeatureSet",
    "File",
    "Folder",
    "GALayer",
    "GDBFeatureClass",
    "GDBTable",
    "GeometricNetwork",
    "LasDataset",
    "Layer",
    "LocationReferencingDataset",
    "MapDocument",
    "MosaicDataset",
    "NALayer",
    "NetworkDataset",
    "ParcelFabric",
    "ProjectionFile",
    "RasterBand",
    "RasterCatalog",
    "RasterDataset",
    "RecordSet",
    "RelationshipClass",
    "RepresentationClass",
    "SDCFeatureClass",
    "SchematicDataset",
    "SchematicDiagram",
    "SchematicFolder",
    "ShapeFile",
    "TIN",
    "Table",
    "TableView",
    "TextFile",
    "Tool",
    "Toolbox",
    "Topology",
    "TraceNetwork",
    "UtilityNetwork",
    "VPFCoverage",
    "VPFFeatureClass",
    "VPFTable",
    "Workspace",
]
