from typing import Optional
import gradio as gr
from matplotlib import pyplot as plt
import networkx as nx

from double_pushout import double_pushout
from utils import *
from graph import Graph
from production import Production


def default_pos(G: nx.Graph):
    pass

def visualise_graph_with_fixed_pos(graph: Graph, pos: Optional[dict] = None):
    plt.figure(figsize=(10, 10))

    G = graph._graph
    
    if not pos:
        pos = nx.spring_layout(G)

    labels = {node: f"{node} ({data['label']})" for node, data in G.nodes(data=True)}
    
    nx.draw(G, pos, labels=labels, with_labels=True, font_weight='bold', font_size=24, node_color='skyblue', node_size=500)
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    return plt.gcf()

def process_input_graph(input_graph_text):
    input_graph = Graph.parse(input_graph_text)
    input_graph_image = visualise_graph_with_fixed_pos(input_graph)

    return input_graph_image

def process_production_rule(production_rule_text):
    production_rule = Production.parse(production_rule_text)
    L_image = visualise_graph_with_fixed_pos(production_rule.L)
    K_image = visualise_graph_with_fixed_pos(production_rule.K)
    R_image = visualise_graph_with_fixed_pos(production_rule.R)

    return L_image, K_image, R_image

def apply_production_rule(input_graph_text, production_rule_text, mapping_text):
    
    input_graph = Graph.parse(input_graph_text)
    production_rule = Production.parse(production_rule_text)
    mapping = parse_mapping(mapping_text)

    global output_graph
    output_graph = double_pushout(input_graph, production_rule, mapping)
    output_graph_image = visualise_graph_with_fixed_pos(output_graph)

    return output_graph_image

def use_as_input():
    global output_graph
    if output_graph:
        return output_graph.to_text()
    else:
        return ""


if __name__ == "__main__":
    output_graph = None

    with gr.Blocks() as demo:
        gr.Markdown("# Single Pushout")

        with gr.Row(equal_height=True):
            input_graph_field = gr.Textbox(label="Input Graph", interactive=True, lines=5)
            input_graph_display = gr.Plot(label="Input Graph")

        with gr.Row():
            production_rule_field = gr.Textbox(label="Production Rule", interactive=True, lines = 15)
            mapping_field = gr.Textbox(label="Indexes Mapping", interactive=True, lines = 5)
            
        with gr.Row(equal_height=True):
            L_graph_display = gr.Plot(label="L")
            K_graph_display = gr.Plot(label="K")
            R_graph_display = gr.Plot(label="R")

        with gr.Row():
            apply_button = gr.Button("Apply")

        with gr.Row():
            output_graph_display = gr.Plot(label="Output Graph", scale=3)
            use_as_input_button = gr.Button("Use as Input", scale=1)

        input_graph_field.change(process_input_graph, [input_graph_field], [input_graph_display])
        production_rule_field.change(process_production_rule, [production_rule_field], [L_graph_display, K_graph_display, R_graph_display])

        apply_button.click(apply_production_rule, [input_graph_field, production_rule_field, mapping_field], [output_graph_display])

        use_as_input_button.click(use_as_input, [], [input_graph_field])

    demo.launch()
