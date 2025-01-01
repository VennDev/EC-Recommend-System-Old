import yaml
from graphviz import Digraph


def yaml_to_graph(yaml_file, output_file):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)

    dot = Digraph(comment="YAML Diagram")

    def build_graph(data, parent=None):
        if isinstance(data, dict):
            for key, value in data.items():
                dot.node(key)
                if parent:
                    dot.edge(parent, key)
                build_graph(value, key)
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                item_key = f"{parent}_{idx}"
                dot.node(item_key, label=str(item))
                if parent is not None:
                    dot.edge(parent, item_key)

    build_graph(data)
    dot.render(output_file, format="dot")


yaml_to_graph("ai_config.yml", "output_images")

