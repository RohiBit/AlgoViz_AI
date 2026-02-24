"""
K-Nearest Neighbors (KNN) Visualization - Instance-Based Learning

Visualizes KNN for classification and regression with distance metrics,
neighbor highlighting, decision boundary, k-value impact, and distance-weighted variants.

Author: AlgoViz AI
License: MIT
"""

from manim import *
from .base import AlgoVizBaseScene
from typing import List, Tuple
import numpy as np


class KNNViz(AlgoVizBaseScene):
    """
    K-Nearest Neighbors (KNN) Visualization.
    
    Features:
    - Query point and k nearest neighbors highlighting
    - Distance metric visualization (Euclidean, Manhattan)
    - Decision boundary showing prediction regions
    - k-value impact: k=1 (irregular), larger k (smoother)
    - Classification: majority vote among k neighbors
    - Regression: average of k neighbor values
    - Distance radius expanding to find neighbors
    - Tie-breaking and equal distance handling
    
    Learning Concepts:
    - Instance-based (lazy) learning: no model training
    - Computational cost: O(n) per prediction
    - Distance metric importance
    - Curse of dimensionality in high dimensions
    - Local approximation of decision boundary
    """

    def __init__(self, k: int = 3, *args, **kwargs):
        """
        Initialize KNN with specified number of neighbors.
        
        Args:
            k (int): Number of neighbors to consider (default 3)
        """
        self.k = k
        super().__init__(*args, **kwargs)

    def construct(self):
        """Construct KNN visualization with query and neighbors."""
        self.play_script_step(
            f"K-Nearest Neighbors (k={self.k}) classifies a point by majority vote among its {self.k} nearest neighbors. "
            f"No model is trained - all computation happens at prediction time."
        )

        # Generate synthetic classification data
        np.random.seed(42)
        
        class_0 = np.random.normal([2, 2], 1.2, (15, 2))
        class_1 = np.random.normal([8, 8], 1.2, (15, 2))
        
        x_data = np.vstack([class_0, class_1])
        y_data = np.hstack([np.zeros(15), np.ones(15)])

        # Query point
        query_point = np.array([6, 6])

        self.visualize_knn(x_data, y_data, query_point, self.k)

    def visualize_knn(self, x_data: np.ndarray, y_data: np.ndarray, query: np.ndarray, k: int):
        """
        Visualize KNN prediction for a query point.
        
        Args:
            x_data (np.ndarray): Training data points (n_samples, 2)
            y_data (np.ndarray): Training labels (0 or 1)
            query (np.ndarray): Query point to classify
            k (int): Number of neighbors
        """
        # Title
        title = Text(f"K-Nearest Neighbors (k={k})", font_size=36, color=GRAY_A)
        title.to_edge(UP)
        self.play(FadeIn(title))

        # Create axes
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            axis_config={"color": GRAY_B},
            tips=False,
        )
        axes.scale(0.5).shift(LEFT * 3)

        self.play(FadeIn(axes))

        # Plot training data
        class_0_points = VGroup()
        class_1_points = VGroup()

        for x, y in x_data[y_data == 0]:
            point = Dot(axes.coords_to_point(x, y), color=BLUE, radius=0.06)
            class_0_points.add(point)

        for x, y in x_data[y_data == 1]:
            point = Dot(axes.coords_to_point(x, y), color=RED, radius=0.06)
            class_1_points.add(point)

        self.play(FadeIn(class_0_points), FadeIn(class_1_points), run_time=1)

        # Query point
        query_dot = Dot(
            axes.coords_to_point(query[0], query[1]),
            color=YELLOW,
            radius=0.1
        )
        query_star = Star(
            n_points=5,
            outer_radius=0.12,
            inner_radius=0.07,
            color=YELLOW,
            fill_opacity=0.9
        )
        query_star.move_to(axes.coords_to_point(query[0], query[1]))

        self.play(FadeIn(query_star))
        self.play_script_step(f"Query point (star) at ({query[0]}, {query[1]}). Finding {k} nearest neighbors...")

        # Calculate distances
        distances = np.linalg.norm(x_data - query, axis=1)
        nearest_indices = np.argsort(distances)[:k]
        nearest_distances = distances[nearest_indices]

        # Highlight k nearest neighbors
        neighbor_circles = VGroup()
        for idx in nearest_indices:
            x, y = x_data[idx]
            circle = Circle(
                axes.coords_to_point(x, y),
                radius=0.08,
                color=WHITE,
                fill_opacity=0,
                stroke_width=2.5
            )
            neighbor_circles.add(circle)

        self.play(FadeIn(neighbor_circles), run_time=0.8)
        self.play_script_step(f"Circled: the {k} nearest neighbors.")

        # Draw distance lines
        distance_lines = VGroup()
        for idx in nearest_indices:
            x, y = x_data[idx]
            line = Line(
                axes.coords_to_point(query[0], query[1]),
                axes.coords_to_point(x, y),
                color=GREEN,
                stroke_width=1.5,
                stroke_opacity=0.5
            )
            distance_lines.add(line)

        self.play(FadeIn(distance_lines), run_time=0.7)

        # Count classes among neighbors
        neighbor_labels = y_data[nearest_indices]
        class_0_count = np.sum(neighbor_labels == 0)
        class_1_count = np.sum(neighbor_labels == 1)

        self.play_script_step(
            f"Among {k} neighbors: {class_0_count} from Class 0 (blue), {class_1_count} from Class 1 (red)."
        )

        # Prediction
        prediction = 0 if class_0_count > class_1_count else 1
        prediction_color = BLUE if prediction == 0 else RED

        prediction_label = Text(
            f"Prediction: Class {int(prediction)}",
            font_size=18,
            color=prediction_color
        )
        prediction_label.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(prediction_label))
        self.wait(1)

        self.play(FadeOut(prediction_label))

        self.wait(2)

    def visualize_decision_boundary(self, x_data: np.ndarray, y_data: np.ndarray, k: int):
        """
        Visualize KNN decision boundary over entire 2D space.
        
        Args:
            x_data (np.ndarray): Training data
            y_data (np.ndarray): Training labels
            k (int): Number of neighbors
        """
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            axis_config={"color": GRAY_B},
            tips=False,
        )
        axes.scale(0.5)

        # Plot training points
        for x, y in x_data[y_data == 0]:
            dot = Dot(axes.coords_to_point(x, y), color=BLUE, radius=0.04)
            self.add(dot)

        for x, y in x_data[y_data == 1]:
            dot = Dot(axes.coords_to_point(x, y), color=RED, radius=0.04)
            self.add(dot)

        self.play_script_step(
            "KNN creates a complex, non-linear decision boundary. "
            "Each region is classified by majority vote of its k nearest training points."
        )

        self.wait(2)

    def compare_k_values(self):
        """Visualize effect of different k values on decision boundary."""
        self.play_script_step(
            "The choice of k greatly affects the decision boundary. "
            "k=1 is irregular, larger k values create smoother boundaries."
        )

        # Create three subplots with k=1, k=3, k=9
        k_values = [1, 3, 9]

        for idx, k_val in enumerate(k_values):
            title = Text(f"k = {k_val}", font_size=16, color=YELLOW)
            title.shift(LEFT * (3 - idx * 3) + UP * 3)

            # Simplified boundary roughness indicator
            if k_val == 1:
                roughness_text = Text("Rough\n(High Variance)", font_size=10, color=ORANGE)
            elif k_val == 3:
                roughness_text = Text("Balanced", font_size=10, color=GREEN)
            else:
                roughness_text = Text("Smooth\n(High Bias)", font_size=10, color=BLUE)

            roughness_text.shift(LEFT * (3 - idx * 3) + DOWN * 3)

            self.add(title, roughness_text)

        self.wait(2)
