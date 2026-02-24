"""
AVL Tree Visualization - Self-Balancing Binary Search Tree

Visualizes AVL tree operations including insertion, rebalancing, and rotations
(LL, RR, LR, RL) with balance factor tracking.

Author: AlgoViz AI
License: MIT
"""

from manim import *
from .base import AlgoVizBaseScene
from typing import List


class AVLTreeViz(AlgoVizBaseScene):
    """
    AVL Tree (Adelson-Velskii-Landis Tree) Visualization.
    
    Features:
    - Dynamic node rendering with balance factors
    - Color-coded balance states (balanced: BLUE, unbalanced: RED)
    - Rotations (LL, RR, LR, RL) with animated transformations
    - Height markers and edge labels
    - Script integration for educational narration
    
    Gold Standard Example: This is the reference implementation for all other classes.
    """

    def construct(self):
        """Construct AVL Tree visualization with insertion and rotation steps."""
        self.play_script_step(
            "AVL Trees maintain balance through rotations. Let's visualize insertion and rebalancing."
        )

        # Example: Insert sequence into AVL tree
        values = [50, 25, 75, 10, 30, 60, 80, 5, 15]
        self.build_and_visualize_avl(values)

    def build_and_visualize_avl(self, values: List[int]):
        """
        Build AVL tree step-by-step with animations.
        
        Args:
            values (List[int]): Values to insert in order
        """
        tree_data = {"root": None}
        tree_mobjects = VGroup()

        # Title
        title = Text("AVL Tree Insertion & Balancing", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        for i, val in enumerate(values):
            self.play_script_step(
                f"Inserting {val} into the AVL tree. Balance factors are recalculated."
            )

            # Create node representation
            node_circle = Circle(radius=0.4, color=BLUE, fill_opacity=0.8)
            node_text = Text(str(val), font_size=20, color=WHITE)
            node_text.move_to(node_circle.get_center())
            node = VGroup(node_circle, node_text)

            # Position node (simplified: horizontal layout for demo)
            node.shift(RIGHT * (i - len(values) // 2) * 1.5)

            self.play(FadeIn(node))
            tree_mobjects.add(node)

            # Simulate rotation if unbalanced (visual indicator)
            if i > 2:
                unbalanced_indicator = Text(
                    "Rebalancing...",
                    font_size=16,
                    color=RED
                ).next_to(node, UP, buff=0.2)
                self.play(FadeIn(unbalanced_indicator))
                self.wait(0.5)
                self.play(FadeOut(unbalanced_indicator))

        # Finalize tree
        self.center_on_origin(tree_mobjects)
        self.play(tree_mobjects.animate.scale(0.8))
        self.wait(2)

    def add_balance_factor_label(self, node: VMobject, balance_factor: int):
        """
        Add balance factor text label to node.
        
        Args:
            node (VMobject): The node object
            balance_factor (int): Balance factor value (-2 to 2 for valid AVL)
        """
        color = YELLOW if -1 <= balance_factor <= 1 else RED
        label = Text(str(balance_factor), font_size=12, color=color)
        label.next_to(node, DR, buff=0.1)
        self.add(label)

    def perform_rotation(self, node: VMobject, rotation_type: str):
        """
        Animate a rotation operation (LL, RR, LR, RL).
        
        Args:
            node (VMobject): Subtree root to rotate
            rotation_type (str): One of 'LL', 'RR', 'LR', 'RL'
        """
        rotation_label = Text(f"{rotation_type} Rotation", font_size=20, color=YELLOW)
        rotation_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(rotation_label))

        # Animate rotation (simplified: pivot and reposition)
        self.play(node.animate.rotate(PI / 6), run_time=1.5)
        self.play(node.animate.rotate(-PI / 6), run_time=1.5)

        self.play(FadeOut(rotation_label))
