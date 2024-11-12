from dataclasses import dataclass
from typing import Self
import networkx as nx

from graph import Graph


@dataclass
class Production:
    L: nx.Graph
    K: nx.Graph
    R: nx.Graph

    @classmethod
    def parse(cls, text: str) -> Self:
        sections = text.split("\n\n")

        if len(sections) != 3:
            raise ValueError("Production should contain exactly 3 sections for L, K, and R")
        
        L = Graph.parse(sections[0])
        K = Graph.parse(sections[1])
        R = Graph.parse(sections[2])
        
        return cls(L, K, R)
