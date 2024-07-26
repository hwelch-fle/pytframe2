from arcpy import SpatialReference, Extent
from arcpy import env
from typing import Any, Literal, TypeAlias
from os import PathLike
from dataclasses import dataclass

# Type Aliases for string literals

LinearUnit = Literal[
    'Kilometers', 
    'Meters', 
    'Decimeters', 
    'Centimeters', 
    'Millimeters', 
    'Points', 
    'NauticalMiles', 
    'NauticalMilesUS', 
    'NauticalMilesInt', 
    'Miles', 
    'MilesUS', 
    'MilesInt', 
    'Yards', 
    'YardsUS', 
    'YardsInt', 
    'Feet', 
    'FeetUS', 
    'FeetInt', 
    'Inches', 
    'InchesUS', 
    'InchesInt',
    ]

CellSizes: TypeAlias = Literal[
    'MAXOF', 
    'MINOF', 
    'number', 
    'layer name',
    ]

CellAlignment: TypeAlias = Literal[
    'DEFAULT', 
    'ALIGN_WITH_PROCESSING_EXTENT', 
    'ALIGN_WITH_INPUT',
    ]

CellProjectionMethods: TypeAlias = Literal[
    'CONVERT_UNITS', 
    'PRESERVE_RESOLUTION', 
    'CENTER_OF_EXTENT',
    ]

PointConfig: TypeAlias = Literal[
    'MEAN', 
    'REMOVE_ALL', 
    'MIN', 
    'MAX', 
    'SUM', 
    'INCLUDE_ALL',
    ]

CompressionTypes: TypeAlias = Literal[
    'LZ77', 
    'LERC', 
    'JPEG', 
    'JPEG_YCbCr', 
    'JPEG2000', 
    'PackBits', 
    'LZW', 
    'RLE', 
    'CCITT_G3', 
    'CCITT_G4', 
    'CCITT_1D',
    ]

SDEConfig: TypeAlias = Literal[
    'ST_GEOMETRY', 
    'SDO_GEOMETRY', 
    'PG_GEOMETRY', 
    'PG_GEOGRAPHY', 
    'GEOMETRY', 
    'GEOGRAPHY',
    ]

GDBConfig: TypeAlias = Literal[
    'DEFAULTS', 
    'TEXT_UTF16', 
    'MAX_FILE_SIZE_4GB', 
    'MAX_FILE_SIZE_256TB', 
    'GEOMETRY_OUTOFLINE', 
    'BLOB_OUTOFLINE', 
    'GEOMETRY_AND_BLOB_OUTOFLINE',
    ]

NoData: TypeAlias = Literal[
    'NONE', 
    'MAXIMUM', 
    'MINIMUM', 
    'MAP_UP', 
    'MAP_DOWN', 
    'PROMOTION',
    ]

OutputMZFlag: TypeAlias = Literal[
    'Same As Input', 
    'Enabled', 
    'Disabled',
    ]

ProcessorType: TypeAlias = Literal[
    'CPU', 
    'GPU', 
    None,
    ]

RandomType: TypeAlias = Literal[
    'ACM599', 
    'MERSENNE_TWISTER', 
    'STANDARD_C',
    ]

PyramidOption: TypeAlias = Literal[
    'NONE', 
    'PYRAMIDS',
    ]

PyramidLevels: TypeAlias = Literal[
    '-1', '0', '1', '2', '3', '4', '5', 
    '6', '7', '8', '9', '10', '11', '12', 
    '13', '14', '15', '16', '17', '18', 
    '19', '20', '21', '22', '23', '24', 
    '25', '26', '27', '28', '29',
    ]

Interpolation: TypeAlias = Literal[
    'NEAREST', 
    'BILINEAR', 
    'CUBIC',
    ]

PyramidSkip: TypeAlias = Literal[
    'NO_SKIP', 
    'SKIP_FIRST'
    ]

PyramidConfig: TypeAlias = tuple[
    PyramidOption,
    PyramidLevels, 
    Interpolation, 
    CompressionTypes, 
    int, 
    PyramidSkip,
    ]

RasterCalculateStatistics: TypeAlias = Literal[
    'STATISTICS', 
    'NONE',
    ]

RasterIgnore: TypeAlias = tuple[int, int]

TinVersion: TypeAlias = Literal[
    'CURRENT', 
    'PRE_10.0',
    ]

UNSET = object()

@dataclass
class Environment:
    _existing_env: dict[str, Any] = UNSET
    addOutputsToMap: bool = UNSET
    annotationTextStringFieldLength: int = UNSET
    autoCancelling: bool = UNSET
    autoCommit: int = UNSET
    baDataSource: str = UNSET
    baNetworkSource: str = UNSET
    baUseDetailedAggregation: bool = UNSET
    buildStatsAndRATForTempRaster: bool = UNSET
    cartographicCoordinateSystem: SpatialReference | str = UNSET
    cartographicPartitions: str = UNSET
    cellAlignment: CellAlignment = UNSET
    cellSize: CellSizes = UNSET
    cellSizeProjectionMethod: str = UNSET
    coincidentPoints: PointConfig = UNSET
    compression: CompressionTypes = UNSET
    configKeyword: GDBConfig | SDEConfig = UNSET
    daylightSaving: bool = UNSET
    extent: Extent = UNSET
    geographicTransformations: str = UNSET
    gpuId: int = UNSET
    isCancelled: bool = UNSET
    maintainAttachments: bool = UNSET
    maintainCurveSegments: bool = UNSET
    maintainSpatialIndex: bool = UNSET
    mask: str = UNSET
    matchMultidimensionalVariable: bool = UNSET
    MDomain: str = UNSET
    MResolution: float = UNSET
    MTolerance: float = UNSET
    nodata: NoData = UNSET
    outputCoordinateSystem: SpatialReference | str = UNSET
    outputMFlag: OutputMZFlag = UNSET
    outputZFlag: OutputMZFlag = UNSET
    outputZValue: float = UNSET
    overwriteOutput: bool = UNSET
    packageWorkspace: PathLike = UNSET
    parallelProcessingFactor: str = UNSET
    preserveGlobalIds: bool = UNSET
    processingServer: str = UNSET
    processingServerPassword: str = UNSET
    processingServerUser: str = UNSET
    processorType: ProcessorType = UNSET
    pyramid: PyramidOption | PyramidLevels | Interpolation | CompressionTypes | int | PyramidSkip = UNSET
    qualifiedFieldNames: bool = UNSET
    randomGenerator: int | RandomType = UNSET
    rasterStatistics: RasterCalculateStatistics | int | int | RasterIgnore = UNSET
    recycleProcessingWorkers: int = UNSET
    referenceScale: int = UNSET
    resamplingMethod: Interpolation = UNSET
    retryOnFailures: int = UNSET
    S100FeatureCatalogueFile: str = UNSET
    scratchFolder: PathLike = UNSET
    scratchGDB: PathLike = UNSET
    scratchWorkspace: PathLike = UNSET
    scriptWorkspace: PathLike = UNSET
    snapRaster: PathLike = UNSET
    terrainMemoryUsage: bool = UNSET
    tileSize: int | int = UNSET
    timeZone: str = UNSET
    tinSaveVersion: TinVersion = UNSET
    transferDomains: bool = UNSET
    transferGDBAttributeProperties: bool = UNSET
    unionDimension: bool = UNSET
    useCompatibleFieldTypes: bool = UNSET
    workspace: PathLike = UNSET
    XYDomain: str = UNSET
    XYResolution: float | LinearUnit = UNSET
    XYTolerance: float | LinearUnit = UNSET
    ZDomain: str = UNSET
    ZResolution: float | LinearUnit = UNSET
    ZTolerance: float | LinearUnit = UNSET
    
    def __enter__(self):
        self._existing_env = dict(env)
        for key, value in self.__dict__.items():
            if hasattr(env, key):
                if env[key] == value or value is UNSET: continue
                try:
                    setattr(env, key, value)
                except IndexError as e:
                    print(f"Invalid value ({value}) for {key}\n{e}")
                except AttributeError:
                    continue # Ignore read-only properties
    
    def __exit__(self, exc_type, exc_value, traceback):
        for key, value in self._existing_env.items():
            try:
                setattr(env, key, value)
            except IndexError as e:
                print(f"Invalid value ({value}) for {key}\n{e}")
            except AttributeError:
                continue # Ignore read-only properties
        self._existing_env = UNSET
    
    def __repr__(self) -> str:
        values = ", ".join(f"{k}={v}" for k, v in self.__dict__.items() if v is not UNSET)
        return f"Environment: {values}"
    
    def __str__(self) -> str:
        return repr(self)
