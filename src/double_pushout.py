from graph import Graph
from production import Production

def double_pushout(input_graph: Graph, production_rule: Production, mapping: dict) -> Graph:
    G = input_graph._graph
    L, K, R = production_rule.L._graph, production_rule.K._graph, production_rule.R._graph
    
    # 1. Sprawdzenie, czy podgraf określony przez mapping zawiera w sobie L
    for u, v, d in L.edges(data=True):
        mapped_u, mapped_v = mapping.get(u), mapping.get(v)
        if mapped_u is None or mapped_v is None or not G.has_edge(mapped_u, mapped_v) or G[mapped_u][mapped_v] != d:
            raise ValueError("Podgraf zdefiniowany przez użytkownika nie zawiera struktury L.")

    # 2. Usunięcie krawędzi, które są w L, ale nie są w K
    K_nodes = set(K.nodes())
    
    # Zidentyfikuj krawędzie L - K, aby je usunąć
    to_remove_edges = [
        (mapping[u], mapping[v]) for u, v in L.edges() 
        if (u in mapping and v in mapping) and not K.has_edge(u, v)
    ]
    # Usuwamy krawędzie L - K
    G.remove_edges_from(to_remove_edges)
    
    # 3. Usunięcie wierzchołków, które są w L, ale nie są w K
    to_remove_nodes = [
        mapping[n] for n in L.nodes() 
        if n in mapping and n not in K_nodes
    ]
    G.remove_nodes_from(to_remove_nodes)

    # 4. Dodanie wierzchołków, które są w R, ale nie są w K
    max_node_id = max(G.nodes(), default=0)
    new_node_ids = {n: max_node_id + i + 1 for i, n in enumerate(R.nodes() - K_nodes)}
    new_mapping = {n: mapping[n] if n in K_nodes else new_node_ids[n] for n in R.nodes()}

    # Dodajemy nowe wierzchołki z R
    for n, d in R.nodes(data=True):
        if n in K_nodes:
            G.nodes[mapping[n]].update(d)  # Aktualizujemy istniejący węzeł, jeśli jest w K
        else:
            G.add_node(new_mapping[n], **d)
    
    # 5. Dodanie krawędzi, które są w R, ale nie są w K
    for u, v, d in R.edges(data=True):
        mapped_u, mapped_v = new_mapping[u], new_mapping[v]
        G.add_edge(mapped_u, mapped_v, **d)

    # 6. Zachowanie pozostałych krawędzi z G, które nie zostały usunięte
    original_edges = input_graph._graph.edges(data=True)
    for u, v, d in original_edges:
        # Dodajemy krawędź, jeśli nadal istnieje w G i nie została nadpisana
        if not G.has_edge(u, v):
            G.add_edge(u, v, **d)
    
    return Graph(G)
