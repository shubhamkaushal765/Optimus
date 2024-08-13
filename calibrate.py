from graph import QubitCalGraph

import networkx as nx
from enum import Enum, auto
import random
import time
import heapq

# Usage example
if __name__ == "__main__":
    qubit_graph = QubitCalGraph()
    graph = qubit_graph.graph

    heap = [
        (len(list(graph.predecessors(node))), -len(list(graph.successors(node))), node)
        for node in graph.nodes
    ]
    while heap:
        task = heapq.heappop(heap)
        print(f"Processing: {task}")
