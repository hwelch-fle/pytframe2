from datetime import datetime
from .base import Table, Dataset, Base, FeatureClassBase

__all__ = [
    "RepresentationClass",
    "GDBTable",
    "GDBFeatureClass",
    "LocationReferencingDataset",
    "GeometricNetwork",
    "Topology",
    "ParcelFabric",
    "CadastralFabric",
    "RasterCatalog",
    "RelationshipClass",
    "SchematicDataset",
    "SchematicDiagram",
    "SchematicFolder",
    "SDCFeatureClass",
]

class AttributeRule:
    @property
    def batch(self) -> bool:
        """
        Indicates whether the rule is run in batch mode.
        True—The rule is run in batch mode.
        False—The rule is not run in batch mode.
        Calculation rules may return either true or false, but constraint rules will always return false, and validation rules will always be true.
        """
    @property
    def checkParameters(self):
        """A system-generated JSON value that defines the configuration of a Data Reviewer-based rule."""
    @property
    def creationTime(self) -> datetime:
        """The date and time the attribute rule was created."""
    @property
    def description(self) -> str:
        """The description of the attribute rule."""
    @property
    def errorMessage(self) -> str:
        """If the attribute rule has a custom error message (that is, constraint rules), this property will return the error message that was assigned for this rule."""
    @property
    def errorNumber(self) -> int:
        """If the attribute rule has a custom error number (that is, constraint rules), this property will return the error number that was assigned for this rule."""
    @property
    def evaluationOrder(self) -> int:
        """If the rule type is calculation, this value gives the order in which the rule is run. The evaluation order is based on the order in which the rule was added to the dataset. For example, if Rule A is added before Rule B, the evaluation number will be lower for Rule A."""
    @property
    def excludeFromClientEvaluation(self) -> bool:
        """
        Returns a Boolean describing whether the rule is excluded from client evaluation.
        True—The rule is excluded from client evaluation (server only).
        False—The rule is run for all clients.
        """
    @property
    def fieldName(self) -> str:
        """If the attribute rule is assigned to a field (that is, a calculation rule type), this property returns the field name."""
    @property
    def id(self) -> int:
        """Returns the rule ID as an integer value."""
    @property
    def isEnabled(self) -> bool:
        """
        Returns a Boolean describing whether the rule is enabled.
        True—The rule is enabled and will be honored.
        False—The rule is disabled and will not be honored.
        """
    @property
    def name(self) -> str:
        """The name of the attribute rule."""
    @property
    def referencesExternalService(self) -> bool:
        """Indicates whether the rule references any external service."""
    @property
    def requiredGeodatabaseClientVersion(self) -> str:
        """The required geodatabase client version is set per rule, depending on which Arcade functions are used in the script expression. For example, if the script includes the Sequence operation, a 10.6.1 geodatabase is required."""
    @property
    def scriptExpression(self) -> str:
        """
        The Arcade expression that defines the rule.
        This property is not available for Data Reviewer rules.
        """
    @property
    def severity(self) -> int:
        """Defines the severity of the error. This property is applicable to validation rule types."""
    @property
    def subtypeCode(self) -> int:
        """If the attribute rule is assigned to a subtype, this property returns the subtype code to which it is assigned."""
    @property
    def tags(self) -> str:
        """A set of tags that are used to identify the rule."""
    @property
    def triggeringEvents(self) -> str:
        """The triggering events defined in the attribute rule. For example, the rule may be triggered by Insert, Update, or Delete events during editing."""
    @property
    def type(self) -> str:
        """
        The type of the attribute rule.
        esriARTCalculation—Calculation attribute rule
        esriARTConstraint—Constraint attribute rule
        esriARTValidation—Validation attribute rule
        """
    @property
    def userEditable(self) -> bool:
        """
        Returns a Boolean describing whether the rule allows editing of the attribute field that is being modified by the rule.
        True—Editors can edit the attribute values.
        False—Editors cannot edit the attribute values.
        """

class FieldGroup:
    @property
    def fieldNames(self) -> list[str]:
        """A list of the field names that participate in the field group."""
    @property
    def isEditingRestrictive(self) -> bool:
        """
        Indicates whether the field group has a restrictive editing experience.
        True—The field group is restrictive.
        False—The field group is not restrictive.
        """
    @property
    def name(self) -> str:
        """The name of the field group."""

class RepresentationClass(Dataset):
    @property
    def overrideFieldName(self) -> str:
        """The name of the Override field."""
    @property
    def requireShapeOverride(self) -> bool:
        """Indicates whether a shape override is required for feature representations."""
    @property
    def ruleIDFieldName(self) -> str:
        """The name of the RuleID field."""

class GDBTable(Table):
    @property
    def aliasName(self) -> str:
        """The alias name for the table."""
    @property
    def defaultSubtypeCode(self) -> int:
        """The default subtype code."""
    @property
    def extensionProperties(self):
        """The properties for the class extension."""
    @property
    def globalIDFieldName(self) -> str:
        """The name of the GlobalID field."""
    @property
    def hasGlobalID(self) -> bool:
        """Indicates whether the table has a GlobalID field."""
    @property
    def modelName(self) -> str:
        """The model name for the table."""
    @property
    def rasterFieldName(self) -> str:
        """The name of the raster field."""
    @property
    def relationshipClassNames(self) -> list[str]:
        """The names of the relationship classes that this table participates in."""
    @property
    def subtypeFieldName(self) -> str:
        """The name of the subtype field."""
    @property
    def versionedView(self) -> str:
        """The name of a versioned view for a versioned feature class."""

class GDBFeatureClass(GDBTable, FeatureClassBase):
    @property
    def areaFieldName(self) -> str:
        """The name of the geometry area field."""
    @property
    def geometryStorage(self) -> str:
        """
        Returns the geometry field storage.
        Binary—Esri Binary storage
        LOB—Esri LOB storage
        WKB—OGC Well Known Binary storage
        ST—Spatial Type storage
        SDO—Oracle Spatial Type storage
        PostGIS—PostgreSQL / PostGIS storage
        MSSQLGeometry—SQLServer / GEOMETRY storage
        MSSQLGeography—SQLServer / GEOGRAPHY storage
        Returns the storage type for enterprise geodatabase feature classes only; for all other feature classes, returns an empty string.
        """
    @property
    def isCompressed(self) -> bool:
        """Returns True if the feature class is compressed."""
    @property
    def lengthFieldName(self) -> str:
        """The name of the geometry length field."""
    @property
    def representations(self) -> list[RepresentationClass]:
        """A list of Describe objects for the representations associated with the feature class."""

class LocationReferencingDataset(Base):
    @property
    def lrsMetadata(self) -> str:
        """The metadata XML for the specified LRS."""
    @property
    def eventBehaviorRules(self) -> str:
        """The event behavior rules as defined for all the events in the metadata (that is, for each event in each LRS Network in the LRS)."""

class GeometricNetwork(Dataset):
    @property
    def featureClassNames(self) -> list[str]:
        """A list of the feature classes participating in the geometric network."""
    @property
    def networkType(self) -> str:
        """The type of associate logical network."""
    @property
    def orphanJunctionFeatureClassName(self) -> str:
        """The name of the feature class that contains the Orphan Junction features."""

class Topology(Dataset):
    @property
    def clusterTolerance(self) -> float:
        """The cluster tolerance of the topology."""
    @property
    def featureClassNames(self) -> list[str]:
        """A Python list containing the names of the feature classes participating in the topology."""
    @property
    def maximumGeneratedErrorCount(self) -> float:
        """The maximum number of errors to generate when validating a topology."""
    @property
    def ZClusterTolerance(self) -> float:
        """The z cluster tolerance of the topology."""

class ParcelFabric(Dataset):
    @property
    def connectionsFeatureClass(self) -> GDBFeatureClass:
        """The Describe object of the Connections feature class that is associated with the parcel fabric."""
    @property
    def parcelTypeNames(self) -> list[str]:
        """Returns a list of parcel type names associated with the parcel fabric."""
    @property
    def parcelTypes(self) -> tuple[tuple[str, str, str, bool], ...]:
        """
        Returns a list of parcel type objects that are associated with the parcel fabric.
        Each parcel type object is a list with four elements:
            The name of the parcel type
            The name of the parcel type polygon feature class
            The name of the parcel type line feature class
            True if the parcel type is a large, administrative parcel
        """
    @property
    def pointsFeatureClass(self) -> GDBFeatureClass:
        """The Describe object of the Points feature class that is associated with the parcel fabric."""
    @property
    def recordsFeatureClass(self) -> GDBFeatureClass:
        """The Describe object of the Records feature class that is associated with the parcel fabric."""
    @property
    def topology(self) -> Topology:
        """The Describe object of the topology that is associated with the parcel fabric."""
    @property
    def topologyEnabled(self) -> bool:
        """Returns whether the parcel topology is enabled."""
    @property
    def AdjustmentPointsFeatureClass(self) -> GDBFeatureClass:
        """The Describe object of the AdjustmentPoints feature class that is associated with the parcel fabric."""
    @property
    def AdjustmentLinesFeatureClass(self) -> GDBFeatureClass:
        """The Describe object of the AdjustmentLines feature class that is associated with the parcel fabric."""
    @property
    def AdjustmentVectorsFeatureClass(self) -> GDBFeatureClass:
        """The Describe object of the AdjustmentVectors feature class that is associated with the parcel fabric."""
    @property
    def version(self) -> int:
        """Returns the parcel fabric version."""

class CadastralFabric(Dataset):
    @property
    def bufferDistanceForAdjustment(self) -> float:
        """The distance used to generate a buffer around the job parcels. This buffer defines the adjustment area."""
    @property
    def compiledAccuracyCategory(self) -> int:
        """The default accuracy category for compiled parcels in this parcel fabric. Category values range from 1 to 7, inclusively."""
    @property
    def defaultAccuracyCategory(self) -> int:
        """The default accuracy category for the whole parcel fabric. Category values range from 1 to 7, inclusively."""
    @property
    def maximumShiftThreshold(self) -> float:
        """Coordinate changes will be written if the shift is greater than this tolerance value."""
    @property
    def multiGenerationEditing(self) -> bool:
        """True if parcel fabrics greater than one level below default can be edited."""
    @property
    def multiLevelReconcile(self) -> bool:
        """True if reconciling and posting with an ancestor more than one generation above the working version is allowed."""
    @property
    def pinAdjustmentBoundary(self) -> bool:
        """True if points on the adjustment area boundary should be pinned."""
    @property
    def pinAdjustmentPointsWithinBoundary(self) -> bool:
        """True if nonadjusted points within the adjustment area should be pinned."""
    @property
    def surrogateVersion(self) -> str:
        """
        The name of the surrogate version if applicable. Indicates whether the parcel fabric is a surrogate version.
        If set, the parcel fabrics can be edited in the surrogate version and its immediate children.
        If not set, fabric editing can only be performed in the default version and its immediate children.
        The surrogate default version functionality is only available to versions later than version 1.
        """
    @property
    def type(self) -> int:
        """The parcel fabric type."""
    @property
    def writeAdjustmentVectors(self) -> bool:
        """True if adjustment vectors should be written."""

class RasterCatalog(GDBFeatureClass):
    @property
    def rasterFieldName(self) -> str:
        """The name of the raster column in the raster catalog."""

class RelationshipRule:
    @property
    def destinationClassID(self) -> int:
        """The object class ID of the destination class."""
    @property
    def destinationMaximumCardinality(self) -> int:
        """The maximum cardinality of the destination class."""
    @property
    def destinationMinimumCardinality(self) -> int:
        """The minimum cardinality of the destination class."""
    @property
    def destinationSubtypeCode(self) -> int:
        """The subtype code of the destination class."""
    @property
    def originClassID(self) -> int:
        """The object class ID of the origin class."""
    @property
    def originMaximumCardinality(self) -> int:
        """The maximum cardinality of the origin class."""
    @property
    def originMinimumCardinality(self) -> int:
        """The minimum cardinality of the origin class."""
    @property
    def originSubtypeCode(self) -> int:
        """The subtype code of the origin class."""
    @property
    def ruleID(self) -> int:
        """The relationship rule ID."""

class RelationshipClass(GDBTable):
    @property
    def backwardPathLabel(self) -> str:
        """The backward path label for the relationship class."""
    @property
    def cardinality(self) -> str:
        """The cardinality for the relationship class."""
    @property
    def classKey(self) -> str:
        """Class key used for the relationship class."""
    @property
    def destinationClassKeys(self) -> tuple[tuple[str, str, str], ...]:
        """A list of tuples, with the object key name, and key role (DestinationPrimary, DestinationForeign)."""
    @property
    def destinationClassNames(self) -> str:
        """A list containing the names of the destination classes."""
    @property
    def forwardPathLabel(self) -> str:
        """The forward path label for the relationship class."""
    @property
    def isAttachmentRelationship(self) -> bool:
        """Indicates whether the relationship class represents a table attachment."""
    @property
    def isAttributed(self) -> bool:
        """Indicates whether the relationships in this relationship class have attributes."""
    @property
    def isComposite(self) -> bool:
        """Indicates whether the relationship class represents a composite relationship in which the origin object class represents the composite object."""
    @property
    def isReflexive(self) -> bool:
        """Indicates whether the origin and destination sets intersect."""
    @property
    def keyType(self) -> str:
        """Key type for the relationship class."""
    @property
    def notification(self) -> str:
        """The notification direction for the relationship class."""
    @property
    def originClassNames(self) -> str:
        """A list containing the names of the origin classes."""
    @property
    def originClassKeys(self) -> tuple[tuple[str, str, str], ...]:
        """A list of tuples, with the object key name, and key role (OriginPrimary, OriginForeign)."""
    @property
    def relationshipRules(self) -> list[RelationshipRule]:
        """A list of relationship rule objects that list the properties of the relationship rules that apply to this relationship class."""
    @property
    def splitPolicy(self) -> str:
        """The split policy that is set for the relationship class."""

class SchematicDataset(Dataset): ...

class SchematicDiagram(Dataset):
    @property
    def diagramClassName(self) -> str:
        """The name of the schematic diagram class associated with the diagram."""

class SchematicFolder(Dataset): ...
class SDCFeatureClass(GDBFeatureClass): ...
