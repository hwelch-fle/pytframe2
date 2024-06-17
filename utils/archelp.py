import arcpy
import os
import shutil
import json


class Parameters(object):
    """ Parameters class to store the parameters of a tool """
    def __init__(self, parameters: list[arcpy.Parameter]) -> None:
        self._parameters = parameters
        for parameter in parameters:
            self.__dict__[parameter.name] = parameter
        return
    
    def __iter__(self):
        for _, value in self._parameters.items():
            yield value
        return
    
    def __getitem__(self, key):
        return self.__dict__[key]



def sanitize_filename(filename: str) -> str:
    """ Sanitize a filename """
    return "".join([char for char in filename if char.isalnum() or char in [" ", "_", "-"]])

def message(message: str, severity: str = "info") -> None:
    """ Print a message """
    match severity.lower():
        case "info":
            arcpy.AddMessage(message)
            print(f"info: {message}")
        case "warning":
            arcpy.AddWarning(message)
            print(f"warning: {message}")
        case "error":
            arcpy.AddError(message)
            print(f"error: {message}")
    return

class Network:
    def __init__(self, nodes: dict[str, arcpy.PointGeometry], edges: dict[str, arcpy.Polyline]) -> None:
        self.nodes = nodes
        self.edges = edges
        self.node_connections, self.edge_connections = self._build_network()
        return
    
    def _build_network(self):
        edge_connections: dict[str, tuple[str]] = {}
        node_connections: dict[str, list[str]] = {}
        for edge_id, edge in self.edges.items():
            node_left, node_right = None, None
            for node_id, node in self.nodes.items():
                if edge.disjoint(node): continue
                if edge.firstPoint == node: node_left = node_id
                elif edge.lastPoint == node: node_right = node_id
                if node_left and node_right: break
            edge_connections[edge_id] = (node_left, node_right)
            node_connections.setdefault(node_left, []).append(edge_id)
            node_connections.setdefault(node_right, []).append(edge_id)
        return node_connections, edge_connections

    def get_node(self, node_id: str) -> dict[str, str]:
        """ Gets a node dictionary where the keys are edge ids
        and the values are the connected node ids"""
        if node_id not in self.node_connections:
            raise ValueError(f"Node: {node_id} not in network!")
        connection_dict = {}
        for edge in self.node_connections[node_id]:
            node = [n for n in edge if n != node_id][0]
            connection_dict[edge] = node
        