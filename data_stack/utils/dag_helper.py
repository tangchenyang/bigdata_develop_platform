import logging
import os


class DAGHelper:

    def __init__(self, graph = None):
        if graph is None:
            import graphviz
            graph = graphviz.Digraph(strict=True)
        self.graph = graph
        self.all_nodes = []
        self.all_edges = []
        self.setup_graph()

    def setup_graph(self):
        self.graph.graph_attr["rankdir"] = "LR"  # Left to Right

    def add_node(self, node_id):
        if node_id in self.all_nodes:
            return

        node_attrs = {
            "shape": "box",
            "color": "azure4",
            "fontsize": "12.0",
        }

        logging.info(f"Add node: {node_id}")
        self.graph.node(node_id, **node_attrs)
        self.all_nodes.append(node_id)

    def add_edge(self, from_node, to_node):
        if (from_node, to_node) in self.all_edges:
            return
        edge_attrs = {"arrowsize": "0.5"}
        logging.info(f"Add edge: {from_node} -> {to_node}")
        self.graph.edge(from_node, to_node, **edge_attrs)
        self.all_edges.append((from_node, to_node))


    def draw(self, path):
        file_folder = os.path.dirname(path)
        file_name, file_format = os.path.basename(path).split(".")
        output_file_path = f"file://{file_folder}/{file_name}.{file_format}"

        logging.info(f"Saving dag image into {output_file_path}")
        self.graph.render(directory=file_folder,  filename=file_name, format=file_format,)

        graph_describe_file_path = f"{file_folder}/{file_name}"
        os.remove(graph_describe_file_path)
        logging.info(f"Saved dag image into {output_file_path}")


