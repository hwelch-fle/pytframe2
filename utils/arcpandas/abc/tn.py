from datetime import datetime

from .base import Dataset

__all__ = [
    "TraceNetwork",
]

class Evaluator:
    @property
    def evaluatorType(self) -> str:
        """The type of evaluator used for the assignment."""
    @property
    def fieldName(self) -> str:
        """The field name for the evaluator."""

class Assignment:
    @property
    def evaluator(self) -> Evaluator:
        """The evaluator object. This object can be used to retrieve properties of the assignment evaluator."""
    @property
    def networkAttributeID(self) -> int:
        """The ID of the attribute assignment."""
    @property
    def networkSourceName(self) -> str:
        """The name of the attribute source."""

class NetworkAttribute:
    @property
    def assignments(self) -> list[Assignment]:
        """The assignments object. This object can be used to retrieve properties of the network attribute assignments."""
    @property
    def bitPosition(self) -> int:
        """The bit position value of the network attribute."""
    @property
    def bitSize(self) -> int:
        """The bit size value of the network attribute."""
    @property
    def dataType(self) -> str:
        """The data type of the network attribute—for example, integer or double."""
    @property
    def edgeWeightID(self) -> int:
        """The edge weight ID value of the network attribute."""
    @property
    def fieldType(self) -> str:
        """The data type of the network attribute field—for example, short or long integer, double, or date."""
    @property
    def isApportionable(self) -> bool:
        """A Boolean value describing whether or not the network attribute is apportionable."""
    @property
    def ID(self) -> int:
        """The ID of the network attribute."""
    @property
    def isEmbedded(self) -> bool:
        """A Boolean value describing whether or not the network attribute is embedded."""
    @property
    def junctionWeightID(self) -> int:
        """The junction weight ID value of the network attribute."""
    @property
    def name(self) -> str:
        """The name of the network attribute."""
    @property
    def usageType(self) -> str:
        """The usage type of the network attribute."""

class ConnectivityPolicy:
    @property
    def classConnectivity(self) -> str:
        """The class connectivity policy of the trace network source."""

class Source:
    @property
    def connectivityPolicies(self) -> ConnectivityPolicy:
        """The connectivityPolicies object. This object can be used to retrieve the connectivity policies for the source."""
    @property
    def elementType(self) -> str:
        """The type of element. Sources may be a Junction or an Edge."""
    @property
    def name(self) -> str:
        """The name of the source."""
    @property
    def sourceID(self) -> int:
        """The ID of the source."""
    @property
    def sourceType(self) -> str:
        """The type of source. Sources may be a JunctionFeature or an EdgeFeature."""

class SystemJunctionSource:
    @property
    def name(self) -> str:
        """The name of the system junction source."""
    @property
    def sourceID(self) -> int:
        """The ID of the system junction source."""
    @property
    def sourceType(self) -> str:
        """The type of the system junction source."""

class AssociationSource:
    @property
    def name(self) -> str:
        """The name of the association network source."""
    @property
    def sourceID(self) -> int:
        """The association network source ID."""
    @property
    def sourceType(self) -> str:
        """The type of association network source."""

class TraceNetwork(Dataset):
    @property
    def associationSource(self) -> AssociationSource:
        """The associationSource object. This object can be used to retrieve properties of the association sources."""
    @property
    def createDirtyAreaForAnyAttributeUpdate(self) -> bool:
        """Whether dirty areas are created for any attribute update when the network topology is enabled."""
    @property
    def creationTime(self) -> datetime:
        """The creation date and time of the trace network."""
    @property
    def globalID(self) -> str:
        """The Global ID of the trace network."""
    @property
    def minimalDirtyAreaSize(self) -> int:
        """The minimum size of the dirty areas in the network topology."""
    @property
    def networkAttributes(self) -> list[NetworkAttribute]:
        """The networkAttributes object. This object can be used to retrieve properties of the network attributes."""
    @property
    def proVersion(self) -> str:
        """The version of ArcGIS Pro used to build the trace network."""
    @property
    def schemaGeneration(self) -> int:
        """The schema generation value of the input trace network."""
    @property
    def sources(self) -> list[Source]:
        """The sources object. This object can be used to retrieve properties of the trace network sources."""
    @property
    def systemJunctionSource(self) -> SystemJunctionSource:
        """The systemJunctionSource object. This object can be used to retrieve properties of the system junction sources."""
