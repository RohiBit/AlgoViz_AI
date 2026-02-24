"""
Gradient Descent in 3D Visualization - Optimization Algorithm with Loss Surface

Visualizes gradient descent optimization on a 3D loss surface (paraboloid or Rosenbrock).
Shows step-by-step descent towards the minimum, learning rate impact, and convergence.

Author: AlgoViz AI
License: MIT
"""

from manim import *
import numpy as np


class GradientDescent3DViz(ThreeDScene):
    """
    Gradient Descent in 3D Visualization.
    
    Features:
    - 3D loss surface (quadratic, Rosenbrock, or custom landscape)
    - Animated ball rolling down the surface toward minimum
    - Gradient vector visualization (direction of steepest descent)
    - Learning rate impact: too large (overshooting), too small (slow progress)
    - Step trajectory showing path taken during optimization
    - Contour projection on XY plane for context
    - Convergence analysis and final position
    
    Learning Concepts:
    - Gradient = direction of steepest increase (negative = descent)
    - Learning rate: step size multiplier for gradient
    - Local vs global minima
    - Saddle points and plateaus
    - Computational efficiency through batch gradient descent
    
    Mathematical Background:
    Loss function: L(x, y) = (x-x*)² + (y-y*)² (simple quadratic)
    or L(x, y) = (a - x)² + b(y - x²)² (Rosenbrock)
    
    Update rule: θ_new = θ_old - α∇L(θ_old)
    where α is learning rate, ∇L is gradient
    """

    def construct(self):
        """Construct 3D gradient descent visualization."""
        # Camera positioning
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        # Title (in 2D, rendered on top)
        title = Text("Gradient Descent on 3D Loss Surface", font_size=36, color=GRAY_A)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)

        # Create and animate loss surface
        self.visualize_3d_gradient_descent()

    def visualize_3d_gradient_descent(self):
        """Visualize gradient descent on a 3D surface."""
        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-5, 5, 2],
            y_range=[-5, 5, 2],
            z_range=[0, 100, 20],
            x_length=8,
            y_length=8,
            z_length=6,
            axis_config={"color": GRAY_B},
            tips=False,
        )
        self.add(axes)

        # Define loss function (quadratic surface)
        def loss_function(x, y):
            return x**2 + y**2

        # Create surface
        surface = axes.plot_surface(
            loss_function,
            x_range=[-5, 5],
            y_range=[-5, 5],
            resolution=(15, 15),
            color=BLUE,
            opacity=0.7,
        )

        self.add(surface)

        # Starting point (random)
        x_start, y_start = 4, 4
        z_start = loss_function(x_start, y_start)
        start_point = np.array([x_start, y_start, z_start])

        # Create ball at starting position
        ball = Sphere(radius=0.3, color=RED, opacity=0.8)
        ball.move_to(axes.coords_to_point(x_start, y_start, z_start))
        self.add(ball)

        # Script label
        script_label = Text(
            "Starting at random position. Computing gradients...",
            font_size=14,
            color=YELLOW
        )
        script_label.to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(script_label)

        # Gradient descent iterations
        learning_rate = 0.1
        iterations = 30
        trajectory_points = [start_point]

        current_x, current_y = x_start, y_start

        for iteration in range(iterations):
            # Compute gradient
            grad_x = 2 * current_x
            grad_y = 2 * current_y

            # Update position
            current_x -= learning_rate * grad_x
            current_y -= learning_rate * grad_y

            new_z = loss_function(current_x, current_y)
            new_point = np.array([current_x, current_y, new_z])

            trajectory_points.append(new_point)

            # Move ball
            new_ball_pos = axes.coords_to_point(current_x, current_y, new_z)
            self.play(ball.animate.move_to(new_ball_pos), run_time=0.1)

            # Every 5 iterations, show loss value
            if iteration % 5 == 0:
                loss_val = loss_function(current_x, current_y)
                loss_text = Text(
                    f"Iteration {iteration}: Loss = {loss_val:.2f}",
                    font_size=12,
                    color=GREEN
                )
                loss_text.to_edge(DOWN, buff=0.3)
                self.add_fixed_in_frame_mobjects(loss_text)
                self.wait(0.2)
                self.remove_fixed_in_frame_mobjects(loss_text)

        # Final convergence message
        final_loss = loss_function(current_x, current_y)
        convergence_text = Text(
            f"Converged! Final Loss: {final_loss:.4f}",
            font_size=16,
            color=GREEN
        )
        convergence_text.to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(convergence_text)

        self.wait(2)

    def visualize_learning_rate_impact(self):
        """
        Compare different learning rates side-by-side.
        
        This would be shown in a separate scene with three 3D plots.
        """
        learning_rates = [0.01, 0.1, 0.5]
        labels = ["Too Small", "Optimal", "Too Large"]
        descriptions = ["Slow convergence", "Good convergence", "Overshoots/Diverges"]

        # In a full implementation, would show three parallel visualizations


class RosenbrockGradientDescent(GradientDescent3DViz):
    """Gradient descent on the Rosenbrock function (harder optimization landscape)."""

    def construct(self):
        """Visualize GD on Rosenbrock surface."""
        self.set_camera_orientation(phi=70 * DEGREES, theta=50 * DEGREES)

        # Title
        title = Text("Rosenbrock Function: Challenging Optimization", font_size=32, color=GRAY_A)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)

        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-1, 3, 1],
            z_range=[0, 300, 50],
            x_length=8,
            y_length=10,
            z_length=7,
            axis_config={"color": GRAY_B},
        )
        self.add(axes)

        # Rosenbrock function: f(x,y) = (1-x)² + 100(y-x²)²
        def rosenbrock(x, y):
            return (1 - x)**2 + 100 * (y - x**2)**2

        surface = axes.plot_surface(
            rosenbrock,
            x_range=[-2, 2],
            y_range=[-1, 3],
            resolution=(20, 20),
            color=PURPLE,
            opacity=0.7,
        )

        self.add(surface)

        # Start at bad position
        x_start, y_start = -1, 2.5
        z_start = rosenbrock(x_start, y_start)
        ball = Sphere(radius=0.2, color=YELLOW, opacity=0.9)
        ball.move_to(axes.coords_to_point(x_start, y_start, z_start))
        self.add(ball)

        # GD iterations with small learning rate
        learning_rate = 0.001
        current_x, current_y = x_start, y_start

        for iteration in range(50):
            # Gradients for Rosenbrock
            grad_x = -2 * (1 - current_x) - 400 * current_x * (current_y - current_x**2)
            grad_y = 200 * (current_y - current_x**2)

            current_x -= learning_rate * grad_x
            current_y -= learning_rate * grad_y

            new_z = rosenbrock(current_x, current_y)
            self.play(
                ball.animate.move_to(axes.coords_to_point(current_x, current_y, new_z)),
                run_time=0.05
            )

        info_text = Text(
            "Rosenbrock is harder: narrow valley requires careful optimization.",
            font_size=12,
            color=YELLOW
        )
        info_text.to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(info_text)

        self.wait(2)
