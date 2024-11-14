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

def create_empty_plot():
    """Creates an empty matplotlib figure with basic formatting."""
    plt.figure(figsize=(10, 10))

    G = nx.Graph()

    return plt.gcf()

def visualise_graph_with_fixed_pos(graph: Graph, pos: Optional[dict] = None):
    plt.figure(figsize=(10, 10))

    G = graph.to_nx()
    
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
    if mapping == {}:
        mapping = get_default_mapping(input_graph)

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

def load_file(file):
    if file is None:
        return None
    content = file.decode('utf-8')
    return content

css = """
.monospace {
    font-family: monospace;
"""

if __name__ == "__main__":
    output_graph = None

    with gr.Blocks(css=css) as demo:
        gr.Markdown("# Double Pushout")

        with gr.Row(equal_height=True):
            with gr.Column():
                input_file_upload = gr.File(
                    label="Upload Input Graph File",
                    file_types=[".txt"],
                    type="binary",
                    file_count="single"
                )
                input_graph_field = gr.Textbox(
                    label="Input Graph", 
                    interactive=True, 
                    lines=5, 
                    elem_classes="monospace",
                    placeholder="Enter the graph in the following format:\n\nABC\n1 a 2\n2 b 3\n3 c 1"
                )
            input_graph_display = gr.Plot(label="Input Graph", value=create_empty_plot())

        with gr.Row():
            with gr.Column():
                production_file_upload = gr.File(
                    label="Upload Production Rule File",
                    file_types=[".txt"],
                    type="binary",
                    file_count="single"
                )
                production_rule_field = gr.Textbox(
                    label="Production Rule", 
                    interactive=True, 
                    lines=15, 
                    elem_classes="monospace",
                    placeholder="Enter the production rule in the following format:\n\nABCD\n1 a 2\n2 b 3\n4 d 1\n\nABCD\n1 a 2\n2 b 3\n2 x 4\n\nABCD\n1 a 2\n2 b 3\n2 x 4"
                )
            with gr.Column():
                mapping_field = gr.Textbox(
                    label="Indexes Mapping", 
                    interactive=True, 
                    lines=5, 
                    elem_classes="monospace",
                    placeholder="Leave empty to use the default mapping, identity, e.g.\n\n1 1\n2 2\n3 3"
                )
            
        with gr.Row(equal_height=True):
            L_graph_display = gr.Plot(label="L", value=create_empty_plot())
            K_graph_display = gr.Plot(label="K", value=create_empty_plot())
            R_graph_display = gr.Plot(label="R", value=create_empty_plot())

        with gr.Row():
            with gr.Column(scale=1):
                apply_button = gr.Button("Apply", elem_classes="circle-button")
                use_as_input_button = gr.Button("Use as Input")
            with gr.Column(scale=3):
                output_graph_display = gr.Plot(label="Output Graph")

        input_file_upload.upload(
            load_file,
            [input_file_upload],
            [input_graph_field]
        )
        production_file_upload.upload(
            load_file,
            [production_file_upload],
            [production_rule_field]
        )

        input_graph_field.change(process_input_graph, [input_graph_field], [input_graph_display])
        production_rule_field.change(process_production_rule, [production_rule_field], [L_graph_display, K_graph_display, R_graph_display])

        apply_button.click(apply_production_rule, [input_graph_field, production_rule_field, mapping_field], [output_graph_display])

        use_as_input_button.click(use_as_input, [], [input_graph_field])

    demo.launch()
