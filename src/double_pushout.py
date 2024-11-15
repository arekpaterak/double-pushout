from graph import Graph
from production import Production


def double_pushout(input_graph: Graph, production_rule: Production, mapping: dict) -> Graph:
    G = input_graph.to_nx()
    L, K, R = production_rule.to_unpacked_nx()

    # Check if the mapping is valid
    if len(set(mapping.values()) - L.nodes) != 0:
        raise ValueError(f"Not all nodes from L ({L.nodes}) are present in the mapping ({set(mapping.values())})")

    for node in mapping.keys():
        if node not in G.nodes:
            raise ValueError("A node in the mapping is not present in the input graph.")

    # Check if the node labels match between the input graph and L
    for G_node, L_node in mapping.items():
        if G.nodes[G_node]["label"] != L.nodes[L_node]["label"]:
            raise ValueError("Node labels do not match between the input graph and L.")

    inverse_mapping = {v: k for k, v in mapping.items()}
    
    # Remove edges that are in L, but not in K
    edges_to_remove = [
        (inverse_mapping[u], inverse_mapping[v]) for u, v in L.edges
        if not K.has_edge(u, v)
    ]
    G.remove_edges_from(edges_to_remove)
    
    # Remove nodes that are in L, but not in K
    nodes_to_remove = [
        inverse_mapping[n] for n in L.nodes
        if n not in K.nodes
    ]
    G.remove_nodes_from(nodes_to_remove)

    # Add nodes that are in R, but not in K
    max_node_id = max(G.nodes(), default=0)
    new_node_ids = {n: max_node_id + i for i, n in enumerate(R.nodes - K.nodes, 1)}
    new_inverse_mapping = {n: inverse_mapping[n] if n in K.nodes else new_node_ids[n] for n in R.nodes()}
    for n, d in R.nodes(data=True):
        if n not in K.nodes:
            G.add_node(new_inverse_mapping[n], **d)
    
    # Add edges that are in R, but not in K
    for u, v, d in R.edges(data=True):
        mapped_u, mapped_v = new_inverse_mapping[u], new_inverse_mapping[v]
        G.add_edge(mapped_u, mapped_v, **d)
    
    return Graph(G)
