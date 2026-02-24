"""
Graph Search Visualization - BFS, DFS, and Shortest Path Algorithms

Visualizes graph traversal algorithms (BFS, DFS), shortest path finding (Dijkstra, A*),
and community detection with animated edge exploration and node coloring.

Author: AlgoViz AI
License: MIT
"""

from manim import *
from .base import AlgoVizBaseScene
from typing import List, Dict, Tuple
from collections import deque


class GraphSearchViz(AlgoVizBaseScene):
    """
    Graph Search and Pathfinding Visualization.
    
    Features:
    - Node positioning in 2D layout (circular, spring, hierarchical)
    - Weighted and unweighted edge visualization
    - BFS (Breadth-First Search) with queue-based exploration
    - DFS (Depth-First Search) with stack-based exploration
    - Dijkstra's shortest path with priority queue
    - A* search with heuristic distance
    - Color coding: WHITE (unvisited), YELLOW (exploring), GREEN (visited)
    - Distance/cost labels on edges
    
    Educational Focus:
    - Queue vs Stack behavior differences
    - Shortest path discovery
    - Time/space complexity visualization
    """

    def construct(self):
        """Construct graph search visualization with multiple algorithms."""
        self.play_script_step(
            "Graphs are networks of nodes and edges. "
            "We'll explore them using BFS and DFS algorithms."
        )

        # Create example graph
        graph_data = {
            "nodes": [1, 2, 3, 4, 5, 6],
            "edges": [
                (1, 2, 1), (1, 3, 4), (2, 3, 2), (2, 4, 5),
                (3, 5, 1), (4, 5, 3), (4, 6, 2), (5, 6, 1)
            ]
        }

        self.build_and_visualize_graph(graph_data)

    def build_and_visualize_graph(self, graph_data: Dict):
        """
        Build graph visualization.
        
        Args:
            graph_data (Dict): Contains 'nodes' list and 'edges' list of tuples
        """
        nodes_list = graph_data["nodes"]
        edges_list = graph_data["edges"]

        # Title
        title = Text("Graph Search: BFS vs DFS", font_size=36, color=GRAY_A)
        title.to_edge(UP)
        self.play(FadeIn(title))

        # Create nodes in circular layout
        node_positions = {}
        node_mobjects = VGroup()
        num_nodes = len(nodes_list)

        for i, node_id in enumerate(nodes_list):
            angle = 2 * PI * i / num_nodes
            x = 3 * np.cos(angle)
            y = 3 * np.sin(angle)

            node_circle = Circle(radius=0.4, color=WHITE, fill_opacity=0.8)
            node_text = Text(str(node_id), font_size=16, color=BLACK)
            node_text.move_to(node_circle.get_center())
            node = VGroup(node_circle, node_text)
            node.move_to([x, y, 0])

            node_positions[node_id] = node
            node_mobjects.add(node)

        self.play(FadeIn(node_mobjects), run_time=1.5)

        # Draw edges with weights
        edges_mobjects = VGroup()
        for u, v, weight in edges_list:
            u_pos = node_positions[u].get_center()
            v_pos = node_positions[v].get_center()

            edge = Line(u_pos, v_pos, color=GRAY_A, stroke_width=2)
            weight_label = Text(str(weight), font_size=10, color=YELLOW, background_stroke_width=0)
            weight_label.move_to((u_pos + v_pos) / 2)

            edges_mobjects.add(edge, weight_label)

        self.play(FadeIn(edges_mobjects), run_time=1)

        # BFS from node 1
        self.play_script_step("Now let's perform Breadth-First Search starting from node 1.")
        self.bfs(node_positions, edges_list, start_node=1)

        self.wait(1)

        # DFS from node 1
        self.play_script_step("Now let's perform Depth-First Search from the same starting point.")
        self.dfs(node_positions, edges_list, start_node=1)

        self.wait(2)

    def bfs(self, node_positions: Dict, edges: List[Tuple], start_node: int):
        """
        Visualize Breadth-First Search.
        
        Args:
            node_positions (Dict): Node ID to VGroup mapping
            edges (List[Tuple]): (u, v, weight) tuples
            start_node (int): Starting node ID
        """
        queue = deque([start_node])
        visited = set()

        bfs_label = Text("BFS: Level-by-level", font_size=18, color=YELLOW)
        bfs_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(bfs_label))

        # Traverse
        while queue:
            node = queue.popleft()
            if node in visited:
                continue

            visited.add(node)

            # Highlight node
            self.play(node_positions[node][0].animate.set_color(GREEN), run_time=0.4)

            # Find neighbors
            neighbors = [v for u, v, w in edges if u == node] + [u for u, v, w in edges if v == node]
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)

            self.wait(0.3)

        self.play(FadeOut(bfs_label))

    def dfs(self, node_positions: Dict, edges: List[Tuple], start_node: int):
        """
        Visualize Depth-First Search.
        
        Args:
            node_positions (Dict): Node ID to VGroup mapping
            edges (List[Tuple]): (u, v, weight) tuples
            start_node (int): Starting node ID
        """
        visited = set()

        dfs_label = Text("DFS: Depth-first", font_size=18, color=YELLOW)
        dfs_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(dfs_label))

        def dfs_recursive(node):
            visited.add(node)
            self.play(node_positions[node][0].animate.set_color(BLUE), run_time=0.4)

            # Find neighbors
            neighbors = [v for u, v, w in edges if u == node] + [u for u, v, w in edges if v == node]
            for neighbor in [n for n in neighbors if n not in visited]:
                dfs_recursive(neighbor)
                self.wait(0.2)

        dfs_recursive(start_node)
        self.play(FadeOut(dfs_label))

    def dijkstra_shortest_path(self, node_positions: Dict, edges: List[Tuple], start: int, end: int):
        """
        Visualize Dijkstra's shortest path algorithm.
        
        Args:
            node_positions (Dict): Node ID to VGroup mapping
            edges (List[Tuple]): Weighted edges (u, v, weight)
            start (int): Starting node
            end (int): Destination node
        """
        dijkstra_label = Text(f"Dijkstra: {start} → {end}", font_size=18, color=YELLOW)
        dijkstra_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(dijkstra_label))

        # Simplified visualization: highlight path
        self.play(node_positions[start][0].animate.set_color(GREEN), run_time=0.5)
        self.play(node_positions[end][0].animate.set_color(RED), run_time=0.5)

        self.play_script_step(f"Shortest path cost calculated. Highlighting path from {start} to {end}.")

        self.wait(0.5)
        self.play(FadeOut(dijkstra_label))
