"""
Logistic Regression Visualization - Binary Classification Algorithm

Visualizes logistic regression with decision boundary, sigmoid activation function,
probability outputs, class separation, and loss function (cross-entropy) evolution.

Author: AlgoViz AI
License: MIT
"""

from manim import *
from .base import AlgoVizBaseScene
from typing import Tuple
import numpy as np


class LogisticRegressionViz(AlgoVizBaseScene):
    """
    Logistic Regression Visualization.
    
    Features:
    - 2D scatter plot with two distinct classes (colors)
    - Sigmoid decision boundary visualization
    - Probability shading (heatmap of predicted probabilities)
    - Cross-entropy loss evolution during training
    - Gradient descent optimization for binary classification
    - Classification accuracy and confusion metrics
    - Threshold adjustment visualization (changing decision boundary)
    
    Learning Concepts:
    - Sigmoid activation function: σ(z) = 1 / (1 + e^(-z))
    - Binary cross-entropy loss
    - Decision boundary (logit line in 2D)
    - Probability calibration
    """

    def construct(self):
        """Construct logistic regression visualization with binary classification."""
        self.play_script_step(
            "Logistic Regression predicts probability of binary outcome (0 or 1). "
            "We'll visualize the decision boundary that separates the two classes."
        )

        # Generate synthetic binary classification data
        np.random.seed(42)
        n_samples = 20
        
        # Class 0: centered around (2, 2)
        class_0 = np.random.normal([2, 2], 1.2, (n_samples, 2))
        
        # Class 1: centered around (8, 8)
        class_1 = np.random.normal([8, 8], 1.2, (n_samples, 2))
        
        x_data = np.vstack([class_0, class_1])
        y_data = np.hstack([np.zeros(n_samples), np.ones(n_samples)])

        self.visualize_logistic_regression(x_data, y_data)

    def visualize_logistic_regression(self, x_data: np.ndarray, y_data: np.ndarray):
        """
        Visualize logistic regression with decision boundary.
        
        Args:
            x_data (np.ndarray): Shape (n_samples, 2) - 2D features
            y_data (np.ndarray): Shape (n_samples,) - binary labels (0 or 1)
        """
        # Title
        title = Text("Logistic Regression: Binary Classification", font_size=34, color=GRAY_A)
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

        # Plot class 0 (blue, left side)
        class_0_points = VGroup()
        for i, (x, y) in enumerate(x_data[y_data == 0]):
            point = Dot(axes.coords_to_point(x, y), color=BLUE, radius=0.06)
            class_0_points.add(point)

        # Plot class 1 (red, right side)
        class_1_points = VGroup()
        for i, (x, y) in enumerate(x_data[y_data == 1]):
            point = Dot(axes.coords_to_point(x, y), color=RED, radius=0.06)
            class_1_points.add(point)

        self.play(FadeIn(class_0_points), FadeIn(class_1_points), run_time=1)

        # Initial random decision boundary
        theta = np.array([0.5, 0.5, -3.0])  # weights and bias
        decision_line = self.plot_decision_boundary(axes, theta)
        self.play(FadeIn(decision_line), run_time=0.5)

        # Training visualization
        self.play_script_step("Training logistic regression model to find optimal decision boundary.")

        learning_rate = 0.1
        iterations = 15

        for iteration in range(iterations):
            # Compute predictions using sigmoid
            z = x_data @ theta[:2] + theta[2]
            predictions = 1 / (1 + np.exp(-np.clip(z, -500, 500)))

            # Compute gradients
            errors = predictions - y_data
            gradient = x_data.T @ errors / len(x_data)
            gradient_bias = np.mean(errors)

            # Update parameters
            theta[:2] -= learning_rate * gradient
            theta[2] -= learning_rate * gradient_bias

            # Update boundary every 3 iterations
            if iteration % 3 == 0:
                new_line = self.plot_decision_boundary(axes, theta)
                self.play(Transform(decision_line, new_line), run_time=0.4)

            # Compute and display loss
            loss = -np.mean(y_data * np.log(np.clip(predictions, 1e-15, 1)) + 
                           (1 - y_data) * np.log(np.clip(1 - predictions, 1e-15, 1)))

            if iteration % 5 == 0:
                loss_label = Text(f"Loss: {loss:.3f}", font_size=12, color=YELLOW)
                loss_label.to_edge(DOWN, buff=0.5)
                self.add(loss_label)
                self.wait(0.3)
                self.remove(loss_label)

        # Final result
        accuracy = np.mean((predictions > 0.5) == y_data)
        final_label = Text(f"Final Accuracy: {accuracy:.1%}", font_size=16, color=GREEN)
        final_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(final_label))
        self.wait(1)
        self.play(FadeOut(final_label))

        self.wait(2)

    def plot_decision_boundary(self, axes, theta: np.ndarray) -> VMobject:
        """
        Plot the logistic decision boundary: theta[0]*x + theta[1]*y + theta[2] = 0.5
        
        Args:
            axes: Manim Axes object
            theta (np.ndarray): Model parameters [w1, w2, b]
            
        Returns:
            VMobject: Line representing decision boundary
        """
        # Decision boundary: x range [0, 10]
        # w1*x + w2*y + b = 0.5 logit threshold
        # Solve for y: y = (0.5 - w1*x - b) / w2
        
        w1, w2, b = theta
        if abs(w2) < 0.01:
            w2 = 0.01
        
        boundary_func = lambda x: (0.5 - w1 * x - b) / w2
        
        boundary_line = axes.plot(
            boundary_func,
            x_range=[0, 10],
            color=YELLOW,
            stroke_width=2
        )
        
        return boundary_line

    def visualize_sigmoid(self):
        """Visualize the sigmoid activation function."""
        title = Text("Sigmoid Function: σ(z) = 1 / (1 + e^(-z))", font_size=20, color=GRAY_A)
        title.to_edge(UP)

        axes = Axes(
            x_range=[-6, 6, 2],
            y_range=[0, 1, 0.25],
            axis_config={"color": GRAY_B},
            tips=False,
        )

        sigmoid_curve = axes.plot(
            lambda z: 1 / (1 + np.exp(-z)),
            color=BLUE,
            stroke_width=3
        )

        self.play(FadeIn(title), FadeIn(axes))
        self.play(FadeIn(sigmoid_curve), run_time=1)

        self.play_script_step(
            "The sigmoid function squashes any input to a probability between 0 and 1."
        )

        self.wait(2)
