"""
Random Forest Visualization - Ensemble Learning with Multiple Decision Trees

Visualizes random forest construction: bootstrap sampling, parallel tree growth,
feature randomness, voting mechanism, and out-of-bag (OOB) error estimation.

Author: AlgoViz AI
License: MIT
"""

from manim import *
from .base import AlgoVizBaseScene
from typing import List
import numpy as np


class RandomForestViz(AlgoVizBaseScene):
    """
    Random Forest Visualization.
    
    Features:
    - Bootstrap aggregating (bagging): sample with replacement
    - Multiple independent decision trees trained in parallel
    - Feature randomness: random feature subset per split
    - Color-coded trees for visualization
    - Voting mechanism: majority vote for classification
    - Out-of-bag (OOB) error: error on samples not in bootstrap
    - Feature importance from tree aggregation
    - Bias-variance tradeoff visualization
    
    Learning Concepts:
    - Bootstrap resampling (with replacement)
    - Ensemble learning (combining weak learners)
    - Feature subsampling reduces correlation between trees
    - Parallel training enables efficiency
    - Robustness through aggregation
    """

    def __init__(self, n_trees: int = 5, *args, **kwargs):
        """
        Initialize random forest with specified number of trees.
        
        Args:
            n_trees (int): Number of trees in the forest (default 5)
        """
        self.n_trees = n_trees
        super().__init__(*args, **kwargs)

    def construct(self):
        """Construct random forest visualization."""
        self.play_script_step(
            f"Random Forest trains {self.n_trees} decision trees independently using bootstrap samples. "
            f"Each tree has a slightly different training set, making them diverse."
        )

        # Generate synthetic classification data
        np.random.seed(42)
        n_samples = 60
        x_data = np.column_stack([
            np.random.uniform(0, 10, n_samples),
            np.random.uniform(0, 10, n_samples)
        ])
        y_data = ((x_data[:, 0] + x_data[:, 1]) > 10).astype(int)

        self.visualize_bootstrap_and_trees(x_data, y_data)

    def visualize_bootstrap_and_trees(self, x_data: np.ndarray, y_data: np.ndarray):
        """
        Visualize bootstrap sampling and parallel tree training.
        
        Args:
            x_data (np.ndarray): Input features
            y_data (np.ndarray): Target labels
        """
        # Title
        title = Text(f"Random Forest: {self.n_trees} Bootstrap Trees", font_size=32, color=GRAY_A)
        title.to_edge(UP)
        self.play(FadeIn(title))

        colors = [BLUE, RED, GREEN, YELLOW, PURPLE]
        tree_colors = colors[:self.n_trees]

        # Show bootstrap sampling for each tree
        self.play_script_step("Step 1: Bootstrap Sampling - create multiple training sets by sampling with replacement.")

        bootstrap_samples = VGroup()
        for tree_idx in range(min(3, self.n_trees)):  # Show 3 trees for clarity
            # Bootstrap sample text
            sample_text = Text(
                f"Tree {tree_idx + 1}\nSample Size: {len(x_data)}\n(with replacement)",
                font_size=10,
                color=tree_colors[tree_idx]
            )
            sample_text.shift(LEFT * (3 - tree_idx * 3))
            bootstrap_samples.add(sample_text)

        self.play(FadeIn(bootstrap_samples), run_time=1)
        self.wait(0.5)

        # Visualize tree training
        self.play_script_step("Step 2: Train a decision tree on each bootstrap sample.")

        tree_nodes = VGroup()
        for tree_idx in range(min(3, self.n_trees)):
            # Create simplified tree node
            root = Polygon(
                [-0.4, 0, 0], [0, 0.4, 0], [0.4, 0, 0], [0, -0.4, 0],
                color=tree_colors[tree_idx],
                fill_opacity=0.7,
                stroke_width=2
            )
            root.shift(LEFT * (3 - tree_idx * 3) + DOWN * 2)

            root_text = Text(
                "Root\nSplit",
                font_size=8,
                color=WHITE
            )
            root_text.move_to(root.get_center())

            tree_node = VGroup(root, root_text)
            tree_nodes.add(tree_node)

        self.play(FadeIn(tree_nodes), run_time=1)
        self.wait(0.5)

        # Aggregation/Voting
        self.play_script_step("Step 3: Aggregate predictions through voting.")

        # Show voting process
        voting_area = Rectangle(
            width=4, height=2,
            color=YELLOW,
            fill_opacity=0.2,
            stroke_width=2
        )
        voting_area.shift(RIGHT * 2 + DOWN * 0.5)

        voting_text = Text(
            "Voting\nTree 1: Class 0\nTree 2: Class 1\nTree 3: Class 0\n—————\nFinal: Class 0 (2/3)",
            font_size=10,
            color=YELLOW
        )
        voting_text.move_to(voting_area.get_center())

        self.play(FadeIn(voting_area), FadeIn(voting_text), run_time=0.8)
        self.wait(1)

        self.play(FadeOut(voting_area), FadeOut(voting_text), FadeOut(bootstrap_samples), FadeOut(tree_nodes))

        self.wait(2)

    def visualize_oob_error(self):
        """
        Visualize Out-of-Bag (OOB) error estimation.
        
        OOB samples are those not included in a particular bootstrap sample.
        They can be used as a validation set without a separate test set.
        """
        self.play_script_step(
            "Out-of-Bag (OOB) Error: On average, ~37% of samples are left out of each bootstrap. "
            "We use these to estimate generalization error without a separate test set."
        )

        # Visualization showing samples left out
        all_samples = 20
        in_sample = 13
        oob_samples = all_samples - in_sample

        sample_display = VGroup()
        for i in range(all_samples):
            if i < in_sample:
                dot = Dot(color=BLUE, radius=0.08).shift(RIGHT * i * 0.4)
            else:
                dot = Dot(color=RED, radius=0.08).shift(RIGHT * i * 0.4)
            sample_display.add(dot)

        legend_in = VGroup(
            Dot(color=BLUE, radius=0.06),
            Text("In-Bag", font_size=10, color=BLUE).next_to(Dot(color=BLUE, radius=0.06), RIGHT, buff=0.1)
        )

        legend_oob = VGroup(
            Dot(color=RED, radius=0.06),
            Text("OOB (Out-of-Bag)", font_size=10, color=RED).next_to(Dot(color=RED, radius=0.06), RIGHT, buff=0.1)
        )

        self.play(FadeIn(sample_display), run_time=1)
        self.play(FadeIn(legend_in), FadeIn(legend_oob), run_time=0.7)

        self.play_script_step(f"OOB error rate = misclassifications on OOB samples / total OOB samples")

        self.wait(2)

    def visualize_feature_importance(self):
        """Visualize feature importance from aggregated trees."""
        self.play_script_step(
            "Feature Importance: measure each feature's contribution to decreasing impurity "
            "across all trees and splits."
        )

        # Create bar chart of feature importance
        features = ["Feature 1", "Feature 2", "Feature 3", "Feature 4", "Feature 5"]
        importances = [0.35, 0.28, 0.22, 0.10, 0.05]

        # Draw axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 0.4, 0.1],
            axis_config={"color": GRAY_B},
            tips=False,
        )

        # Draw bars
        bars = VGroup()
        for i, (feat, imp) in enumerate(zip(features, importances)):
            bar = Rectangle(
                width=0.6,
                height=imp * 10,
                color=BLUE if imp > 0.2 else YELLOW if imp > 0.1 else RED,
                fill_opacity=0.8,
                stroke_width=1.5
            )
            bar.shift(RIGHT * (i + 1) * 0.9 + UP * imp * 5)
            bars.add(bar)

        self.play(FadeIn(axes), FadeIn(bars), run_time=1)

        self.play_script_step("Features with higher bars contribute more to the forest's predictions.")

        self.wait(2)
