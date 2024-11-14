import networkx as nx

from graph import Graph
from production import Production


def read_text_from_file(filepath: str) -> str:
    with open(filepath, 'r') as file:
        return file.read().strip()

def load_graph(path: str) -> nx.Graph:
    input_text = read_text_from_file(path)

    return Graph.parse(input_text)

def load_production(path: str) -> Production:
    input_text = read_text_from_file(path)

    return Production.parse(input_text)
    
def parse_mapping(mapping_text: str) -> dict:
    if not mapping_text:
        return {}

    lines = mapping_text.strip().split("\n")
    
    mapping = {}
    for line in lines:
        node1, node2 = line.strip().split(" ")
        mapping[int(node1)] = int(node2)
        
    return mapping

def get_default_mapping(graph: Graph) -> dict:
    return {node: node for node in graph.to_nx().nodes()}
