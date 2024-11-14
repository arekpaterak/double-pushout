from dataclasses import astuple, dataclass
from typing import Self
import networkx as nx

from graph import Graph


@dataclass
class Production:
    L: Graph
    K: Graph
    R: Graph

    def to_nx(self):
        return self.L._graph, self.K._graph, self.R._graph

    @classmethod
    def parse(cls, text: str) -> Self:
        sections = text.strip().replace("\r", "").split("\n\n")

        if len(sections) != 3:
            raise ValueError("Production should contain exactly 3 sections for L, K, and R")
        
        L = Graph.parse(sections[0])
        K = Graph.parse(sections[1])
        R = Graph.parse(sections[2])
        
        return cls(L, K, R)
