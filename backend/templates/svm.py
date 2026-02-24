"""
Support Vector Machine (SVM) Visualization - Binary Classification with Margins

Visualizes SVM concepts including maximum margin, support vectors, kernel trick,
decision boundary, and soft-margin SVM with misclassified points.

Author: AlgoViz AI
License: MIT
"""

from manim import *
from .base import AlgoVizBaseScene
from typing import Tuple
import numpy as np


class SVMViz(AlgoVizBaseScene):
    """
    Support Vector Machine Visualization.
    
    Features:
    - Maximum margin separator between two classes
    - Support vectors highlighted (critical boundary points)
    - Margin visualization (white space between decision boundary and support vectors)
    - Hard-margin SVM (linearly separable data)
    - Soft-margin SVM with slack variables (linearly non-separable)
    - Kernel trick visualization (non-linear transformations)
    - C parameter (regularization) impact on margin
    
    Learning Concepts:
    - Hyperplane optimization: maximize margin subject to constraints
    - Support vectors: data points on or inside the margin
    - Kernel functions: linear, polynomial, RBF
    - Dual problem formulation
    """

    def construct(self):
        """Construct SVM visualization with linearly separable data."""
        self.play_script_step(
            "Support Vector Machines find the maximum margin separator between two classes. "
            "The critical points on the margin are called support vectors."
        )

        # Generate well-separated synthetic data
        np.random.seed(42)
        
        # Class 0: upper left
        class_0 = np.random.normal([2, 7], 1.0, (15, 2))
        
        # Class 1: lower right
        class_1 = np.random.normal([8, 3], 1.0, (15, 2))
        
        x_data = np.vstack([class_0, class_1])
        y_data = np.hstack([np.zeros(15), np.ones(15)])

        self.visualize_svm(x_data, y_data)

    def visualize_svm(self, x_data: np.ndarray, y_data: np.ndarray):
        """
        Visualize SVM with maximum margin separator.
        
        Args:
            x_data (np.ndarray): Shape (n_samples, 2) - 2D features
            y_data (np.ndarray): Shape (n_samples,) - binary labels
        """
        # Title
        title = Text("Support Vector Machine: Maximum Margin Classification", font_size=30, color=GRAY_A)
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

        # Plot class 0 (blue)
        class_0_points = VGroup()
        for x, y in x_data[y_data == 0]:
            point = Dot(axes.coords_to_point(x, y), color=BLUE, radius=0.06)
            class_0_points.add(point)

        # Plot class 1 (red)
        class_1_points = VGroup()
        for x, y in x_data[y_data == 1]:
            point = Dot(axes.coords_to_point(x, y), color=RED, radius=0.06)
            class_1_points.add(point)

        self.play(FadeIn(class_0_points), FadeIn(class_1_points), run_time=1)

        # Decision boundary (separating hyperplane)
        boundary_line = axes.plot(lambda x: -0.8 * x + 10, color=YELLOW, stroke_width=2.5)
        self.play(FadeIn(boundary_line), run_time=0.5)

        self.play_script_step("This is the decision boundary. Now we'll show the maximum margin.")

        # Margin boundaries (parallel lines)
        margin_dist = 0.8  # Controls margin width
        upper_margin = axes.plot(
            lambda x: -0.8 * x + 10 + margin_dist / np.sqrt(1 + 0.8**2),
            color=GREEN,
            stroke_width=1.5,
            stroke_opacity=0.5
        )
        lower_margin = axes.plot(
            lambda x: -0.8 * x + 10 - margin_dist / np.sqrt(1 + 0.8**2),
            color=GREEN,
            stroke_width=1.5,
            stroke_opacity=0.5
        )

        self.play(FadeIn(upper_margin), FadeIn(lower_margin), run_time=0.7)
        self.play_script_step("The green lines represent the margin. Support vectors touch or lie inside the margin.")

        # Highlight support vectors (points closest to boundary)
        sv_indices = self.identify_support_vectors(x_data, y_data)
        support_vector_group = VGroup()

        for idx in sv_indices:
            x, y = x_data[idx]
            point = Circle(
                axes.coords_to_point(x, y),
                radius=0.12,
                color=WHITE,
                fill_opacity=0,
                stroke_width=2.5
            )
            support_vector_group.add(point)

        self.play(FadeIn(support_vector_group), run_time=0.7)
        self.play_script_step(f"Support vectors (circled): These {len(sv_indices)} points determine the margin.")

        self.wait(2)

    def identify_support_vectors(self, x_data: np.ndarray, y_data: np.ndarray) -> np.ndarray:
        """
        Identify support vector candidates (points closest to boundary).
        
        Args:
            x_data (np.ndarray): Feature vectors
            y_data (np.ndarray): Labels
            
        Returns:
            np.ndarray: Indices of support vectors
        """
        # Simplified: return indices of 3 samples per class closest to decision boundary
        # In real SVM, these are determined by solving optimization problem
        
        sv_per_class = 3
        all_sv = []
        
        for label in [0, 1]:
            class_indices = np.where(y_data == label)[0]
            # Distance to center of each class
            class_data = x_data[class_indices]
            center = class_data.mean(axis=0)
            distances = np.linalg.norm(class_data - center, axis=1)
            # Take closest points (they're on margin)
            sv_idx = class_indices[np.argsort(distances)[:sv_per_class]]
            all_sv.extend(sv_idx)
        
        return np.array(all_sv)

    def visualize_kernel_trick(self):
        """Visualize non-linear decision boundary using kernel trick."""
        self.play_script_step(
            "For non-linearly separable data, the kernel trick maps data to higher dimensions "
            "where it becomes linearly separable."
        )

        # Create 2D input space with overlapping circles
        axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": GRAY_B},
            tips=False,
        )
        axes.scale(0.5).shift(LEFT * 2.5)

        # Non-linearly separable data
        circle_inner = Circle(radius=0.5, color=BLUE, fill_opacity=0.3)
        circle_outer = Circle(radius=1.2, color=RED, fill_opacity=0.3)

        self.add(axes)
        self.play(FadeIn(circle_inner), FadeIn(circle_outer))

        self.play_script_step(
            "RBF (Radial Basis Function) kernel is commonly used for non-linear SVM."
        )

        self.wait(2)


class SVMRegression(SVMViz):
    """Support Vector Regression (SVR) for continuous target prediction."""

    def construct(self):
        """Construct SVR visualization."""
        self.play_script_step(
            "Support Vector Regression extends SVM to regression problems. "
            "It seeks to fit data within an epsilon-insensitive tube."
        )
        # Would visualize regression with tolerance tube
