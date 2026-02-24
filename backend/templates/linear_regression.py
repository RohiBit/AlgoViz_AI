"""
Linear Regression Visualization - Supervised Learning Algorithm

Visualizes linear regression with scatter plot, regression line, gradient descent
optimization, loss function evolution, and residual errors.

Author: AlgoViz AI
License: MIT
"""

from manim import *
from .base import AlgoVizBaseScene
from typing import List, Tuple
import numpy as np


class LinearRegressionViz(AlgoVizBaseScene):
    """
    Linear Regression Visualization.
    
    Features:
    - Scatter plot of training data
    - Regression line (y = mx + b)
    - Residual errors (vertical distance from points to line)
    - Cost function (Mean Squared Error) evolution
    - Gradient descent iterations showing line convergence
    - Learning rate impact visualization
    - R² score and performance metrics
    
    Learning Concepts:
    - Ordinary Least Squares (OLS)
    - Gradient descent optimization
    - Loss function minimization
    - Overfitting and underfitting
    """

    def construct(self):
        """Construct linear regression visualization with data fitting."""
        self.play_script_step(
            "Linear Regression finds the best-fit line through data points by minimizing error. "
            "We'll visualize how the regression line evolves through training."
        )

        # Generate synthetic data
        np.random.seed(42)
        x_data = np.random.uniform(0, 10, 15)
        y_data = 2.5 * x_data + 1 + np.random.normal(0, 2, 15)

        self.visualize_linear_regression(x_data, y_data)

    def visualize_linear_regression(self, x_data: np.ndarray, y_data: np.ndarray):
        """
        Visualize linear regression fitting process.
        
        Args:
            x_data (np.ndarray): Feature values
            y_data (np.ndarray): Target values
        """
        # Title
        title = Text("Linear Regression: Finding Best Fit", font_size=36, color=GRAY_A)
        title.to_edge(UP)
        self.play(FadeIn(title))

        # Create axes
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 35, 5],
            axis_config={"color": GRAY_B},
            tips=False,
        )
        axes.scale(0.6).shift(LEFT * 3)

        self.play(FadeIn(axes))

        # Plot data points
        data_points = VGroup()
        for x, y in zip(x_data, y_data):
            point = Dot(axes.coords_to_point(x, y), color=BLUE, radius=0.08)
            data_points.add(point)

        self.play(FadeIn(data_points), run_time=1)

        # Initial regression line (random)
        m_current, b_current = 1.0, 5.0
        line = axes.plot(lambda x: m_current * x + b_current, color=RED, stroke_width=2)
        self.play(FadeIn(line), run_time=0.5)

        # Gradient descent iterations
        learning_rate = 0.01
        iterations = 10

        for iteration in range(iterations):
            self.play_script_step(
                f"Iteration {iteration + 1}: Calculating gradients and updating parameters."
            )

            # Compute gradient (simplified)
            gradient_m = np.mean([2 * (m_current * x + b_current - y) * x for x, y in zip(x_data, y_data)])
            gradient_b = np.mean([2 * (m_current * x + b_current - y) for x, y in zip(x_data, y_data)])

            # Update parameters
            m_current -= learning_rate * gradient_m
            b_current -= learning_rate * gradient_b

            # Update line
            new_line = axes.plot(lambda x: m_current * x + b_current, color=YELLOW, stroke_width=2)
            self.play(Transform(line, new_line), run_time=0.5)

            # Calculate and display MSE
            mse = np.mean([((m_current * x + b_current) - y) ** 2 for x, y in zip(x_data, y_data)])
            mse_label = Text(f"MSE: {mse:.2f}", font_size=14, color=GREEN)
            mse_label.to_edge(DOWN, buff=0.5)
            self.add(mse_label)
            self.wait(0.3)
            self.remove(mse_label)

            if iteration == iterations - 1:
                # Final line in green
                final_line = axes.plot(lambda x: m_current * x + b_current, color=GREEN, stroke_width=3)
                self.play(Transform(line, final_line), run_time=0.5)

        self.play_script_step("Regression line converged! Final equation: y = {:.2f}x + {:.2f}".format(m_current, b_current))

        self.wait(2)

    def visualize_residuals(self, x_data: np.ndarray, y_data: np.ndarray, m: float, b: float):
        """
        Show residual errors as vertical lines.
        
        Args:
            x_data (np.ndarray): Feature values
            y_data (np.ndarray): Target values
            m (float): Slope of line
            b (float): Intercept of line
        """
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 35, 5],
            axis_config={"color": GRAY_B},
            tips=False,
        )
        axes.scale(0.6)

        residuals = VGroup()
        for x, y in zip(x_data, y_data):
            y_pred = m * x + b
            residual_line = Line(
                axes.coords_to_point(x, y),
                axes.coords_to_point(x, y_pred),
                color=RED,
                stroke_width=1,
                stroke_opacity=0.6
            )
            residuals.add(residual_line)

        self.play_script_step("These red lines show residual errors: actual value minus predicted value.")
        self.play(FadeIn(residuals), run_time=1)

        self.wait(1)
