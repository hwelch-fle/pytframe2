import arcpy

__all__ = [
    "Workspace",
    "Table",
    "FeatureClass",
    "Layer",
    "RasterBand",
    "RasterDataset",
    "ArcInfoItem",
    "ArcInfoTable",
    "BIMFileWorkspace",
    "CadDrawingDataset",
    "CadFeatureClass",
    "CoverageFeatureClass",
    "Coverage",
    "DbaseTable",
    "File",
    "Folder",
    "GALayer",
    "LasDataset",
    "MapDocument",
    "MosaicDataset",
    "ProjectionFile",
    "RecordSet",
    "FeatureSet",
    "ShapeFile",
    "TableView",
    "TextFile",
    "TIN",
    "Tool",
    "Toolbox",
    "VPFCoverage",
    "VPFFeatureClass",
    "VPFTable",
]

class _Base:
    @property
    def baseName(self) -> str:
        """The file base name."""
    @property
    def catalogPath(self) -> str:
        """The path of the data."""
    @property
    def children(self) -> list["Base"]:
        """
        A list of sub elements.
        If describing a workspace, the children property returns the contents of that workspace, including various data types such as feature classes, tables, rasters, and feature datasets.
        """
    @property
    def childrenExpanded(self) -> bool:
        """Indicates whether the children have been expanded."""
    @property
    def dataElementType(self) -> str:
        """The element type of the element."""
    @property
    def dataType(self) -> str:
        """The type of the element."""
    @property
    def extension(self) -> str:
        """The file extension."""
    @property
    def file(self) -> str:
        """The file name."""
    @property
    def fullPropsRetrieved(self) -> bool:
        """Indicates whether full properties have been retrieved."""
    @property
    def metadataRetrieved(self) -> bool:
        """Indicates whether the metadata has been retrieved."""
    @property
    def name(self) -> str:
        """The user-assigned name for the element."""
    @property
    def path(self) -> str:
        """The file path."""

class _Workspace(_Base):
    @property
    def connectionProperties(self):
        """
        connectionProperties is a property set.
        The connection properties for an enterprise geodatabase workspace will vary depending on the type of enterprise database being used.
        """
    @property
    def connectionString(self) -> str:
        """The connection string that is used in conjunction with the enterprise database type. For any other workspace type, an empty string is returned."""
    @property
    def currentRelease(self) -> bool:
        """For a geodatabase workspace, specifies whether the geodatabase's version is current. This property can be used to assess whether the geodatabase can be upgraded."""
    @property
    def domains(self) -> str:
        """A list containing the geodatabase domain names. To work with these domain names, you can use tools in the Domains toolset."""
    @property
    def release(self) -> str:
        """For a geodatabase workspace, returns the geodatabase release value."""
    @property
    def supportsBigInteger(self) -> bool:
        """Specifies whether the workspace supports Big Integer type fields."""
    @property
    def supportsBigObjectID(self) -> bool:
        """Specifies whether the workspace supports objects with 64-bit Object ID."""
    @property
    def supportsDateOnly(self) -> bool:
        """Specifies whether the workspace supports fields of type Date Only."""
    @property
    def supportsTimeOnly(self) -> bool:
        """Specifies whether the workspace supports fields of type Time Only."""
    @property
    def supportsTimestampOffset(self) -> bool:
        """Specifies whether the workspace supports fields of type Timestamp Offset."""
    @property
    def workspaceFactoryProgID(self) -> str:
        """The ID is a string that you can use to distinguish between workspace types with a finer granularity than you can with workspaceType."""
    @property
    def workspaceType(self) -> str:
        """
        Specifies the workspace type.
        FileSystem—The workspace type is a file-based workspace (shapefile, coverage, and so on) or an in-memory workspace.
        LocalDatabase—The workspace type is a local geodatabase (a file or personal geodatabase) or a memory workspace.
        RemoteDatabase—The workspace type is a geodatabase that requires a remote connection (enterprise, OLE DB, and so on).
        """

class _Dataset(_Base):
    @property
    def canVersion(self) -> bool:
        """Indicates whether the dataset can be versioned."""
    @property
    def changeTracked(self) -> bool:
        """Indicates whether the dataset is change tracked."""
    @property
    def datasetType(self) -> str:
        """Returns the type of dataset being described."""
    @property
    def DSID(self) -> int:
        """The ID of the dataset."""
    @property
    def extent(self) -> arcpy.Extent:
        """
        The Extent object.
        extent is available for spatial datasets only.
        """
    @property
    def isArchived(self) -> bool:
        """
        Indicates whether the dataset has been archived.
        isArchived is only supported for an enterprise geodatabase.
        """
    @property
    def isVersioned(self) -> bool:
        """Indicates whether the dataset is versioned."""
    @property
    def MExtent(self) -> str:
        """
        A space-delimited string (MMin, MMax).
        MExtent is available for spatial datasets only.
        """
    @property
    def spatialReference(self) -> arcpy.SpatialReference:
        """
        Returns the SpatialReference object for the dataset.
        spatialReference is available for spatial datasets only.
        """
    @property
    def workspace(self) -> Workspace:
        """
        Returns a Describe object with the properties of the input dataset's workspace.
        See Workspace properties for specific workspace-related Describe details.
        Use this property to determine workspace properties for many data types including: layers, and feature classes in a geodatabase that may or may not be in a feature dataset.
        """
    @property
    def ZExtent(self) -> str:
        """
        A space-delimited string (ZMin, ZMax).
        ZExtent is available for spatial datasets only.
        """

class _EditorTracking:
    @property
    def editorTrackingEnabled(self) -> bool:
        """True if editor tracking is enabled for the dataset."""
    @property
    def creatorFieldName(self) -> str:
        """The name of the field that contains the username of the person who created a feature, row, or raster."""
    @property
    def createdAtFieldName(self) -> str:
        """The name of the field that contains the date and time a feature, row, or raster was created."""
    @property
    def editorFieldName(self) -> str:
        """The name of the field that contains the username of the person who most recently edited a feature, row, or raster."""
    @property
    def editedAtFieldName(self) -> str:
        """The name of the field that contains the date and time a feature, row, or raster was most recently edited."""
    @property
    def isTimeInUTC(self) -> bool:
        """True if times stored in the CreatedAt field and EditedAt field are stored in  UTC (coordinated universal time). False if they are stored in database time."""

class _TableBase(_Dataset):
    @property
    def hasOID(self) -> bool:
        """Indicates whether the table has an Object ID field."""
    @property
    def hasOID64(self) -> bool:
        """
        Indicates whether the table's Object ID field is 64-bit integer.
        This property is only supported when the hasOID property returns True.
        Use the Python getattr function to avoid an AttributeError exception.
        """
    @property
    def OIDFieldName(self) -> str:
        """The name of the Object ID field if it exists."""
    @property
    def fields(self) -> list[arcpy.Field]:
        """A list of Field objects for the table. This property is equivalent to using the ListFields function."""
    @property
    def indexes(self) -> list[arcpy.Index]:
        """A list of Index objects for the table. This property is equivalent to using the ListIndexes function."""

class _FeatureClassBase(_TableBase):
    @property
    def dateAccessed(self) -> str:
        """The date in UTC that the feature class _was last accessed."""
    @property
    def dateCreated(self) -> str:
        """The date in UTC that the feature class _was created."""
    @property
    def dateModified(self) -> str:
        """The date in UTC that the feature class _was last modified."""
    @property
    def featureType(self) -> str:
        """The feature type of the feature class."""
    @property
    def hasM(self) -> bool:
        """Indicates whether the geometry is m-value enabled."""
    @property
    def hasZ(self) -> bool:
        """Indicates whether the geometry is z-value enabled."""
    @property
    def hasSpatialIndex(self) -> bool:
        """
        Indicates whether the feature class _has a spatial index.
        Compressed datasets do not have a spatial index on the shape column and will return False.
        """
    @property
    def shapeFieldName(self) -> str:
        """The name of the geometry field."""
    @property
    def shapeType(self) -> str:
        """The geometry shape type."""
    @property
    def size(self) -> int:
        """The size of the feature class _in bytes."""
    @property
    def splitModel(self) -> str:
        """The split model that is set for the feature class."""

class _Table(_TableBase, _EditorTracking): ...
class _FeatureClass(_FeatureClassBase, _EditorTracking): ...

class _Layer(_Dataset):
    @property
    def dataElement(self) -> Base:
        """The Describe object of the data source to which the layer refers."""
    @property
    def endTimeField(self) -> str:
        """The end time field of the layer (if the layer is time-aware)."""
    @property
    def featureClass(self) -> FeatureClass:
        """The Describe object of the feature class _associated with the feature layer."""
    @property
    def FIDSet(self) -> str:
        """
        arcpy.Describe will return a semicolon-delimited string of selected feature IDs (record numbers).
        arcpy.da.Describe will return a list of selected feature IDs. If a selection has not been applied to the layer, FIDSet will return a None; if a selection was applied to the layer, but it returned no records, FIDSet will return an empty list.
        """
    @property
    def fieldInfo(self) -> arcpy.FieldInfo:
        """The FieldInfo object (property set) of the layer."""
    @property
    def layer(self):
        """The Describe object of the layer within a .lyr file."""
    @property
    def nameString(self) -> str:
        """The name of the layer."""
    @property
    def startTimeField(self) -> str:
        """The start time field of the layer (if the layer is time-aware)."""
    @property
    def table(self) -> TableBase:
        """The Describe object of the table within a layer."""
    @property
    def TimeZone(self) -> str:
        """The time zone referred to by the start and end time fields (if time is specified for the layer)."""
    @property
    def whereClause(self) -> str:
        """The layer's definition query where clause."""

class _RasterBand(_TableBase):
    @property
    def height(self) -> int:
        """The number of rows."""
    @property
    def isInteger(self) -> bool:
        """Indicates whether the raster band has integer type."""
    @property
    def meanCellHeight(self) -> float:
        """The cell size in y direction."""
    @property
    def meanCellWidth(self) -> float:
        """The cell size in x direction."""
    @property
    def noDataValue(self) -> str:
        """The NoData value of the raster band."""
    @property
    def pixelType(self) -> str:
        """The pixel type."""
    @property
    def primaryField(self) -> int:
        """The index of the field."""
    @property
    def tableType(self) -> str:
        """
        The class _names of the table.
        Value—Values in the table are used for values only, not for indexing.
        Index—Values in the table are used as indexes in the raster table.
        Invalid—Values are invalid.
        """
    @property
    def width(self) -> int:
        """The number of columns."""

class _RasterDataset(_RasterBand):
    @property
    def bandCount(self) -> int:
        """The number of bands in the raster dataset."""
    @property
    def compressionType(self) -> str:
        """The compression type."""
    @property
    def format(self) -> str:
        """The raster format."""
    @property
    def permanent(self) -> bool:
        """Indicates the permanent state of the raster: False if the raster is temporary and True if the raster is permanent."""
    @property
    def sensorType(self) -> str:
        """The sensor type used to capture the image."""

class _ArcInfoItem(_Base):
    @property
    def alternateName(self) -> str:
        """The alternate name is another name you can use to refer to the item. It sometimes contains abbreviated names for items that otherwise have long descriptive names. Long item names often help for documentation purposes. Shorter names may be convenient for ad hoc usage."""
    @property
    def isIndexed(self) -> bool:
        """True if the item is indexed. Indexed items speed up selection operations on large INFO files."""
    @property
    def isPseudo(self) -> bool:
        """True if the item is a pseudo item."""
    @property
    def isRedefined(self) -> bool:
        """True if it is a redefined item. Redefined items can be subsets of regular items or can span multiple regular items."""
    @property
    def itemType(self) -> str:
        """The data type of the item. One of Binary, Character, Date, Floating, Integer, Number, and OID."""
    @property
    def numberDecimals(self) -> int:
        """The number of digits to the right of the decimal place. This is only for item types that hold decimal numbers."""
    @property
    def outputWidth(self) -> int:
        """The number of spaces used to display the item's values."""
    @property
    def startPosition(self) -> int:
        """The starting position of a redefined item."""
    @property
    def width(self) -> int:
        """The number of spaces (or bytes) used to store the item's values."""

class _ArcInfoTable(_TableBase):
    @property
    def itemSet(self) -> list[ArcInfoItem]:
        """A list of items in the table.

        Each entry in the list is an ArcInfo Workstation Item properties Describe object, representing one item in the table.
        """

class _BIMFileWorkspace(_Dataset):
    @property
    def activeWorldFilePath(self) -> str:
        """The path to a .wld3 file that will be used to adjust the spatial coordinates of features in the file."""
    @property
    def author(self) -> str:
        """The BIM file author's name."""
    @property
    def bimLevels(self) -> str:
        """The BIM level names that will be returned as a JSON array of JSON objects."""
    @property
    def buildingName(self) -> str:
        """The building name."""
    @property
    def client(self) -> str:
        """The user-provided name of the organization for which the file was created."""
    @property
    def designOptions(self) -> str:
        """A flat JSON array for design options that includes the design option name, whether the option is a primary option, and the name of the option set."""
    @property
    def displayUnitSystem(self) -> str:
        """Specifies the display units, either Imperial or Metric."""
    @property
    def externalSources(self) -> str:
        """A list of files referenced as a JSON array of a JSON object"""
    @property
    def isIFC(self) -> bool:
        """Specifies whether the BIM workspace is an .ifc file."""
    @property
    def isRevit(self) -> bool:
        """Specifies whether the BIM workspace is a Revit file."""
    @property
    def landTitle(self) -> str:
        """The land title."""
    @property
    def lengthDisplayUnit(self) -> str:
        """The length display unit."""
    @property
    def organizationName(self) -> str:
        """The organization name."""
    @property
    def organizationDescription(self) -> str:
        """The organization description."""
    @property
    def phases(self) -> str:
        """A list of construction phases that will be returned as a JSON array of JSON objects."""
    @property
    def projectAddress(self) -> str:
        """The location address of the project."""
    @property
    def projectName(self) -> str:
        """The name of the project."""
    @property
    def projectNumber(self) -> str:
        """The project number."""
    @property
    def projectStatus(self) -> str:
        """The project status."""
    @property
    def version(self) -> str:
        """The BIM file version."""
    @property
    def worksets(self) -> str:
        """A list of workset names that will be returned as a JSON array of JSON objects."""

class _CadDrawingDataset(_Dataset):
    @property
    def activeWorldFilePath(self) -> str:
        """Path to WLD3 file being used to adjust the spatial coordinates of features in the file."""
    @property
    def angleUnitType(self) -> str:
        """The units of angular measures reported in the file: Decimal Degrees, DMS, Grads, Radians, or Surveyor's Unit."""
    @property
    def author(self) -> str:
        """CAD user-entered file author's name."""
    @property
    def cadLayers(self) -> str:
        """A string list of CAD layers in the file."""
    @property
    def civilCSDescription(self) -> str:
        """The coordinate system description from Civil 3D in the file."""
    @property
    def civilCSName(self) -> str:
        """The coordinate system name from Civil 3D in the file."""
    @property
    def client(self) -> str:
        """CAD user-entered name of the client for whom the file was created."""
    @property
    def comments(self) -> str:
        """CAD user-entered comment within file."""
    @property
    def company(self) -> str:
        """CAD user-entered company name for the file."""
    @property
    def externalSources(self) -> str:
        """A list of files referenced within this file as a JSON array of a JSON object."""
    @property
    def is2D(self) -> bool:
        """Indicates whether a CAD dataset is 2D."""
    @property
    def is3D(self) -> bool:
        """Indicates whether a CAD dataset is 3D."""
    @property
    def isAutoCAD(self) -> bool:
        """Indicates whether a CAD dataset is an AutoCAD file."""
    @property
    def isCivil3D(self) -> bool:
        """Indicates whether a CAD dataset is an AutoCAD Civil 3D file."""
    @property
    def isDGN(self) -> bool:
        """Indicates whether a CAD dataset is a MicroStation file."""
    @property
    def keywords(self) -> str:
        """CAD user-entered keywords that can be used as search criteria for the file."""
    @property
    def lastSavedBy(self) -> str:
        """CAD user-entered name of the last person who last saved the file."""
    @property
    def lengthUnitType(self) -> str:
        """The units of linear measures used in the file: Decimal, Architectural, Engineering, Fractional, or Scientific."""
    @property
    def manager(self) -> str:
        """CAD user-entered name of the manager responsible for the file."""
    @property
    def subject(self) -> str:
        """CAD user-entered subject of the content of the file."""
    @property
    def title(self) -> str:
        """CAD user-entered document title of the file."""
    @property
    def version(self) -> str:
        """CAD authoring application file version."""

class _CadFeatureClass(_FeatureClassBase): ...

class _CoverageFeatureClass(_FeatureClassBase):
    @property
    def featureClassType(self) -> str:
        """The feature class _types."""
    @property
    def hasFAT(self) -> bool:
        """True if the coverage feature class _has a Feature Attribute Table (FAT) and False if it does not."""
    @property
    def topology(self) -> str:
        """
        Indicates the state of the coverage feature class _topology.
        NotApplicable—The topology is not supported by this feature class.
        Preliminary—Topology is preliminary.
        Exists—Topology exists.
        Unknown—Topology status is unknown.
        """

class _Coverage(_Dataset):
    @property
    def tolerances(self):
        """Tolerances is a property set"""

class _DbaseTable(_TableBase): ...
class _File(_Base): ...
class _Folder(_Workspace): ...

class _GALayer(_Layer):
    @property
    def areaOfInterest(self) -> arcpy.Extent:
        """The extent of the geostatistical layer."""
    @property
    def dataCollection(self) -> arcpy.ValueTable:
        """A value table of the datasets used to create the geostatistical layer. It is recommended that you instead use the GeostatisticalDatasets class _to determine the source dataset."""

class _LasDataset(_File, _Dataset):
    @property
    def constraintCount(self) -> int:
        """The number of surface constraint features referenced by the LAS dataset."""
    @property
    def fileCount(self) -> int:
        """The number of LAS files referenced by the LAS dataset."""
    @property
    def hasStatistics(self) -> bool:
        """Indicates whether statistics had been calculated for the LAS files referenced by the LAS dataset."""
    @property
    def needsUpdateStatistics(self) -> bool:
        """Indicates whether statistics are out of date or had not been calculated. Returns false if statistics are up to date."""
    @property
    def pointCount(self) -> int:
        """The number of data points in the LAS files referenced by the LAS dataset."""
    @property
    def usesRelativePath(self) -> bool:
        """Indicates whether the LAS dataset references its data elements using relative paths."""

class _MapDocument(_Base): ...

class _MosaicDataset(_RasterDataset, _EditorTracking):
    @property
    def allowedCompressionMethods(self) -> str:
        """The methods of compression that can be used to transmit the mosaicked image from the server to the client. This property influences an image service generated from the mosaic dataset."""
    @property
    def allowedFields(self) -> str:
        """The attribute table fields that are visible to the client when the mosaic dataset is served as an image service."""
    @property
    def allowedMensurationCapabilities(self) -> str:
        """The mensuration tools that can be used with an image service."""
    @property
    def allowedMosaicMethods(self) -> str:
        """Specifies the order of the rasters mosaicked together to render the mosaicked display."""
    @property
    def applyColorCorrection(self) -> bool:
        """If color correction information is available in the mosaic dataset, a value of True means it will be applied."""
    @property
    def blendWidth(self) -> float:
        """The distance used by the Blend mosaic operator."""
    @property
    def blendWidthUnits(self) -> str:
        """Specifies the blend width units."""
    @property
    def cellSizeToleranceFactor(self) -> float:
        """The way mosaic dataset items with different pixel sizes are grouped together for some operations, such as mosaicking or seamline generation."""
    @property
    def childrenNames(self) -> str:
        """A list of side-table names that are components of the mosaic dataset."""
    @property
    def clipToBoundary(self) -> bool:
        """True means the image extent is limited to the geometry of the boundary. False means it is limited to the extent of the boundary."""
    @property
    def clipToFootprint(self) -> bool:
        """Specifies whether the extent of each raster is limited to its footprint."""
    @property
    def ConnectionFiles(self) -> str:
        """The paths to Cloud Storage Connection (.acs) files, if any of the mosaic dataset items were added from an .acs file."""
    @property
    def defaultCompressionMethod(self) -> str:
        """The default compression method for the image. This value comes from the list of methods returned by the allowedCompressionMethods property."""
    @property
    def defaultMensurationCapability(self) -> str:
        """The default mensuration tool that will be used with an image service. This value comes from the list returned by the allowedMensurationCapabilities property."""
    @property
    def defaultMosaicMethod(self) -> str:
        """The default mosaic method for the mosaicked image. This value comes from the list returned by the allowedMosaicMethods property."""
    @property
    def defaultProcessingTemplate(self) -> str:
        """Returns the name of the current default processing template."""
    @property
    def defaultResamplingMethod(self) -> str:
        """Specifies the default sampling method of the pixels."""
    @property
    def dimensionAttributes(self) -> str:
        """
        Returns a list of variables, its dimension names, and the attributes of every dimension separated by a pipe (|).
        Dimension attributes include Description, Unit, Count, Minimum, Maximum, Interval, IntervalUnits, HasRegularIntervals, and HasRanges.
        The format of the returned string is <variable1>|<dimension2>|Description:<description>;Unit:<unit>;Count:<number of dimension values>;Minimum:<min dimension value>;Maximum:<max dimension value>;Interval:<interval>; IntervalUnit:<interval unit>;HasRegularIntervals:<boolean>; HasRanges:<boolean>, <variable1>|<dimension2>|Description:<description>; ... ..
        """
    @property
    def dimensionNames(self) -> str:
        """
        Returns a list of dimension names associated with every variable in a multidimensional mosaic dataset.
        The variable name and the dimension name are separated by a pipe (|), and each variable and dimension pair is separated by a comma.
        The format of the returned string is <variable_name1>|<dimension_name2>, <variable_name2>| dimension_name2>.
        """
    @property
    def dimensionValues(self) -> str:
        """
        Returns the values for each dimension associated with every variable:The variable name, dimension name, and dimension values are separated by a pipe (|).
        Each <variable>|dimension|dimensionValue tuple is separated by a comma.
        The minimum and maximum values of the dimensions are separated by a dash.
        The dimension values are separated by a semicolon.The format of the returned string is <variable1>|<dimension1>|<minDimValue>-<maxDimValue>;<minDimValue>-<maxDimValue>;<minDimValue>-<maxDimValue>;<minDimValue>-<maxDimValue>, <variable1>|<dimension2>|<minDimValue>-<maxDimValue>; ... ..
        """
    @property
    def endTimeField(self) -> str:
        """The field that defines the end time."""
    @property
    def footprintMayContainNoData(self) -> bool:
        """True if NoData is a valid pixel value."""
    @property
    def GCSTransforms(self) -> str:
        """The transformations applied if the spatial references of the source rasters differ from the spatial reference of the mosaic dataset."""
    @property
    def isMultidimensional(self) -> bool:
        """True if the mosaic dataset has associated multidimensional information."""
    @property
    def JPEGQuality(self) -> int:
        """The percentage of image quality retained if JPEG compression is used on this dataset."""
    @property
    def LERCTolerance(self) -> float:
        """The maximum error value applied per pixel if the mosaic dataset uses LERC compression."""
    @property
    def maxDownloadImageCount(self) -> int:
        """The maximum number of rasters that a client can download from an image service."""
    @property
    def maxDownloadSizeLimit(self) -> int:
        """The maximum size, in megabytes, of rasters that a client can download from an image service."""
    @property
    def maxRastersPerMosaic(self) -> int:
        """The maximum number of rasters mosaicked. This property affects an image service generated from the mosaic dataset."""
    @property
    def maxRecordsReturned(self) -> int:
        """The maximum number of records returned by the server when viewing the mosaic dataset as a published image service."""
    @property
    def maxRequestSizeX(self) -> int:
        """The maximum number of columns returned each time a mosaicked image is generated."""
    @property
    def maxRequestSizeY(self) -> int:
        """The maximum number of rows returned each time a mosaicked image is generated."""
    @property
    def minimumPixelContribution(self) -> int:
        """The minimum number of pixels needed within the area of interest for a mosaic dataset item to be considered as part of that area."""
    @property
    def mosaicOperator(self) -> str:
        """Specifies the default method for resolving overlapping cells."""
    @property
    def multidimensionalInfo(self) -> str:
        """Returns a JSON object representing the multidimensional information of a mosaic dataset."""
    @property
    def orderBaseValue(self) -> float:
        """
        The images are sorted based on the difference between this value and the value specified in the orderField property.
        This is applicable only for the By Attribute mosaic method.
        If the orderBaseValue is a time-related value, the time string is returned in the following format: YYYY/DD/MM HH:MM:SS.
        """
    @property
    def orderField(self) -> str:
        """The metadata attribute used for raster ordering. This is applicable only for the By Attribute mosaic method."""
    @property
    def processingTemplates(self) -> str:
        """Returns a list of processing template names associated with the mosaic dataset."""
    @property
    def rasterMetadataLevel(self) -> str:
        """
        Specifies the metadata that will be transmitted from the server to the client.
        """
    @property
    def referenced(self) -> bool:
        """True if it is a referenced mosaic dataset; False if it is a regular mosaic dataset."""
    @property
    def sortAscending(self) -> str:
        """Specifies the default ordering of the images defined by the mosaic methods."""
    @property
    def startTimeField(self) -> str:
        """The field that defines the start time."""
    @property
    def timeValueFormat(self) -> str:
        """The format in which the start time and end time values are specified."""
    @property
    def useTime(self) -> bool:
        """True if the mosaic dataset is time aware."""
    @property
    def variableAttributes(self) -> str:
        """
        Returns a list of variables and their attributes.
        The name of the variable and its attributes are separated by a pipe (|).
        Each variable and its attributes are separated by a comma.
        The attributes of a variable are Description and Unit.
        The format of the returned string is <variable_name1>|Unit:<units>;Description:<Description>, <variable_name2>|Unit:<units>;Description:<Description>.
        """
    @property
    def variableNames(self) -> str:
        """
        Returns a list of variable names associated with the multidimensional raster.
        The format of the returned string is <variable_name1>, <variable_name2>, ..., <variable_nameX>.
        """
    @property
    def viewpointSpacingX(self) -> float:
        """
        The horizontal offset used to calculate where the center of the area of interest (display view) is when you click an arrow button on the Viewpoint dialog box.
        These values are calculated in the units of the spatial reference system of the mosaic dataset.
        This is applicable only for the Closest to Viewpoint mosaic method.
        """
    @property
    def viewpointSpacingY(self) -> float:
        """
        The vertical offset used to calculate where the center of the area of interest (display view) is when you click an arrow button on the Viewpoint dialog box.
        These values are calculated in the units of the spatial reference system of the mosaic dataset.
        This is applicable only for the Closest to Viewpoint mosaic method.
        """

class _ProjectionFile:
    @property
    def spatialReference(self) -> arcpy.SpatialReference:
        """The SpatialReference class _instance of the projection file."""

class _RecordSet(TableBase):
    @property
    def json(self) -> str:
        """A JSON string representing the table or feature class _that underlies the arcpy.RecordSet or arcpy.FeatureSet."""
    @property
    def pjson(self) -> str:
        """
        Pretty JSON. A JSON string formatted to be easily readable.
        This string is a little larger because it includes extra newline and whitespace characters.
        """

class _FeatureSet(RecordSet, FeatureClassBase): ...
class _ShapeFile(FeatureClassBase): ...

class _TableView(TableBase):
    @property
    def table(self) -> TableBase:
        """A Describe object of the table associated with the table view."""
    @property
    def FIDSet(self) -> str:
        """
        arcpy.Describe will return a semicolon-delimited string of selected record IDs (record numbers).
        arcpy.da.Describe will return a list of selected record IDs.
        If there are no selected records, FIDSet will return a None; if there is no selection, FIDSet will return an empty list.
        """
    @property
    def fieldInfo(self) -> arcpy.FieldInfo:
        """The FieldInfo object (property set) of the table."""
    @property
    def whereClause(self) -> str:
        """The table view selection where clause."""
    @property
    def nameString(self) -> str:
        """The name of the table view."""

class _TextFile(File, TableBase): ...

class _TIN(Dataset):
    @property
    def fields(self) -> list[arcpy.Field]:
        """A list containing Field objects for the TIN dataset."""
    @property
    def hasEdgeTagValues(self) -> bool:
        """Indicates whether the TIN dataset has edge tag values."""
    @property
    def hasNodeTagValues(self) -> bool:
        """Indicates whether the TIN dataset has node tag values."""
    @property
    def hasTriangleTagValues(self) -> bool:
        """Indicates whether the TIN dataset has triangle tag values."""
    @property
    def isDelaunay(self) -> bool:
        """Indicates whether the TIN dataset was constructed using Delaunay triangulation."""
    @property
    def ZFactor(self) -> int:
        """Multiplication factor applied to all z-values in a TIN to provide unit congruency between coordinate components."""

class _Tool(Dataset): ...
class _Toolbox(Dataset): ...
class _VPFCoverage(Dataset): ...
class _VPFFeatureClass(FeatureClassBase): ...
class _VPFTable(TableBase): ...
