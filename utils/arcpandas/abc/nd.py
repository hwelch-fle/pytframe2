from .base import Base, Dataset, Layer

__all__ = [
    "NetworkDataset",
    "NALayer",
]

class NetworkSourceDirectionsFieldMapping:
    @property
    def againstField(self) -> str:
        """The name of the field in your data mapped to the property designated in the key property for transitions in the to-from direction (against the direction of digitization) of line features."""
    @property
    def alongField(self) -> str:
        """The name of the field in your data mapped to the property designated in the key property for transitions in the from-to direction (along the direction of digitization) of line features."""
    @property
    def key(self) -> str:
        """The name of the network dataset directions property to which your data's field is being mapped."""
    @property
    def undirectedField(self) -> str:
        """The name of the field in your data mapped to the property designated in the key property for transitions that apply to all directions of travel."""

class LandmarkSource:
    @property
    def featureClassName(self) -> str:
        """The name of the point feature class associated with this landmark source."""
    @property
    def labelFieldName(self) -> str:
        """The name of the text field in the landmark feature class that describes the landmark."""
    @property
    def levelFieldName(self) -> str:
        """The name of the field used to associate landmarks with a specific floor level of a building."""
    @property
    def searchTolerance(self) -> float:
        """The size of the search radius. In general, when a route passes by a landmark within the search radius, it is reported in the directions. The units for this field are specified under searchToleranceUnits."""
    @property
    def searchToleranceUnits(self) -> str:
        """The units of the searchTolerance value."""
    @property
    def useSpatialSearch(self) -> bool:
        """A Boolean indicating whether the landmarks are spatial (True) or nonspatial (False)."""

class StreetNameFields:
    @property
    def prefixDirectionFieldName(self) -> str:
        """The field name used for prefix direction."""
    @property
    def prefixTypeFieldName(self) -> str:
        """The field name used for prefix type."""
    @property
    def streetNameFieldName(self) -> str:
        """The field name used for street name."""
    @property
    def suffixDirectionFieldName(self) -> str:
        """The field name used for suffix direction."""
    @property
    def suffixTypeFieldName(self) -> str:
        """The field name used for suffix type."""
    @property
    def priority(self) -> int:
        """The priority for when these street name fields are used. The default value is 1."""
    @property
    def fullNameFieldName(self) -> str:
        """The field name used to store the full street name."""
    @property
    def highwayDirectionFieldName(self) -> str:
        """The field name used for highway direction."""
    @property
    def languageFieldName(self) -> str:
        """The field name used to store the language for the street name."""

class ShieldsDescription:
    @property
    def shieldTypeX(self) -> int:
        """The shield type for a particular shield (indicated by X)"""
    @property
    def shieldDescriptionX(self) -> int:
        """The shield description for a particular shield (indicated by X)"""

class Shields:
    @property
    def combinedFieldName(self) -> str:
        """The field name whose values contain the whole address description."""
    @property
    def description(self) -> ShieldsDescription:
        """The Shields Description object."""
    @property
    def descriptionCount(self) -> int:
        """The number of shields."""
    @property
    def numberFieldName(self) -> str:
        """The field name whose values contain the house number."""
    @property
    def typeFieldName(self) -> str:
        """The field name whose values contain the street type."""
    @property
    def useCombinedField(self) -> bool:
        """Indicates whether the shield information is contained in a single field (True) or in two fields (False)."""

class NetworkSourceDirections:
    @property
    def adminAreaFieldName(self) -> str:
        """
        The name of the field containing the administrative area information for generating driving directions.
        If the administrative area information is not defined for the network dataset, the adminAreaFieldName property will throw an exception.
        """
    @property
    def fieldMappings(self) -> list[NetworkSourceDirectionsFieldMapping]:
        """
        Returns a list of Network Source Directions Field Mapping objects for this source.
        If field mappings are not defined for this network source, the fieldMappings property will throw an exception.
        """
    @property
    def landmarkEventSources(self) -> list[LandmarkSource]:
        """
        Returns a list of Landmark Source objects for this source.
        If landmark event sources (confirmation landmarks) are not defined for this network source, the landmarkEventSources property will throw an exception.
        """
    @property
    def landmarkManeuverSources(self) -> list[LandmarkSource]:
        """
        Returns a list of Landmark Source objects for this source.
        If landmark maneuver sources (turn landmarks) are not defined for this network source, the landmarkManeuverSources property will throw an exception.
        """
    @property
    def streetNameFields(self) -> list[StreetNameFields]:
        """Returns a list of Street Name Field objects for this network source."""
    @property
    def shields(self) -> Shields:
        """
        Returns a Shields object.
        This object can be used to determine the shield properties used in driving directions.
        If the shields information is not defined for the network dataset, the shields property will throw an exception.
        """

class ConnectivityPolicy:
    @property
    def usesSubtypes(self) -> bool:
        """
        For edge sources and junction sources.
        A Boolean indicating whether the given edge source or junction source determines connectivity groups and policies by subtypes.
        """
    @property
    def classConnectivity(self) -> str:
        """
        For edge sources and junction sources.
        Indicates the policy determining how all edge elements in the given edge source or junction elements in the given junction source connect to each other.
        If the usesSubtypes property for a given edge source or junction source returns True, then this property should not be used to determine the connectivity policy.
        Instead, use the connPolicyX property for a particular subtype.
        """
    @property
    def subtypeConnCount(self) -> int:
        """
        For edge sources and junction sources.
        The total number of subtypes that are used to define connectivity policies for the given edge source or junction source.
        If the usesSubtypes property returns False, then this property returns 0.
        """
    @property
    def connSubtypeX(self) -> int:
        """
        For edge sources and junction sources.
        The subtype code used to define the subtype for the given edge feature source or junction feature source.
        connSubtypeX is a dynamic property that is supported only if the subTypeConnCount value is greater than 0.
        """
    @property
    def connPolicyX(self) -> str:
        """
        For edge sources and junction sources.
        Indicates the policy determining how all edge elements for a particular subtype in the given edge source connect to each other or how all junction elements for a particular subtype in the given junction source connect to each other.
        connPolicyX is a dynamic property that is supported only if the subTypeConnCount value is greater than 0.
        """
    @property
    def defaultGroup(self) -> int:
        """
        For edge sources only.
        The connectivity group in which this edge feature source participates.
        If the usesSubtypes property returns True, then this property returns -1. In such a case, use the groupNameX property for a particular subtype.
        """
    @property
    def groupCount(self) -> int:
        """
        For edge sources only.
        The total number of subtypes that are used to define connectivity groups for the given edge source.
        If the usesSubtypes property returns False, then this property returns 0.
        """
    @property
    def groupSubtypeX(self) -> int:
        """
        For edge sources only.
        The subtype code used to define the subtype for the given edge feature source.
        groupSubtypeX is a dynamic property that is supported only if the groupCount value is greater than 0.
        """
    @property
    def groupNameX(self) -> str:
        """
        For edge sources only.
        The connectivity group in which the particular subtype of the given edge feature source participates.
        groupNameX is a dynamic property that is supported only if the groupCount value is greater than 0.
        """
    @property
    def defaultGroupsCount(self) -> int:
        """
        For junction sources only.
        The total number of connectivity groups to which a given junction source belongs.
        If the usesSubtypes property returns True, then use the subtypeXGroupsCount property to determine the total number of connectivity groups to which a particular subtype of a given junction source belongs.
        If the usesSubtypes property returns True, then this property returns 0."""
    @property
    def defaultGroupNameX(self) -> str:
        """
        For junction sources only.
        The connectivity group in which this junction feature source participates.
        defaultGroupNameX is a dynamic property that is supported only if the defaultGroupsCount value is greater than 0.
        The possible range of values for X depends on the defaultGroupsCount property.
        """
    @property
    def subtypeGroupCount(self) -> int:
        """
        For junction sources only.
        The total number of subtypes that are used to define connectivity groups for the given junction source.
        If the usesSubtypes property returns False, then this property returns 0.
        """
    @property
    def subtypeGroupX(self) -> int:
        """
        For junction sources only.
        The subtype code used to define the subtype (indicated by X) for the given junction feature source.
        subtypeGroupX is a dynamic property that is supported only if the subtypeGroupCount value is greater than 0.
        """
    @property
    def subtypeXGroupsCount(self) -> int:
        """
        For junction sources only.
        The total number of connectivity groups to which a particular subtype (indicated by X) of a given junction source belongs.
        subtypeXGroupsCount is a dynamic property that is supported only if the subTypeGroupCount value is greater than 0.
        """
    @property
    def subtypeXGroupNameX(self) -> str:
        """
        For junction sources only
        The connectivity group in which the particular subtype of the given edge feature source participates.
        groupNameX is a dynamic property that is supported only if the groupCount value is greater than 0.
        """

class NetworkSource:
    @property
    def name(self) -> str:
        """The name of the feature class associated with this network source."""
    @property
    def sourceID(self) -> int:
        """The unique identifier of this network source within the network dataset."""
    @property
    def sourceType(self) -> str:
        """The type of network source."""
    @property
    def elementType(self) -> str:
        """Network element type of the network source."""

class EdgeSource(NetworkSource):
    @property
    def fromElevationFieldName(self) -> str:
        """The field name in the feature class associated with the given edge feature source that is used as the from elevation field when determining connectivity at coincident end vertices."""
    @property
    def toElevationFieldName(self) -> str:
        """The field name in the feature class associated with the given edge feature source that is used as the to elevation field when determining connectivity at coincident end vertices."""
    @property
    def connectivityPolicies(self) -> ConnectivityPolicy:
        """The network dataset edge Connectivity Policies object. This object can be used to determine connectivity information, such as connectivity policies and connectivity groups, used by the edge sources of the network dataset."""
    @property
    def sourceDirections(self) -> NetworkSourceDirections:
        """
        The Network Source Directions object.
        This object can be used to determine directions properties specific to a particular edge source.
        The sourceDirections property is available only if the network dataset supports directions which can be determined using the supportsDirections property.
        """

class JunctionSource(NetworkSource):
    @property
    def connectivityPolicies(self) -> ConnectivityPolicy:
        """The network dataset junction Connectivity Policies object. This object can be used to determine connectivity information, such as connectivity policies and connectivity groups, used by the junction sources of the network dataset."""
    @property
    def elevationFieldName(self) -> str:
        """The field name in the feature class associated with the given junction feature source that is used as the elevation field when determining connectivity at coincident vertices."""

class SystemJunctionSource(NetworkSource):
    @property
    def elevationFieldName(self) -> str:
        """The field name that is used as the elevation field when determining connectivity at coincident vertices."""

class TurnSource(NetworkSource): ...

class HistoricalTrafficData:
    @property
    def timeInterval(self) -> float:
        """The time interval of the traffic data."""
    @property
    def timeIntervalUnits(self) -> str:
        """The units of the time interval of the traffic data."""
    @property
    def firstTimeSliceFieldName(self) -> str:
        """The field name of the first time slice of the given period in the profile table."""
    @property
    def lastTimeSliceFieldName(self) -> str:
        """The field name of the last time slice of the given period in the profile table."""
    @property
    def firstTimeSliceStartTime(self) -> str:
        """The start time of valid period of day for traffic data."""
    @property
    def timeSliceDurationInMinutes(self) -> int:
        """The duration of time slice in minutes."""
    @property
    def profilesTableName(self) -> str:
        """The name of the table containing profiles."""
    @property
    def joinTableName(self) -> str:
        """The name of the join table between edges and profiles."""
    @property
    def joinTableBaseTravelTimeFieldName(self) -> str:
        """The field name for base travel time in the join table."""
    @property
    def joinTableBaseTravelTimeUnits(self) -> str:
        """The units for the base travel time in the join table."""
    @property
    def joinTableProfileIDFieldNames(self) -> list[str]:
        """A Python list containing field names of the join table pointing to speed profiles."""
    @property
    def joinTableBaseSpeedFieldName(self) -> str:
        """The field name for base speed in the join table."""
    @property
    def joinTableBaseSpeedUnits(self) -> str:
        """The units for the base speed in the join table."""
    @property
    def lengthAttributeName(self) -> str:
        """The name of the network cost attribute used to define the length along the elements of the network. This attribute is used to calculate the travel time for a given edge based on the speed if the historical traffic data is speed based. This property can be used to determine if a network dataset has been configured using a speed-based or time-based profile type. If the historical traffic data is time based, this property returns an empty string."""

class LiveTrafficData:
    @property
    def tmcTableName(self) -> str:
        """The name of the table that contains the relationship between streets and traffic messaging channel (TMC) codes."""
    @property
    def tmcFieldName(self) -> str:
        """The name of the field in the Streets—TMC join table that contains the TMC codes."""
    @property
    def trafficFeedLocation(self) -> str:
        """The source of the live traffic feed."""
    @property
    def trafficFeedType(self) -> str:
        """Specifies the type of live traffic feed."""

class NetworkDirectionsAttributeMappings:
    @property
    def attribute(self) -> str:
        """The name of the network attribute mapped to the directions property described by the key property."""
    @property
    def key(self) -> str:
        """The name of the network dataset directions property to which the network dataset's attribute is being mapped."""

class NetworkDirections:
    @property
    def attributeMappings(self) -> list[NetworkDirectionsAttributeMappings]:
        """
        Returns a list of Network Directions Attribute Mapping objects for this source.
        If attribute mappings are not defined for this network, the attributeMappings property will raise an exception.
        """
    @property
    def defaultOutputLengthUnits(self) -> str:
        """The default length units that will be used for reporting distances in driving directions."""
    @property
    def lengthAttributeName(self) -> str:
        """The name of the network attribute to be used for reporting travel distances."""
    @property
    def referenceLandmarkSourceNames(self) -> str:
        """A list of the names of the tables containing reference landmarks. Returns None if there are no reference landmark tables."""
    @property
    def roadClassAttributeName(self) -> str:
        """The name of the network attribute to be used for road classification."""
    @property
    def roadSplitsTableName(self) -> str:
        """The name of the table containing road splits."""
    @property
    def signpostFeatureClassName(self) -> str:
        """The name of the feature class containing signposts."""
    @property
    def signpostStreetsTableName(self) -> str:
        """The name of the indexed table containing signpost street references."""
    @property
    def timeAttributeName(self) -> str:
        """The name of the network attribute to be used for reporting travel time."""

class NetworkAttribute:
    @property
    def dataType(self) -> str:
        """The network attribute data type."""
    @property
    def dataX(self):
        """
        The value of the network attribute assigned to a network source using the evaluator.
        In the case of a script evaluator, the entire expression is returned.
        The data type of the returned value depends on the data type and the evaluator type associated with the network attribute.
        dataX is a dynamic property. This property is not supported with SDC-based network datasets.
        """
    @property
    def defaultEdgeData(self):
        """
        The value for the network attribute that is associated by default with all the edge network sources in the network dataset.
        In the case of a script evaluator, the entire expression is returned.
        The data type of the returned value depends on the data type and the default edge evaluator type associated with the network attribute.
        """
    @property
    def defaultEdgeEvaluatorType(self) -> str:
        """The default edge evaluator type used by the network dataset."""
    @property
    def defaultJunctionData(self):
        """
        The value for the network attribute that is associated by default with all the junction network sources in the network dataset.
        In case of a script evaluator, the entire expression is returned.
        The data type of the returned value depends on the data type and the default junction evaluator type associated with the network attribute.
        """
    @property
    def defaultJunctionEvaluatorType(self) -> str:
        """The default junction evaluator type used by the network dataset."""
    @property
    def defaultTurnData(self):
        """
        The value for the network attribute that is associated by default with all the turn network sources in the network dataset.
        In the case of a script evaluator, the entire expression is returned.
        The property is available only if the network dataset supports turns that can be determined using the supportsTurns property.
        The data type of the returned value depends on the data type and the default turn evaluator type associated with the network attribute.
        """
    @property
    def defaultTurnEvaluatorType(self) -> str:
        """The network dataset default turn evaluator type.
        The property is available only if the network dataset supports turns that can be determined using the supportsTurns property.
        """
    @property
    def directions(self) -> NetworkDirections:
        """
        A Network Directions Describe object that provides information about the network's directions configuration.
        If the network dataset does not support directions, this property will raise an exception.
        """
    @property
    def edgeDirectionX(self) -> str:
        """
        The direction for the edge network sources along which the evaluator assigns the value for the network attribute.
        There is no direction associated with junction and turn network sources.
        edgeDirectionX is a dynamic property.
        """
    @property
    def evaluatorCount(self) -> int:
        """The total number of evaluators used to derive values from the given network source for this network attribute."""
    @property
    def evaluatorTypeX(self) -> str:
        """The type of evaluator. evaluatorTypeX is a dynamic property."""
    @property
    def name(self) -> str:
        """The name of the network attribute."""
    @property
    def parameterCount(self) -> int:
        """The total number of attribute parameters defined for the network attribute."""
    @property
    def parameterDefaultValueX(self):
        """
        The default value for the parameter.
        parameterDefaultValueX is a dynamic property that is supported only if the parameterCount value is greater than 0.
        The data type of the returned value depends on the data type of the attribute parameter.
        """
    @property
    def parameterNameX(self) -> str:
        """
        The name of the parameter.
        parameterNameX is a dynamic property that is supported only if the parameterCount value is greater than 0.
        """
    @property
    def parameterTypeX(self) -> str:
        """
        The data type for the parameter.
        parameterTypeX is a dynamic property that is supported only if the parameterCount value is greater than 0.
        """
    @property
    def parameterUsageTypeX(self) -> str:
        """
        The usage type for the parameter.
        parameterUsageTypeX is a dynamic property that is supported only if the parameterCount value is greater than 0.
        """
    @property
    def sourceNameX(self) -> str:
        """
        The name of the network source for which the evaluator calculates the value of a given network attribute.
        sourceNameX is a dynamic property.
        """
    @property
    def trafficSupportType(self) -> str:
        """The type of traffic data currently configured for the network attribute."""
    @property
    def units(self) -> str:
        """
        The units for the network attribute.
        Units of a cost attribute are either distance or time units, for example, centimeters, meters, miles, minutes, or seconds.
        Descriptors, hierarchies, and restrictions have unknown units.
        """
    @property
    def usageType(self) -> str:
        """The network attribute usage type."""
    @property
    def useByDefault(self) -> bool:
        """
        Indicates if the network attribute is used by default on a newly created network analysis layer.
        Only one cost attribute in the network dataset can be set to be used by default.
        Descriptor attributes cannot be used by default.
        """

class NetworkDataset(Dataset):
    @property
    def attributes(self) -> list[NetworkAttribute]:
        """Returns a list of Network Attribute objects."""
    @property
    def defaultTravelModeName(self) -> str:
        """The name of the network dataset's default travel mode. Returns an empty string if the network dataset does not have a default travel mode."""
    @property
    def directions(self) -> NetworkDirections:
        """
        Returns a Network Directions object defined for the network dataset.
        This object can be used to get directions information at the network dataset level.
        The directions property is available only if the supportsDirections property returns True.
        """
    @property
    def edgeSources(self) -> list[EdgeSource]:
        """Returns a list of Edge Source objects."""
    @property
    def elevationModel(self) -> str:
        """The network elevation model used to refine the connectivity of the network dataset."""
    @property
    def historicalTrafficData(self) -> HistoricalTrafficData:
        """
        Returns the Historical Traffic Data object defined for the network dataset.
        This object can be used to get historical traffic information such as the historical traffic tables used by the network dataset.
        This property is available only if the supportsHistoricalTrafficData property returns True.
        """
    @property
    def isBuildable(self) -> bool:
        """Indicates whether the network dataset can be built. SDC-based network datasets cannot be built, as they are read-only."""
    @property
    def junctionSources(self) -> list[JunctionSource]:
        """Returns a list of Junction Source objects."""
    @property
    def liveTrafficData(self) -> LiveTrafficData:
        """
        Returns a Live Traffic Data object defined for the network dataset.
        This object can be used to get information about live traffic properties, such as traffic feed name used by the network dataset.
        This property is available only if the supportsLiveTrafficData property returns True.
        """
    @property
    def networkType(self) -> str:
        """The type of workspace containing the network dataset."""
    @property
    def optimizations(self) -> list[str]:
        """
        Returns a list of strings indicating which optimizations, if any, the network dataset uses.
        If the network dataset has a service area index to increase the speed at which service area polygons are calculated, the value Service Area Index is returned in the list of optimizations.
        If the network dataset is dissolved, the value Dissolve is returned in the list of optimizations.
        If no optimizations are present, an empty list is returned.
        """
    @property
    def sources(
        self,
    ) -> EdgeSource | JunctionSource | SystemJunctionSource | TurnSource:
        """
        Returns a list of Network Source objects.
        This property returns all the sources for the network dataset.
        If you want to get a list of a particular source type—for example, only the edge sources—use the edgeSources property.
        """
    @property
    def supportsDirections(self) -> bool:
        """Indicates whether the network dataset supports generating directions."""
    @property
    def supportsHistoricalTrafficData(self) -> bool:
        """Indicates whether the network dataset supports the use of historical traffic information."""
    @property
    def supportsLiveTrafficData(self) -> bool:
        """Indicates whether the network dataset supports the use of live traffic information."""
    @property
    def supportsTurns(self) -> bool:
        """Indicates whether the network dataset supports turns."""
    @property
    def systemJunctionSource(self) -> SystemJunctionSource:
        """
        Returns a System Junction Source object defined for the network dataset.
        This property is not available with SDC-based network datasets, as they do not support system junction sources.
        """
    @property
    def timeZoneAttributeName(self) -> str:
        """The name of the time zone attribute. If the network dataset does not support time zones, this property returns an empty string."""
    @property
    def timeZoneTableName(self) -> str:
        """The name of the time-zone table that stores the list of time zones used by the network dataset."""
    @property
    def trafficSupportType(self) -> str:
        """The type of traffic data currently configured for this network dataset."""
    @property
    def turnSources(self) -> list[TurnSource]:
        """Returns a list of Turn Source objects."""

class NetworkAnalystSolver:
    @property
    def timeOfDay(self) -> str:
        """
        Indicates the time to depart from or arrive at the facilities.
        The interpretation of this value depends on whether travel is toward or away from the facilities.
        It represents the departure time if the travelDirection property is set to TRAVEL_FROM and represents the arrival time if the travelDirection property is set to TRAVEL_TO.
        """
    @property
    def timeZoneUsage(self) -> str:
        """Indicates whether the route start time should be interpreted as the local time of the first stop in the route or as Coordinated Universal Time (UTC)."""

class RouteSolver(NetworkAnalystSolver):
    @property
    def findBestSequence(self) -> str:
        """Indicates if the solver will automatically re-order the stops to minimize the impedance or visit the stops in the given order."""
    @property
    def orderingType(self) -> str:
        """The ordering of stops when findBestSequence property has a value FIND_BEST_ORDER."""
    @property
    def routesShape(self) -> str:
        """The shape type for the route features that are output by the solver."""
    @property
    def startTime(self) -> str:
        """The start date and time for the route."""
    @property
    def timeZoneUsageForTimeFields(self) -> str:
        """Indicates whether datetime fields in the input data, such as time window fields, should be interpreted as the local time of the stop in the route or as Coordinated Universal Time (UTC)."""
    @property
    def useTimeWindows(self) -> str:
        """Indicates if time windows will be used at the stops."""

class ServiceAreaSolver(NetworkAnalystSolver):
    @property
    def defaultBreaks(self) -> str:
        """A space-separated string of impedance values indicating the extent of the service area to be calculated."""
    @property
    def exclusionSources(self) -> str:
        """A semicolon-separated list of network sources to be excluded when generating the polygons."""
    @property
    def includeNetworkSourceFields(self) -> str:
        """Indicates if additional fields are added to the service area lines to hold information about the underlying source features traversed during the analysis."""
    @property
    def mergeSimilarRanges(self) -> str:
        """Indicates how to merge polygons that share similar break values when generating polygons for multiple facilities."""
    @property
    def serviceAreaLines(self) -> str:
        """The type of lines to be generated based on the service area analysis."""
    @property
    def serviceAreaLinesType(self) -> str:
        """Indicates if overlapping lines are generated when computing the service area lines."""
    @property
    def serviceAreaPolygons(self) -> str:
        """The type of polygons to be generated."""
    @property
    def serviceAreaPolygonType(self) -> str:
        """Indicates how to create concentric service area polygons when using multiple break values."""
    @property
    def splitLinesAtBreaks(self) -> str:
        """Indicates if the service area lines will be split at the boundaries of the breaks."""
    @property
    def travelDirection(self) -> str:
        """The direction of travel to or from the facilities."""
    @property
    def trimDistance(self) -> str:
        """A space-separated string indicating the distance and units within which the polygons are trimmed."""
    @property
    def trimPolygons(self) -> str:
        """Indicates if the resulting polygons will be trimmed to be within a specified distance."""

class ClosestFacilitySolver(NetworkAnalystSolver):
    @property
    def cfRoutesShape(self) -> str:
        """The shape type for the route features that are output by the solver."""
    @property
    def defaultCutoff(self) -> float:
        """
        The default impedance value at which to stop searching for facilities for a given incident.
        If no cutoff value is specified in the network analysis layer, the property returns an empty string.
        """
    @property
    def defaultTargetFacilityCount(self) -> int:
        """The default number of closest facilities to find per incident."""
    @property
    def timeOfDayUsage(self) -> str:
        """Indicates whether the value of the timeOfDay property represents the arrival or departure times for the routes. This property returns the following keywords:START_TIMEEND_TIMENOT_USED"""
    @property
    def travelDirection(self) -> str:
        """The direction of travel between facilities and incidents."""

class OriginDestinationCostMatrixSolver(NetworkAnalystSolver):
    @property
    def defaultCutoff(self) -> float:
        """Indicates the default impedance value at which to cut off searching for destinations for a given origin.
        If no cutoff value is specified in the network analysis layer, the property returns an empty string.
        """
    @property
    def defaultTargetDestinationCount(self) -> int:
        """
        The default number of destinations to find for each origin.
        If the network analysis layer specifies that all destinations are to be found, this property returns an empty string.
        """
    @property
    def odLinesShape(self) -> str:
        """The type of line generated by the solver."""

class LocationAllocationSolver(NetworkAnalystSolver):
    @property
    def defaultCapacity(self) -> float:
        """The default capacity of facilities when the problemType property is set to MAXIMIZE_CAPACITATED_COVERAGE."""
    @property
    def defaultCutoff(self) -> float:
        """
        The maximum impedance at which a demand point can be allocated to a facility.
        If no cutoff value is specified in the network analysis layer, the property returns an empty string.
        """
    @property
    def defaultTargetFacilityCount(self) -> int:
        """The number of facilities that the solver should locate."""
    @property
    def impedanceParameter(self) -> float:
        """The parameter value to the equations specified in the impedance transformation."""
    @property
    def impedanceTransformation(self) -> str:
        """Indicates the equation used by the solver for transforming the network cost between facilities and demand points."""
    @property
    def laLinesShape(self) -> str:
        """The type of line generated by the solver."""
    @property
    def problemType(self) -> str:
        """The location-allocation problem type that will be solved."""
    @property
    def targetMarketShare(self) -> float:
        """The target market share in percentage to solve when the problemType property is set to TARGET_MARKET_SHARE."""
    @property
    def travelDirection(self) -> str:
        """The direction of travel between facilities and demand points when calculating the network costs."""

class VehicleRoutingProblemSolver(NetworkAnalystSolver):
    @property
    def defaultDate(self) -> str:
        """The implied date for time field values that don't have a date specified with the time."""
    @property
    def distanceFieldUnits(self) -> str:
        """The distance units used by distance fields of the network analysis layer's sublayers and tables (network analysis classes)."""
    @property
    def excessTransitTimePenaltyFactor(self) -> str:
        """Indicates how the solver rates the importance of reducing excess transit time."""
    @property
    def excessTransitTimePenaltyFactorValue(self) -> float:
        """The value used as the penalty factor for excess transit time in the objective function."""
    @property
    def timeFieldUnits(self) -> str:
        """The time units used by the temporal fields of the network analysis layer's sublayers and tables (network analysis classes)."""
    @property
    def timeWindowViolationPenaltyFactor(self) -> str:
        """Indicates how the solver rates the importance of honoring time windows without causing violations."""
    @property
    def timeWindowViolationPenaltyFactorValue(self) -> float:
        """The value used as the penalty factor for time window violation in the objective function."""
    @property
    def timeZoneUsageForTimeFields(self) -> str:
        """Indicates whether datetime fields in the input data, such as time window fields, should be interpreted as the local time of the order or as coordinated universal time (UTC)."""
    @property
    def vrpRoutesShape(self) -> str:
        """The shape type for the route features that are output by the solver."""
    @property
    def spatialClustering(self) -> bool:
        """Specifies whether to use spatial clustering."""

class NetworkAttributeParameter:
    @property
    def attributeNameX(self) -> str:
        """The name of a network attribute for which the parameter is defined."""
    @property
    def parameterNameX(self) -> str:
        """The name of the parameter."""
    @property
    def parameterValueX(self):
        """
        The value for the parameter as specified in the network analysis layer.
        This parameter value is used during the solve operation.
        The data type of the parameter value matches the data type of the attribute parameter as defined in the network dataset.
        For restriction usage parameters, the value returned will be a numerical value corresponding to the standard restriction usage options.
        """

class NetworkAnalystLocator:
    @property
    def sourceX(self) -> str:
        """The name of a particular class used by the locator."""
    @property
    def snapTypeX(self) -> str:
        """An underscore-separated string containing the snap types used for a given class in the locator."""
    @property
    def searchQueryX(self) -> str:
        """A query to restrict the search to a subset of the features within a given class in the locator."""

class NALayer(Base):
    @property
    def network(self) -> NetworkDataset:
        """The Network Dataset object. This object can be used to get all the properties, such as catalogPath, of the underlying network dataset used by the analysis layer."""
    @property
    def nameString(self) -> str:
        """The name of the Network Analyst layer."""
    @property
    def solverName(self) -> str:
        """The Network Analyst solver being referenced by the layer. Each layer can reference only one solver."""
    @property
    def impedance(self) -> str:
        """The network cost attribute used as the impedance during the analysis."""
    @property
    def accumulators(self) -> str:
        """A semicolon-separated list of network cost attributes that are accumulated as part of the analysis."""
    @property
    def restrictions(self) -> str:
        """A semicolon-separated list of restriction attributes that are applied for the analysis."""
    @property
    def ignoreInvalidLocations(self) -> bool:
        """
        A Boolean expression indicating the way in which the solver considers invalid network locations within the Network Analyst classes.
        A value of True indicates that the invalid locations are ignored by the solver.
        A value of False indicates that the invalid locations are not ignored by the solver.
        """
    @property
    def uTurns(self) -> str:
        """Indicates how the U-turns at junctions, which could occur during network traversal between stops, are being handled by the solver."""
    @property
    def useHierarchy(self) -> str:
        """Indicates whether the Network Analyst Layer is using Hierarchy."""
    @property
    def hierarchyAttribute(self) -> str:
        """The name of the hierarchy attribute."""
    @property
    def hierarchyLevelCount(self) -> int:
        """The number of hierarchy ranges used to define the hierarchy attribute. The maximum value is 3."""
    @property
    def maxValueForHierarchyX(self) -> int:
        """
        A given hierarchy attribute can have values that define the hierarchy ranges.
        The maximum values for each range can be obtained from the maxValueForHierarchyX property, where X indicates the hierarchy level.
        For example, the maximum value for the first hierarchy range (used to define the primary roads) can be obtained from the maxValueForHierarchy1 property.
        Use the hierarchyLevelCount property to determine the possible number of maxValueForHierarchy properties for a given hierarchy attribute.
        For example, if the hierarchyLevelCount property returns 3, the Describe object will support the MaxValueForHierarchy1 and MaxValueForHierarchy2 properties.
        """
    @property
    def locatorCount(self) -> int:
        """The total number of classes that are used to search through for determining a network location."""
    @property
    def locators(self) -> list[NetworkAnalystLocator]:
        """The Network Analyst Locator object. This object can be used to obtain name, snap type, and the search query information for the classes that are used for finding network locations."""
    @property
    def findClosest(self) -> str:
        """Indicates how the network source features are searched when locating network analysis objects."""
    @property
    def searchTolerance(self) -> str:
        """A space-separated string indicating the search tolerance and the units used when finding the network locations."""
    @property
    def excludeRestrictedElements(self) -> str:
        """Indicates whether the network analysis objects can be located only on traversable portions of network sources."""
    @property
    def solverProperties(
        self,
    ) -> (
        RouteSolver
        | ServiceAreaSolver
        | ClosestFacilitySolver
        | OriginDestinationCostMatrixSolver
        | LocationAllocationSolver
        | VehicleRoutingProblemSolver
    ):
        """The Network Analyst Solver object. This object can be used to determine the solver-specific properties in a Network Analyst layer."""
    @property
    def children(self) -> list[Layer]:
        """Returns a list of Describe objects that reference individual network analysis classes (such as stops and routes) as layers.
        This property cannot be used with the network analysis layer stored on disk as a layer file.
        """
    @property
    def parameterCount(self) -> int:
        """The total number of attribute parameters defined for all the network attributes of the underlying network dataset used by the Network Analyst layer."""
    @property
    def parameters(self) -> NetworkAttributeParameter:
        """The Network Attribute Parameter object. This object can be used to determine the attribute parameters used for the network analysis."""
