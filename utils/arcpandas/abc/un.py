from datetime import datetime

__all__ = [
    "UtilityNetwork",
]

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

class SystemJunctionObject:
    @property
    def sourceID(self) -> int:
        """The ID of the system junction object source."""

class SystemJunction:
    @property
    def name(self) -> str:
        """The name of the system junction source."""
    @property
    def sourceID(self) -> int:
        """The ID of the system junction source."""
    @property
    def sourceType(self) -> str:
        """The type of the system junction source."""

class AssetType:
    @property
    def assetTypeCode(self) -> int:
        """The asset type code."""
    @property
    def assetTypeName(self) -> str:
        """The asset type name."""
    @property
    def associationDeleteType(self) -> str:
        """The association deletion type for the asset type."""
    @property
    def associationRoleType(self) -> str:
        """The association role type for the asset type."""
    @property
    def categories(self) -> str:
        """The categories for the asset type."""
    @property
    def connectivityPolicy(self) -> str:
        """The connectivity policy for the asset type."""
    @property
    def containmentViewScale(self) -> int:
        """The value of the containment view scale for the asset type."""
    @property
    def creationTime(self) -> str:
        """The creation time of the asset type."""
    @property
    def isLinearConnectivityPolicySupported(self) -> bool:
        """Whether the asset type supports a linear connectivity policy.True—The asset type supports linear connectivity.False—The asset type does not support linear connectivity."""
    @property
    def isTerminalConfigurationSupported(self) -> bool:
        """Whether the asset type supports terminal configuration.True—The asset type supports terminal configuration.False—The asset type does not support terminal configuration."""
    @property
    def splitContent(self) -> bool:
        """Whether the asset type supports splitting content.True—The asset type supports splitting content.False—The asset type does not support splitting content."""
    @property
    def terminalConfigurationID(self) -> int:
        """The asset type's terminal configuration ID."""

class AssetGroup:
    @property
    def assetGroupCode(self) -> int:
        """The asset group code."""
    @property
    def assetGroupName(self) -> str:
        """The asset group name."""
    @property
    def assetTypes(self) -> list[AssetType]:
        """The assetTypes object. This object can be used to retrieve     properties of the asset types."""
    @property
    def creationTime(self) -> str:
        """The creation time of the asset group."""

class JunctionSource:
    @property
    def assetGroups(self) -> list[AssetGroup]:
        """The assetGroups object. This object can be used to retrieve properties of the junction source asset groups."""
    @property
    def assetTypeFieldName(self) -> str:
        """The asset type field name for the junction source."""
    @property
    def objectClassID(self) -> int:
        """The object class ID for the junction source."""
    @property
    def shapeType(self) -> str:
        """The shape type of the junction source."""
    @property
    def sourceID(self) -> int:
        """The source ID for the junction source."""
    @property
    def sourceName(self) -> str:
        """The name of the junction source."""
    @property
    def supportedProperties(self) -> str:
        """The supported properties of the junction source."""
    @property
    def usesGeometry(self) -> bool:
        """Whether the junction source uses geometry or not."""
    @property
    def utilityNetworkFeatureClassUsageType(self) -> str:
        """The feature class usage type for the junction source."""

class EdgeSource:
    @property
    def assetGroups(self) -> list[AssetGroup]:
        """The assetGroups object. This object can be used to retrieve properties of the edge source asset groups."""
    @property
    def assetTypeFieldName(self) -> str:
        """The asset type field name for the edge source."""
    @property
    def objectClassID(self) -> int:
        """The object class ID for the edge source."""
    @property
    def shapeType(self) -> str:
        """The shape type of the edge source."""
    @property
    def sourceID(self) -> int:
        """The source ID for the edge source."""
    @property
    def sourceName(self) -> str:
        """The name of the edge source."""
    @property
    def supportedProperties(self) -> str:
        """The name of the edge source."""
    @property
    def usesGeometry(self) -> bool:
        """Whether the edge source uses geometry or not."""
    @property
    def utilityNetworkFeatureClassUsageType(self) -> str:
        """The feature class usage type for the edge source."""

class TierGroup:
    @property
    def creationTime(self) -> str:
        """The creation time of the tier group."""
    @property
    def name(self) -> str:
        """The name of the tier group."""

class ValidAssetType:
    @property
    def assetTypeCode(self) -> int:
        """The asset type code"""

class AggregatedLine:
    @property
    def assetGroupCode(self) -> int:
        """The asset group code of the aggregated line for the SubnetLine class."""
    @property
    def assetTypes(self) -> list[ValidAssetType]:
        """The assetTypes object. This object can be used to retrieve the assetTypeCode of the aggregated line's asset types. The assetTypeCode is the integer value of the asset type code of the aggregated line for the SubnetLine class."""

class ValidDevice:
    @property
    def assetGroupCode(self) -> int:
        """The asset group code of the valid device."""
    @property
    def assetTypes(self) -> list[ValidAssetType]:
        """The assetTypes object. This object can be used to retrieve the assetTypeCode of the valid device's asset types. The assetTypeCode is the integer value of the asset type code of the valid device."""

class ValidEdgeObject:
    @property
    def assetGroupCode(self) -> int:
        """The asset group code of the valid edge object."""
    @property
    def assetTypes(self) -> list[ValidAssetType]:
        """The assetTypes object. This object can be used to retrieve the assetTypeCode of the valid edge object's asset types. The assetTypeCode is the integer value of the asset type code of the valid edge object."""

class ValidJunction:
    @property
    def assetGroupCode(self) -> int:
        """The asset group code of the valid junction."""
    @property
    def assetTypes(self) -> list[ValidAssetType]:
        """The assetTypes object. This object can be used to retrieve the assetTypeCode of the valid junction's asset types. The assetTypeCode is the integer value of the asset type code of the valid junction."""

class ValidJunctionObject:
    @property
    def assetGroupCode(self) -> int:
        """The asset group code of the valid junction object."""
    @property
    def assetTypes(self) -> list[ValidAssetType]:
        """The assetTypes object. This object can be used to retrieve the assetTypeCode of the valid junction object's asset types. The assetTypeCode is the integer value of the asset type code of the valid junction object."""

class ValidJunctionObjectSubnetworkController:
    @property
    def assetGroupCode(self) -> int:
        """The asset group code of the valid junction object subnetwork controller."""
    @property
    def assetTypes(self) -> list[ValidAssetType]:
        """The assetTypes object. This object can be used to retrieve the assetTypeCode of the valid junction object subnetwork controller's asset types. The assetTypeCode is the integer value of the asset type code of the valid junction object subnetwork controller."""

class ValidLine:
    @property
    def assetGroupCode(self) -> int:
        """The asset group code of the valid line."""
    @property
    def assetTypes(self) -> list[ValidAssetType]:
        """The assetTypes object. This object can be used to retrieve the assetTypeCode of the valid line's asset types. The assetTypeCode is the integer value of the asset type code of the valid line."""

class ValidSubnetworkController:
    @property
    def assetGroupCode(self) -> int:
        """The asset group code of the subnetwork controller."""
    @property
    def assetTypes(self) -> list[ValidAssetType]:
        """The assetTypes object. This object can be used to retrieve the assetTypeCode of the subnetwork controller's asset types. The assetTypeCode is the integer value of the asset type code of the valid subnetwork controller."""

class ManageSubnetwork:
    @property
    def isDirty(self) -> bool:
        """
        Describes whether the Is dirty attribute in the Subnetworks table and SubnetLine class is managed by the update subnetwork operation.
        This property requires a Utility Network Version value of 5 or later.
        """

class ConditionBarrier:
    @property
    def combineUsingOr(self) -> bool:
        """Whether the condition barrier is using an Or condition for the combine using parameter."""
    @property
    def isSpecificValue(self) -> bool:
        """Whether the condition barrier is using a specific value to terminate the trace."""
    @property
    def name(self) -> str:
        """The name of the network attribute or category used for the condition barrier—for example, Device status."""
    @property
    def operator(self) -> str:
        """The operator used for the condition barrier—for example, is equal to or is greater than or equal to."""
    @property
    def type(self) -> str:
        """The type of condition barrier used—for example, using a specific value or a network attribute."""
    @property
    def value(self) -> int:
        """The value of the network attribute or category used for the condition barrier."""

class FunctionBarrier:
    @property
    def functionType(self) -> str:
        """The type of function used for the function barrier—for example, the minimum, maximum, or count."""
    @property
    def networkAttributeName(self) -> str:
        """The name of the network attribute used for the function barrier condition."""
    @property
    def networkAttributeOperator(self) -> str:
        """The type of operator used for the function barrier—for example, is equal to or is less than."""
    @property
    def useLocalValues(self) -> bool:
        """Whether the function barrier is using the local values for the trace."""
    @property
    def value(self) -> int:
        """The specific value of the network attribute or category used for the function barrier."""

class FilterBarrier:
    @property
    def combineUsingOr(self) -> bool:
        """Whether the filter barrier is using an Or condition for the combine using parameter."""
    @property
    def isSpecificValue(self) -> bool:
        """Whether the filter barrier is using a specific value to terminate the trace."""
    @property
    def name(self) -> str:
        """The name of the network attribute or category used for the filter barrier—for example, Device status."""
    @property
    def operator(self) -> str:
        """The operator used for the filter barrier—for example, is equal to or is greater than or equal to."""
    @property
    def type(self) -> str:
        """The type of filter barrier used—for example, using a specific value or a network attribute."""
    @property
    def value(self) -> int:
        """The specific value of the network attribute or category used for the filter barrier."""

class FilterFunctionBarrier:
    @property
    def functionType(self) -> str:
        """The type of function used for the filter function barrier—for example, the minimum, maximum, or count."""
    @property
    def networkAttributeName(self) -> str:
        """The name of the network attribute used for the filter function barrier condition."""
    @property
    def networkAttributeOperator(self) -> str:
        """The type of operator used for the filter function barrier—for example, is equal to or is less than."""
    @property
    def useLocalValues(self) -> bool:
        """Whether the filter function barrier is using the local values for the trace."""
    @property
    def value(self) -> int:
        """The specific value of the network attribute or category used for the filter function barrier."""

class Condition:
    @property
    def combineUsingOr(self) -> bool:
        """Whether the condition is using an Or condition for the combine using parameter."""
    @property
    def isSpecificValue(self) -> bool:
        """Whether the condition is using a specific value to terminate the trace."""
    @property
    def name(self) -> str:
        """The name of the network attribute or category used for the condition—for example, Device status."""
    @property
    def operator(self) -> str:
        """The operator used for the condition—for example, is equal to or is greater than or equal to."""
    @property
    def type(self) -> str:
        """The type of condition used—for example, using a specific value or a network attribute."""
    @property
    def value(self) -> int:
        """The specific value of the network attribute or category used for the condition."""

class Function:
    @property
    def conditions(self) -> list[Condition]:
        """The conditions object. This object can be used to retrieve  properties of the conditions that are set for the functions parameter."""
    @property
    def functionType(self) -> str:
        """The type of function used for the function parameter—for example,

        the minimum, maximum, or count."""
    @property
    def networkAttributeName(self) -> str:
        """The name of the network attribute used for the function condition."""
    @property
    def summaryAttributeName(self) -> str:
        """The name of the network attribute used to filter the function results."""

class NearestAsset:
    @property
    def assetGroupCode(self) -> int:
        """The asset group code."""
    @property
    def assetTypeCode(self) -> int:
        """The asset type code."""
    @property
    def networkSourceID(self) -> int:
        """The ID of the network source."""

class NearestNeighbor:
    @property
    def costNetworkAttributeName(self) -> str:
        """If the filter nearest function is being used, this is the name of the network attribute that is being used to calculate the cost. If the filter nearest function is not being used, this property returns an empty string."""
    @property
    def count(self) -> int:
        """If the filter nearest function is being used, this is the value of the number of features to be returned. If the filter nearest function is not being used, this property returns a -1 value."""
    @property
    def nearestAssets(self) -> list[NearestAsset]:
        """The nearestAssets object. If the filter nearest function is being used, these are the asset groups and asset types that will be returned. If the filter nearest function is not being used, this property returns an empty list."""
    @property
    def nearestCategories(self) -> list[str]:
        """If the filter nearest function is being used, these are the names of the categories that will be returned. If the filter nearest function is not being used, this property returns an empty list."""

class OutputFilter:
    @property
    def assetGroupCode(self) -> int:
        """The asset group code."""
    @property
    def assetTypeCode(self) -> int:
        """The asset type code."""
    @property
    def networkSourceID(self) -> int:
        """The ID of the network source."""

class OutputCondition:
    @property
    def combineUsingOr(self) -> bool:
        """Whether the output condition is using an Or condition for the combine using parameter."""
    @property
    def isSpecificValue(self) -> bool:
        """Whether the output condition is using a specific value to terminate the trace."""
    @property
    def name(self) -> str:
        """The name of the network attribute or category used for the output condition—for example, Device status."""
    @property
    def operator(self) -> str:
        """The operator used for the output condition—for example, is equal to or is greater than or equal to."""
    @property
    def type(self) -> str:
        """The type of output condition used—for example, using a specific value or a network attribute."""
    @property
    def value(self) -> int:
        """The specific value of the network attribute or category used for the output condition."""

class Propagator:
    @property
    def networkAttributeName(self) -> str:
        """The name of the network attribute used to filter the propagators condition."""
    @property
    def networkAttributeOperator(self) -> str:
        """The type of operator used for the propagation—for example, is equal to or is less than."""
    @property
    def substitutionAttributeName(self) -> str:
        """The network attribute used for substitution."""
    @property
    def tracePropagatorFunctionType(self) -> str:
        """The type of function used for the function barrier—for example,  propagated bitwise and, propagated min, or propagated max."""
    @property
    def value(self) -> int:
        """The specific value of the network attribute or category used for the propagation."""

class TraceConfiguration:
    @property
    def conditionBarriers(self) -> list[ConditionBarrier]:
        """The conditionBarriers object. This object can be used to retrieve properties of the condition barriers set for the trace configuration."""
    @property
    def diagramTemplateName(self) -> str:
        """The name of the diagram template used for the trace configuration."""
    @property
    def domainNetworkName(self) -> str:
        """The name of the domain network."""
    @property
    def filterBarriers(self) -> list[FilterBarrier]:
        """The filterBarriers object. This object can be used to retrieve properties of the filter barriers set for the trace configuration."""
    @property
    def filterBitsetNetworkAttributeName(self) -> str:
        """The name of the network attribute that can be used to filter by bitset."""
    @property
    def filterFunctionBarriers(self) -> list[FilterFunctionBarrier]:
        """The filterFunctionBarriers object. This object can be used to retrieve properties of the filter function barriers set for the trace configuration."""
    @property
    def filterScope(self) -> str:
        """The traversability that is enforced for a specific category—for example, both junctions and edges, junctions only, or edges only."""
    @property
    def functionBarriers(self) -> list[FunctionBarrier]:
        """The functionBarriers object. This object can be used to retrieve properties of the function barriers set for the trace configuration."""
    @property
    def functions(self) -> list[Function]:
        """The functions object. This object can be used to retrieve properties of the functions set for the trace configuration."""
    @property
    def includeBarriers(self) -> bool:
        """Whether the trace is configured to include barrier features in the trace results."""
    @property
    def includeContainers(self) -> bool:
        """Whether the trace is configured to include container features in the trace results."""
    @property
    def includeContent(self) -> bool:
        """Whether the trace is configured to include content in containers in the trace results."""
    @property
    def includeStructures(self) -> bool:
        """Whether the trace is configured to include structure features in the trace results."""
    @property
    def nearestNeighbor(self) -> NearestNeighbor:
        """The nearestNeighbor object. This object can be used to retrieve properties of the nearest neighbor set for the trace configuration."""
    @property
    def outputConditions(self) -> list[OutputCondition]:
        """The outputConditions object. This object can be used to retrieve properties of the output conditions set for the trace configuration."""
    @property
    def outputFilters(self) -> list[OutputFilter]:
        """The outputFilters object. This object can be used to retrieve properties of the output filters set for the trace configuration."""
    @property
    def propagators(self) -> list[Propagator]:
        """The propagators object. This object can be used to retrieve properties of the propagators set for the trace configuration."""
    @property
    def shortestPathNetworkAttributeName(self) -> str:
        """The name of the network attribute used to calculate the shortest path."""
    @property
    def targetTierName(self) -> str:
        """The name of the target tier for which the starting tier flows toward."""
    @property
    def tierName(self) -> str:
        """The name of the tier to start the trace."""
    @property
    def traversabilityScope(self) -> str:
        """The traversability that is enforced—for example, both junctions and edges, junctions only, or edges only."""
    @property
    def validateConsistency(self) -> bool:
        """Whether the trace is configured to validate consistency in trace results."""

class Tier:
    @property
    def aggregatedLinesForSubnetLine(self) -> list[AggregatedLine]:
        """An aggregatedLinesForSubnetLine object that can be used to retrieve properties of the aggregated lines for the SubnetLine class."""
    @property
    def creationTime(self) -> str:
        """The time that the tier was created."""
    @property
    def diagramTemplates(self) -> str:
        """A list of diagram templates used for the tier."""
    @property
    def manageSubnetwork(self) -> ManageSubnetwork:
        """A manageSubnetwork object that can be used to retrieve properties of the state of the subnetwork."""
    @property
    def name(self) -> str:
        """The name of the tier."""
    @property
    def rank(self) -> int:
        """The value of the tier rank."""
    @property
    def subnetworkFieldName(self) -> str:
        """The subnetwork field name."""
    @property
    def supportDisjointSubnetwork(self) -> bool:
        """Returns whether the tier supports disjoint subnetworks."""
    @property
    def tierGroupName(self) -> str:
        """If the network has a hierarchical tier definition, this is the name of the tier group to which the tier belongs."""
    @property
    def tierID(self) -> int:
        """The ID of the tier."""
    @property
    def tierTopology(self) -> str:
        """The tier topology type—for example, radial or mesh tier topology."""
    @property
    def updateSubnetworkEditModeForDefaultVersion(self) -> str:
        """The edit mode for subnetwork updates on the default version."""
    @property
    def updateSubnetworkEditModeForNamedVersion(self) -> str:
        """The edit mode for subnetwork updates on a named version."""
    @property
    def updateSubnetworkOnContainers(self) -> bool:
        """Returns whether the update subnetwork process will update the supported subnetwork name for domain network containers."""
    @property
    def updateSubnetworkOnStructures(self) -> bool:
        """Returns whether the update subnetwork process will update the supported subnetwork name attribute for structure network containers."""
    @property
    def updateSubnetworkTraceConfiguration(self) -> TraceConfiguration:
        """An updateSubnetworkTraceConfiguration object that can be used to retrieve properties of the trace configuration when updating the subnetwork."""
    @property
    def validDevices(self) -> list[ValidDevice]:
        """A validDevices object that can be used to retrieve properties of the valid devices."""
    @property
    def validEdgeObjects(self) -> list[ValidEdgeObject]:
        """A validEdgeObjects object that can be used to retrieve properties of the valid edge objects."""
    @property
    def validJunctions(self) -> list[ValidJunction]:
        """A validJunctions object that can be used to retrieve properties of the valid junctions."""
    @property
    def validJunctionObjects(self) -> list[ValidJunctionObject]:
        """A validJunctionObjects object that can be used to retrieve properties of the valid junction objects."""
    @property
    def validJunctionObjectSubnetworkControllers(
        self,
    ) -> list[ValidJunctionObjectSubnetworkController]:
        """A validJunctionObjectSubnetworkControllers object that can be used to retrieve properties of the valid junction object subnetwork controllers."""
    @property
    def validLines(self) -> list[ValidLine]:
        """A validLines object that can be used to retrieve properties of the valid lines."""
    @property
    def validSubnetworkControllers(self) -> list[ValidSubnetworkController]:
        """A validSubnetworkControllers object that can be used to retrieve properties of the valid subnetwork controllers."""

class DomainNetwork:
    @property
    def creationTime(self) -> datetime:
        """The date and time that the domain network was created."""
    @property
    def domainNetworkAliasName(self) -> str:
        """If the domain network has an alias, this property will return the domain network alias name."""
    @property
    def domainNetworkID(self) -> int:
        """The ID of the network domain."""
    @property
    def domainNetworkName(self) -> str:
        """The name of the domain network."""
    @property
    def edgeSources(self) -> list[EdgeSource]:
        """The domain network edgeSources object. This object can be used to retrieve information about the edge sources in the domain network."""
    @property
    def isStructureNetwork(self) -> bool:
        """Whether the domain network is a structure network."""
    @property
    def junctionSources(self) -> list[JunctionSource]:
        """The domain network junctionSources object. This object can be used to retrieve information about the junction sources in the domain network."""
    @property
    def releaseNumber(self) -> int:
        """The release number of when the domain network was created."""
    @property
    def subnetworkControllerType(self) -> str:
        """The subnetwork controller type for the domain network—for example, source or sink."""
    @property
    def subnetworkLabelFieldName(self) -> str:
        """The name of the field used for subnetwork labels in the domain network."""
    @property
    def subnetworkTableName(self) -> str:
        """The name of the subnetwork table for the domain network."""
    @property
    def tierDefinition(self) -> str:
        """The tier definition for the domain network—for example, hierarchical or partitioned."""
    @property
    def tierGroups(self) -> list[TierGroup]:
        """The domain network tierGroups object. This object can be used to retrieve information about the tier groups of the domain network. This property is only available for hierarchical tier definitions."""
    @property
    def tiers(self) -> list[Tier]:
        """The domain network tiers object. This object can be used to retrieve information about the tiers in the domain network."""

class Evaluator:
    @property
    def evaluatorType(self) -> str:
        """The type of evaluator used for the assignment."""
    @property
    def fieldName(self) -> str:
        """The field name used for the evaluator."""

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
    def creationTime(self) -> datetime:
        """The creation date and time for the network attribute."""
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
        """A Boolean value describing whether the network attribute is apportionable."""
    @property
    def ID(self) -> int:
        """The ID of the network attribute."""
    @property
    def isEmbedded(self) -> bool:
        """A Boolean value describing whether the network attribute is embedded."""
    @property
    def isNullable(self) -> bool:
        """A Boolean value describing whether the network attribute is nullable (allows null values)."""
    @property
    def isOverridable(self) -> bool:
        """A Boolean value describing whether the network attribute can be overridden."""
    @property
    def isSubstitution(self) -> bool:
        """A Boolean value describing whether the network attribute is for substitution."""
    @property
    def junctionWeightID(self) -> int:
        """The junction weight ID value of the network attribute."""
    @property
    def name(self) -> str:
        """The name of the network attribute."""
    @property
    def networkAttributeToSubstitute(self) -> str:
        """The value used for attribute substitution."""
    @property
    def usageType(self) -> str:
        """The usage type of the network attribute—for example, terminal ID, source ID, and asset group."""

class Terminal:
    @property
    def isUpstreamTerminal(self) -> bool:
        """Whether the terminal is upstream.True—The terminal is upstream.False—The terminal is downstream."""
    @property
    def terminalID(self) -> int:
        """The terminal ID."""
    @property
    def terminalName(self) -> str:
        """The name of the terminal."""

class TerminalPath:
    @property
    def fromTerminalID(self) -> int:
        """The ID of the from terminal. The path starts from this terminal."""
    @property
    def toTerminalID(self) -> int:
        """The ID of the to terminal. The path goes to this terminal."""

class ValidConfigurationPath:
    @property
    def description(self) -> str:
        """The description of the valid configuration path."""
    @property
    def ID(self) -> int:
        """The ID of the valid configuration path."""
    @property
    def name(self) -> str:
        """The name of the valid configuration path."""
    @property
    def terminalPaths(self) -> list[TerminalPath]:
        """The terminalPaths object. This object can be used to retrieve properties of the terminal paths."""

class TerminalConfiguration:
    @property
    def creationTime(self) -> str:
        """The creation time of the terminal configuration."""
    @property
    def defaultConfiguration(self) -> str:
        """Of the valid terminal configurations available, this is the default path terminal configuration."""
    @property
    def terminalConfigurationID(self) -> int:
        """The ID of the terminal configuration."""
    @property
    def terminalConfigurationName(self) -> str:
        """The name of the terminal configuration."""
    @property
    def terminals(self) -> list[Terminal]:
        """The terminals object. This object can be used to retrieve properties of the terminals."""
    @property
    def traversabilityModel(self) -> str:
        """The traversability of the terminal configuration. The directionality can be either directional or bidirectional."""
    @property
    def validConfigurationPaths(self) -> list[ValidConfigurationPath]:
        """The validConfigurationPaths object. This object can be used to retrieve properties of the valid terminal configuration paths."""

class Category:
    @property
    def creationTime(self) -> str:
        """The creation time of the category."""
    @property
    def name(self) -> str:
        """The name of the category."""

class UtilityNetwork:
    @property
    def associationSource(self) -> AssociationSource:
        """The associationSource object. This object can be used to retrieve properties of the association sources."""
    @property
    def categories(self) -> list[Category]:
        """The categories object. This object can be used to retrieve properties of the utility network categories."""
    @property
    def createDirtyAreaForAnyAttributeUpdate(self) -> bool:
        """Whether dirty areas are created for any attribute update when the network topology is enabled."""
    @property
    def creationTime(self) -> datetime:
        """The creation date and time of the utility network."""
    @property
    def domainNetworks(self) -> list[DomainNetwork]:
        """The domainNetworks object. This object can be used to retrieve properties of the domain networks."""
    @property
    def globalID(self) -> str:
        """The Global ID of the utility network."""
    @property
    def minimalDirtyAreaSize(self) -> int:
        """The minimum size of the dirty areas in the network topology."""
    @property
    def networkAttributes(self) -> list[NetworkAttribute]:
        """The networkAttributes object. This object can be used to retrieve properties of the network attributes."""
    @property
    def proVersion(self) -> str:
        """The last ArcGIS Pro client that created or upgraded the utility network."""
    @property
    def schemaGeneration(self) -> int:
        """The Utility Network Version of the input utility network."""
    @property
    def serviceTerritoryFeatureClassName(self) -> str:
        """The name of the polygon feature class used to set the extent for the utility network."""
    @property
    def systemJunctionObjectSource(self) -> SystemJunctionObject:
        """The systemJunctionObjectSource object. This object can be used to retrieve properties of the system junction object sources."""
    @property
    def systemJunctionSource(self) -> SystemJunction:
        """The systemJunctionSource object. This object can be used to retrieve properties of the system junction sources."""
    @property
    def terminalConfigurations(self) -> list[TerminalConfiguration]:
        """The terminalConfigurations object. This object can be used to retrieve properties of the terminal configurations."""
