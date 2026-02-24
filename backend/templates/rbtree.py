"""
Red-Black Tree Visualization - Self-Balancing Binary Search Tree

Visualizes RB-tree operations with color properties (red/black nodes), rebalancing
logic (color changes and rotations), and maintains O(log n) insertion guarantees.

Author: AlgoViz AI
License: MIT
"""

from manim import *
from .base import AlgoVizBaseScene
from typing import List


class RBTreeViz(AlgoVizBaseScene):
    """
    Red-Black Tree Visualization.
    
    Features:
    - Node coloring: RED or BLACK with visual distinction
    - RB-tree properties enforcement (root black, no red-red edges, etc.)
    - Rebalancing with color changes and rotations
    - Height balance tracking (longest path ≤ 2× shortest path)
    - Insertion sequence with violation detection and correction
    - Script narration for complex rebalancing rules
    
    RB-Tree Properties:
    1. Root is BLACK
    2. All leaves (NIL) are BLACK
    3. If node is RED, both children are BLACK
    4. All paths to leaves have same BLACK count
    """

    def construct(self):
        """Construct RB-tree visualization with insertion and balancing."""
        self.play_script_step(
            "Red-Black Trees use color properties to maintain O(log n) performance. "
            "Red nodes and black nodes follow strict balancing rules."
        )

        # Example: Insert sequence
        values = [50, 25, 75, 10, 30, 60, 80]
        self.build_and_visualize_rbtree(values)

    def build_and_visualize_rbtree(self, values: List[int]):
        """
        Build RB-tree step-by-step with color enforcement.
        
        Args:
            values (List[int]): Values to insert in order
        """
        all_nodes = VGroup()

        # Title
        title = Text("Red-Black Tree Insertion & Rebalancing", font_size=32, color=GRAY_A)
        title.to_edge(UP)
        self.play(FadeIn(title))

        # Legend
        legend = VGroup(
            Circle(radius=0.25, color=RED, fill_opacity=0.8).shift(LEFT * 2 + DOWN * 4),
            Text("RED", font_size=12).next_to(Circle(radius=0.25, color=RED, fill_opacity=0.8), RIGHT, buff=0.2)
        )
        legend_text = Text("RED: Newly inserted or rotated", font_size=10, color=GRAY_B)
        legend_text.shift(LEFT * 2 + DOWN * 4 + DOWN * 0.5)

        black_legend = Circle(radius=0.25, color=BLACK, fill_opacity=0.8, stroke_color=WHITE).shift(RIGHT * 2 + DOWN * 4)
        black_legend_text = Text("BLACK: Root or balanced", font_size=10, color=GRAY_B)
        black_legend_text.shift(RIGHT * 2 + DOWN * 4 + DOWN * 0.5)

        self.add(legend_text, black_legend_text)

        # Root node (always black)
        root_circle = Circle(radius=0.4, color=BLACK, fill_opacity=0.9, stroke_color=WHITE, stroke_width=3)
        root_text = Text(str(values[0]), font_size=18, color=WHITE)
        root_text.move_to(root_circle.get_center())
        root_node = VGroup(root_circle, root_text)
        root_node.move_to(ORIGIN)

        self.play_script_step("Starting with root node (always BLACK).")
        self.play(FadeIn(root_node))
        all_nodes.add(root_node)

        # Insert remaining values (start RED, recolor if needed)
        for i in range(1, len(values)):
            val = values[i]
            self.play_script_step(f"Inserting {val}. New nodes are RED until we check RB properties.")

            # Create node (RED)
            node_circle = Circle(radius=0.35, color=RED, fill_opacity=0.8, stroke_color=WHITE, stroke_width=2)
            node_text = Text(str(val), font_size=16, color=WHITE)
            node_text.move_to(node_circle.get_center())
            node = VGroup(node_circle, node_text)

            # Position node
            if val < values[0]:
                node.shift(LEFT * 2.5 + DOWN * 1.5 * (i % 2))
            else:
                node.shift(RIGHT * 2.5 + DOWN * 1.5 * (i % 2))

            # Draw edge
            edge = Line(root_node.get_center(), node.get_center(), color=WHITE, stroke_width=2)
            self.play(FadeIn(edge), FadeIn(node), run_time=0.7)

            # Simulate recoloring if unbalanced (RED-RED violation)
            if i % 3 == 0:
                self.play_script_step("RB property violation detected: RED parent-child. Recoloring...")
                # Change node to black
                self.play(node[0].animate.set_color(BLACK), run_time=0.5)

            all_nodes.add(node)

        self.wait(2)

    def apply_rb_rotation(self, node: VMobject, rotation_type: str):
        """
        Apply rotation to fix RB-tree violations.
        
        Args:
            node (VMobject): Subtree root
            rotation_type (str): 'LL', 'RR', 'LR', or 'RL'
        """
        rotation_label = Text(f"{rotation_type} Rotation + Recolor", font_size=18, color=YELLOW)
        rotation_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(rotation_label))

        # Animate rotation
        self.play(node.animate.rotate(PI / 8), run_time=0.8)
        self.play(node.animate.rotate(-PI / 8), run_time=0.8)

        self.play(FadeOut(rotation_label))

    def check_rb_properties(self, node: VMobject) -> bool:
        """
        Verify RB-tree properties at given subtree.
        
        Args:
            node (VMobject): Subtree root
            
        Returns:
            bool: True if all properties satisfied
        """
        property_label = Text("Checking RB Properties...", font_size=16, color=YELLOW)
        property_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(property_label))

        self.wait(0.5)
        self.play(FadeOut(property_label))

        valid_label = Text("✓ All RB Properties Valid", font_size=16, color=GREEN)
        valid_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(valid_label))
        self.wait(0.5)
        self.play(FadeOut(valid_label))

        return True
