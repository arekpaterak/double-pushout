from graph import Graph
from production import Production


def double_pushout(input_graph: Graph, production_rule: Production, mapping: dict) -> Graph:
    G = input_graph._graph
    L, K, R = production_rule.L._graph, production_rule.K._graph, production_rule.R._graph
    inverse_mapping = {v: k for k, v in mapping.items()}
    
    # Step 1: Identify the match and remove the L-K portion
    subgraph_nodes = set(mapping.values())
    subgraph_edges = [
        (u, v) for u, v, d in G.edges(data=True)
        if u in subgraph_nodes and v in subgraph_nodes
    ]
    
    # Check if the match satisfies the L graph structure
    for u, v, d in L.edges(data=True):
        mapped_u, mapped_v = mapping[u], mapping[v]
        if not G.has_edge(mapped_u, mapped_v) or G[mapped_u][mapped_v] != d:
            raise ValueError("Mapping does not satisfy the L graph structure")

    # Remove edges and nodes in G that correspond to L - K
    K_nodes = set(K.nodes())
    mapped_K_nodes = set(mapping[n] for n in K_nodes)
    to_remove_nodes = [n for n in subgraph_nodes if n in mapping.values() and n not in mapped_K_nodes]
    to_remove_edges = [
        (u, v) for u, v in subgraph_edges
        if (u not in mapped_K_nodes or v not in mapped_K_nodes) or not K.has_edge(inverse_mapping[u], inverse_mapping[v])
    ]

    G.remove_edges_from(to_remove_edges)
    G.remove_nodes_from(to_remove_nodes)

    # Step 2: Add the R-K portion
    # Remap R nodes to new identifiers, ensuring no conflicts
    max_node_id = max(G.nodes(), default=0)
    new_node_ids = {n: max_node_id + i + 1 for i, n in enumerate(R.nodes() - K_nodes)}
    new_mapping = {**mapping, **new_node_ids}

    inverse_mapping = {v: k for k, v in mapping.items()}

    # Add nodes and edges from R to G
    for n, d in R.nodes(data=True):

        if n in K_nodes:
            G.nodes[mapping[n]]['label'] = d['label']  # Update label if necessary
        else:
            G.add_node(new_mapping[n], **d)
    
    for u, v, d in R.edges(data=True):
        mapped_u, mapped_v = new_mapping[u], new_mapping[v]
        G.add_edge(mapped_u, mapped_v, **d)

    return Graph(G)
