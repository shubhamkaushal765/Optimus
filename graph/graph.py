from pathlib import Path
import yaml, random
import itertools
import networkx as nx
import matplotlib.pyplot as plt

from utils.dict_utils import dotdict


class QubitCalGraph:
    """
    A class to generate and visualize a calibration dependency graph for qubits.

    Attributes:
        config_path (str): Path to the configuration file.
    """

    def __init__(self, config_path="./graph.yml"):
        self.config = dotdict(yaml.safe_load(open(config_path)))
        random.seed(self.config.seed)

        # define qubits and their respective calibrations
        self.qubits = [f"q{i}" for i in range(self.config.qubits)]
        self.cals = [
            f"cal_{q}_{i}"
            for i in range(self.config.each_qubit_cal)
            for q in self.qubits
        ]

        self.graph = self.generate_graph()
        self.cmap = [
            "lightblue" if node in self.qubits else "lightgreen"
            for node in self.graph.nodes()
        ]

    def generate_graph(self):
        """
        Generate a calibration dependency graph.

        Returns:
            nx.DiGraph: The generated graph.
        """

        qubits = self.qubits
        cals = self.cals

        # generate qubit-to-cal pairs
        q2c = list(itertools.product(qubits, cals))
        q2c = random.sample(q2c, len(q2c) // 4)

        # generate cal-to-cal pairs
        c2c = [(x, y) for x in cals for y in cals if x != y]
        c2c = random.sample(c2c, len(c2c) // 10)

        G = nx.DiGraph()
        G.add_nodes_from(qubits + cals)
        G.add_edges_from(q2c + c2c)

        return G

    def plot_graph(self):
        """
        Plot the calibration dependency graph.
        """

        pos = nx.planar_layout(self.graph)
        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            node_color=self.cmap,
            node_size=1000,
            font_size=10,
            font_weight="bold",
            arrows=True,
        )

        plt.title("Calibration Dependency Graph")
        plt.show()

    def save_plot(self, filename="images/calibration_graph.png"):
        """
        Save the calibration dependency graph plot to a file.

        Args:
            filename (str): The name of the file to save the plot to. Defaults to "calibration_graph.png".
        """
        plt.figure(figsize=(12, 8))  # Create a new figure with a larger size
        pos = nx.planar_layout(self.graph)
        nx.draw(
            self.graph,
            pos,
            with_labels=True,
            node_color=self.cmap,
            node_size=1000,
            font_size=10,
            font_weight="bold",
            arrows=True,
        )

        plt.title("Calibration Dependency Graph")
        plt.tight_layout()  # Adjust the layout to prevent cutting off labels
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        plt.close()  # Close the figure to free up memory
        print(f"Graph saved to {filename}")
