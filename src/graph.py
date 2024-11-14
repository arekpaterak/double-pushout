from dataclasses import dataclass
from typing import Self
import networkx as nx


@dataclass
class Graph:
    _graph: nx.Graph

    @classmethod
    def parse(cls, text: str) -> Self:
        lines = text.strip().replace("\r", "").split('\n')
        
        G = nx.Graph()

        node_labels = list(lines[0].strip().replace(" ", ""))

        if any(label.isdigit() for label in node_labels):
            raise ValueError("Node labels should be letters")

        for id, label in enumerate(node_labels, 1):
            G.add_node(id, label=label)

        for line in lines[1:]:
            edge_definition = line.strip().split()
            if len(edge_definition) != 3:
                raise ValueError("Edge definition should match the format: node1 label node2")
            
            node1, label, node2 = edge_definition
            if not node1.isdigit() or not node2.isdigit():
                raise ValueError("Node identifiers should be integers")
            if not label.isalpha():
                raise ValueError("Edge label should be a letter")
            if node1 == "0" or node2 == "0":
                raise ValueError("Node identifiers should be greater than 0")

            G.add_edge(int(node1), int(node2), label=label)

        return cls(G)

    def to_nx(self) -> nx.Graph:
        return self._graph

    def to_text(self) -> str:
        lines = []

        node_labels = "".join(data["label"] for _, data in self._graph.nodes(data=True))
        lines.append(node_labels)

        for node1, node2, data in self._graph.edges(data=True):
            lines.append(f"{node1}{data['label']}{node2}")

        return "\n".join(lines)
