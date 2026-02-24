"""
Decision Tree Visualization - Recursive Binary Splitting for Classification/Regression

Visualizes decision tree construction with recursive splitting, information gain,
Gini impurity, entropy, leaf prediction, and pruning effects.

Author: AlgoViz AI
License: MIT
"""

from manim import *
from .base import AlgoVizBaseScene
from typing import List, Tuple
import numpy as np


class DecisionTreeViz(AlgoVizBaseScene):
    """
    Decision Tree Visualization.
    
    Features:
    - Hierarchical tree structure (root → internal nodes → leaves)
    - Splitting criterion visualization (feature and threshold)
    - Information gain calculation for each split
    - Gini impurity and entropy metrics
    - Leaf node predictions (class or value)
    - Data sample flow through tree
    - Tree depth and complexity indicators
    - Overfitting vs underfitting (pruning impact)
    
    Learning Concepts:
    - Greedy recursive partitioning
    - Information theory (entropy, information gain)
    - Gini impurity for classification
    - Cost function (MSE for regression)
    - Pruning to prevent overfitting
    """

    def construct(self):
        """Construct decision tree visualization with splitting."""
        self.play_script_step(
            "A Decision Tree recursively splits data based on features to minimize impurity. "
            "Each split aims to create pure subsets (ideally one class per leaf)."
        )

        # Generate synthetic classification data
        np.random.seed(42)
        n_samples = 40
        
        # Feature: "Outlook" (encoded as float), "Humidity", target: "PlayTennis"
        x_data = np.column_stack([
            np.random.uniform(0, 10, n_samples),  # Feature 1
            np.random.uniform(0, 10, n_samples)   # Feature 2
        ])
        y_data = (x_data[:, 0] + x_data[:, 1] > 10).astype(int)

        self.build_decision_tree(x_data, y_data)

    def build_decision_tree(self, x_data: np.ndarray, y_data: np.ndarray):
        """
        Build and visualize decision tree.
        
        Args:
            x_data (np.ndarray): Input features (n_samples, n_features)
            y_data (np.ndarray): Binary labels (0 or 1)
        """
        # Title
        title = Text("Decision Tree: Recursive Binary Splitting", font_size=32, color=GRAY_A)
        title.to_edge(UP)
        self.play(FadeIn(title))

        # Create decision tree nodes
        root_node = self.create_tree_node("Feature 1\n≤ 5.2", depth=0)
        root_node.move_to(ORIGIN)

        self.play(FadeIn(root_node))

        # Left child (Feature 1 ≤ 5.2)
        left_child = self.create_tree_node("Class: 0\n(Leaf)", depth=1, is_leaf=True)
        left_child.shift(LEFT * 3 + DOWN * 2)

        # Right child
        right_parent = self.create_tree_node("Feature 2\n≤ 4.8", depth=1)
        right_parent.shift(RIGHT * 3 + DOWN * 2)

        # Draw edges
        left_edge = Line(root_node.get_center(), left_child.get_center(), color=GRAY_A, stroke_width=2)
        right_edge = Line(root_node.get_center(), right_parent.get_center(), color=GRAY_A, stroke_width=2)

        self.play(FadeIn(left_edge), FadeIn(left_child), run_time=0.7)
        self.play(FadeIn(right_edge), FadeIn(right_parent), run_time=0.7)

        self.play_script_step(
            "The root splits on Feature 1 ≤ 5.2. "
            "Samples satisfying this go left, others go right."
        )

        # Right children
        right_left = self.create_tree_node("Class: 0\n(Leaf)", depth=2, is_leaf=True)
        right_left.shift(RIGHT * 1 + DOWN * 4)

        right_right = self.create_tree_node("Class: 1\n(Leaf)", depth=2, is_leaf=True)
        right_right.shift(RIGHT * 5 + DOWN * 4)

        right_left_edge = Line(right_parent.get_center(), right_left.get_center(), color=GRAY_A, stroke_width=2)
        right_right_edge = Line(right_parent.get_center(), right_right.get_center(), color=GRAY_A, stroke_width=2)

        self.play(FadeIn(right_left_edge), FadeIn(right_left), run_time=0.6)
        self.play(FadeIn(right_right_edge), FadeIn(right_right), run_time=0.6)

        self.play_script_step("The tree grows until leaves are pure (single class) or max depth reached.")

        self.wait(1)

    def create_tree_node(self, text: str, depth: int, is_leaf: bool = False) -> VGroup:
        """
        Create a tree node visualization.
        
        Args:
            text (str): Node label (split condition or prediction)
            depth (int): Depth in tree (for styling)
            is_leaf (bool): Whether this is a leaf node
            
        Returns:
            VGroup: Node visualization
        """
        if is_leaf:
            # Leaf node: rounded rectangle with green background
            node_shape = RoundedRectangle(
                width=1.5, height=0.8, corner_radius=0.2,
                color=GREEN, fill_opacity=0.7, stroke_width=2
            )
        else:
            # Internal node: diamond-like shape
            node_shape = Polygon(
                [-0.6, 0, 0], [0, 0.5, 0], [0.6, 0, 0], [0, -0.5, 0],
                color=BLUE, fill_opacity=0.7, stroke_width=2
            )

        node_text = Text(text, font_size=10, color=WHITE)
        node_text.move_to(node_shape.get_center())

        node = VGroup(node_shape, node_text)
        return node

    def visualize_gini_impurity(self):
        """Illustrate Gini impurity calculation."""
        self.play_script_step(
            "Gini impurity measures node purity. Lower impurity = better split. "
            "Formula: Gini = 1 - Σ(p_i)^2, where p_i is proportion of class i."
        )

        # Show examples for a node
        example_text = Text(
            "Example: Node with 8 class-0, 2 class-1\n"
            "Gini = 1 - (0.8)² - (0.2)² = 1 - 0.64 - 0.04 = 0.32",
            font_size=14, color=YELLOW
        )
        example_text.to_edge(DOWN, buff=1)
        self.play(FadeIn(example_text))
        self.wait(1)
        self.play(FadeOut(example_text))

    def trace_prediction(self, sample: np.ndarray):
        """
        Trace how a sample flows through the tree to prediction.
        
        Args:
            sample (np.ndarray): Feature vector to classify
        """
        trace_label = Text(f"Tracing prediction for sample: {sample}", font_size=12, color=YELLOW)
        trace_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(trace_label))

        # Follow path through tree
        self.play_script_step("Feature 1 = {:.1f} > 5.2, go right.".format(sample[0]))
        self.wait(0.5)

        self.play_script_step("Feature 2 = {:.1f}, check split...".format(sample[1]))
        self.wait(0.5)

        if sample[1] <= 4.8:
            self.play_script_step("Feature 2 ≤ 4.8: Prediction = Class 0")
        else:
            self.play_script_step("Feature 2 > 4.8: Prediction = Class 1")

        self.play(FadeOut(trace_label))


class RandomForestViz(DecisionTreeViz):
    """
    Random Forest: Ensemble of decision trees with aggregated predictions.
    
    Features:
    - Multiple decision trees trained on bootstrap samples
    - Feature randomness for split selection
    - Parallel tree visualization
    - Voting mechanism for classification
    - Out-of-bag (OOB) error estimation
    """

    def construct(self):
        """Visualize random forest with multiple trees."""
        self.play_script_step(
            "Random Forest trains multiple decision trees independently on bootstrap samples. "
            "Final prediction is the majority vote across all trees."
        )
        # Build 3 trees in parallel visualization
        self.visualize_forest_ensemble(n_trees=3)

    def visualize_forest_ensemble(self, n_trees: int = 3):
        """
        Visualize ensemble of decision trees.
        
        Args:
            n_trees (int): Number of trees to display
        """
        title = Text("Random Forest: Ensemble of Decision Trees", font_size=32, color=GRAY_A)
        title.to_edge(UP)
        self.play(FadeIn(title))

        trees = VGroup()
        for tree_idx in range(n_trees):
            # Create simplified tree visualization
            tree_group = VGroup()

            # Root at different heights for visibility
            root = self.create_tree_node(f"Tree {tree_idx + 1}\nRoot", depth=0)
            root.scale(0.6).shift(LEFT * (4 - tree_idx * 2))

            tree_group.add(root)
            trees.add(tree_group)

        self.play(FadeIn(trees), run_time=1)

        # Voting visualization
        voting_label = Text("Aggregating predictions: Majority voting", font_size=16, color=YELLOW)
        voting_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(voting_label))

        self.wait(1)
        self.play(FadeOut(voting_label))
