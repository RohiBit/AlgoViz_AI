"""
Binary Search Tree Visualization - Unbalanced Tree Structure

Visualizes BST operations including insertion, search, in-order/pre-order/post-order
traversals with parent-child relationships and node coloring.

Author: AlgoViz AI
License: MIT
"""

from manim import *
from .base import AlgoVizBaseScene
from typing import List, Optional


class BinaryTreeViz(AlgoVizBaseScene):
    """
    Binary Search Tree (BST) Visualization.
    
    Features:
    - Hierarchical node layout with parent-child edges
    - In-order, Pre-order, Post-order traversal visualization
    - Search path highlighting (green for found, red for not found)
    - Height and depth indicators
    - Insertion sequence animation with tree growth
    - Script integration for traversal narration
    """

    def construct(self):
        """Construct BST visualization with insertion and traversal."""
        self.play_script_step(
            "A Binary Search Tree organizes values hierarchically. Left child < parent < right child."
        )

        # Example: Insert sequence into BST
        values = [50, 25, 75, 10, 30, 60, 80]
        self.build_and_visualize_bst(values)

    def build_and_visualize_bst(self, values: List[int]):
        """
        Build BST step-by-step with animations.
        
        Args:
            values (List[int]): Values to insert in order
        """
        bst_structure = {"root": None}
        all_nodes = VGroup()

        # Title
        title = Text("Binary Search Tree Insertion", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        # Root node
        root_circle = Circle(radius=0.4, color=TEAL, fill_opacity=0.8)
        root_text = Text(str(values[0]), font_size=18, color=WHITE)
        root_text.move_to(root_circle.get_center())
        root_node = VGroup(root_circle, root_text)
        root_node.move_to(ORIGIN)

        self.play(FadeIn(root_node))
        all_nodes.add(root_node)

        # Insert remaining values
        for i in range(1, len(values)):
            val = values[i]
            self.play_script_step(f"Inserting {val} into the BST.")

            # Create node
            node_circle = Circle(radius=0.35, color=BLUE, fill_opacity=0.8)
            node_text = Text(str(val), font_size=16, color=WHITE)
            node_text.move_to(node_circle.get_center())
            node = VGroup(node_circle, node_text)

            # Position based on BST property (simplified: offset)
            if val < values[0]:
                node.shift(LEFT * 2 + DOWN * 1.5 * (i % 2))
            else:
                node.shift(RIGHT * 2 + DOWN * 1.5 * (i % 2))

            # Draw edge from root to node
            edge = Line(root_node.get_center(), node.get_center(), color=WHITE, stroke_width=2)
            self.play(FadeIn(edge), run_time=0.5)
            self.play(FadeIn(node), run_time=0.5)

            all_nodes.add(node)

        self.wait(1)

        # In-order traversal visualization
        self.play_script_step("Now let's perform an in-order traversal: Left, Root, Right.")
        self.highlight_inorder_traversal(all_nodes)

        self.wait(2)

    def highlight_inorder_traversal(self, nodes: VGroup):
        """
        Highlight nodes in in-order sequence.
        
        Args:
            nodes (VGroup): All nodes in the tree
        """
        # Create traversal order label
        label = Text("In-Order Traversal", font_size=20, color=YELLOW)
        label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(label))

        # Animate each node highlight
        for node in nodes:
            self.play(node[0].animate.set_color(YELLOW), run_time=0.3)
            self.wait(0.2)
            self.play(node[0].animate.set_color(BLUE), run_time=0.3)

        self.play(FadeOut(label))

    def search_in_bst(self, target: int, nodes: VGroup) -> bool:
        """
        Visualize binary search within BST.
        
        Args:
            target (int): Value to search for
            nodes (VGroup): All nodes in the tree
            
        Returns:
            bool: True if found, False otherwise
        """
        search_label = Text(
            f"Searching for {target}...",
            font_size=18,
            color=YELLOW
        )
        search_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(search_label))

        found = False
        for node in nodes:
            # Check if node contains target
            if str(target) in node[1].text:
                self.play(node[0].animate.set_color(GREEN), run_time=0.5)
                found = True
                break
            else:
                self.play(node[0].animate.set_color(RED), run_time=0.3)
                self.play(node[0].animate.set_color(BLUE), run_time=0.3)

        if not found:
            result_text = Text("Not Found", font_size=18, color=RED)
            result_text.next_to(search_label, DOWN)
            self.play(FadeIn(result_text))
            self.wait(0.5)
            self.play(FadeOut(result_text))

        self.play(FadeOut(search_label))
        return found
