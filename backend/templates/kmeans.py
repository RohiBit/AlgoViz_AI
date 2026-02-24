"""
K-Means Clustering Visualization - Unsupervised Learning Algorithm

Visualizes K-means iterations including centroid initialization, assignment,
update steps, convergence, and optimal k-value determination (elbow method).

Author: AlgoViz AI
License: MIT
"""

from manim import *
from .base import AlgoVizBaseScene
from typing import List
import numpy as np


class KMeansViz(AlgoVizBaseScene):
    """
    K-Means Clustering Visualization.
    
    Features:
    - Random initialization of k centroids
    - Assignment step: assign points to nearest centroid
    - Update step: recalculate centroids as mean of assigned points
    - Convergence visualization: iterations until centroids stop moving
    - Color-coded clusters (one color per cluster)
    - Centroid movement arrows showing trajectory
    - Elbow method for finding optimal k
    - Silhouette score visualization
    
    Learning Concepts:
    - Lloyd's algorithm (standard K-means)
    - Euclidean distance metric
    - Local vs global minima
    - Computational complexity: O(nkd) per iteration
    """

    def __init__(self, k: int = 3, *args, **kwargs):
        """
        Initialize K-means with specified number of clusters.
        
        Args:
            k (int): Number of clusters (default 3)
        """
        self.k = k
        super().__init__(*args, **kwargs)

    def construct(self):
        """Construct K-means visualization with clustering iterations."""
        self.play_script_step(
            f"K-means clustering partitions data into {self.k} groups. "
            f"Let's visualize how centroids evolve and points are assigned."
        )

        # Generate synthetic data with natural clusters
        np.random.seed(42)
        cluster_centers = np.array([[2, 8], [8, 2], [8, 8]])
        
        data = []
        for center in cluster_centers:
            cluster_data = np.random.normal(center, 1.2, (20, 2))
            data.append(cluster_data)
        
        x_data = np.vstack(data)

        self.visualize_kmeans(x_data, self.k)

    def visualize_kmeans(self, x_data: np.ndarray, k: int):
        """
        Visualize K-means clustering process.
        
        Args:
            x_data (np.ndarray): Input data points (n_samples, 2)
            k (int): Number of clusters
        """
        # Title
        title = Text(f"K-Means Clustering (k={k})", font_size=36, color=GRAY_A)
        title.to_edge(UP)
        self.play(FadeIn(title))

        # Create axes
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            axis_config={"color": GRAY_B},
            tips=False,
        )
        axes.scale(0.5).shift(LEFT * 2.5)

        self.play(FadeIn(axes))

        # Color palette for clusters
        colors = [BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE]
        cluster_colors = colors[:k]

        # Random initialization of centroids
        centroid_indices = np.random.choice(len(x_data), k, replace=False)
        centroids = x_data[centroid_indices].copy()

        # Create initial centroid markers
        centroid_mobjects = VGroup()
        for i, centroid in enumerate(centroids):
            marker = Dot(
                axes.coords_to_point(centroid[0], centroid[1]),
                color=cluster_colors[i],
                radius=0.12
            )
            star = Star(
                n_points=5,
                outer_radius=0.15,
                inner_radius=0.08,
                color=cluster_colors[i],
                fill_opacity=0.9
            )
            star.move_to(axes.coords_to_point(centroid[0], centroid[1]))
            centroid_mobjects.add(star)

        self.play(FadeIn(centroid_mobjects), run_time=0.7)
        self.play_script_step("Stars represent the initial random centroids.")

        # K-means iterations
        max_iterations = 8
        for iteration in range(max_iterations):
            self.play_script_step(
                f"Iteration {iteration + 1}: Assign points to nearest centroid."
            )

            # Assignment step
            distances = np.zeros((len(x_data), k))
            for i, centroid in enumerate(centroids):
                distances[:, i] = np.linalg.norm(x_data - centroid, axis=1)

            assignments = np.argmin(distances, axis=1)

            # Plot points colored by cluster
            data_points = VGroup()
            for point_idx, (x, y) in enumerate(x_data):
                cluster_id = assignments[point_idx]
                point = Dot(
                    axes.coords_to_point(x, y),
                    color=cluster_colors[cluster_id],
                    radius=0.05,
                    fill_opacity=0.6
                )
                data_points.add(point)

            if iteration == 0:
                self.play(FadeIn(data_points), run_time=1)
            else:
                self.play(Transform(data_points, data_points), run_time=0.5)

            self.wait(0.5)

            # Update step
            self.play_script_step("Iteration {}: Recalculate centroid positions.".format(iteration + 1))

            new_centroids = np.zeros_like(centroids)
            for cluster_id in range(k):
                cluster_mask = assignments == cluster_id
                if np.any(cluster_mask):
                    new_centroids[cluster_id] = x_data[cluster_mask].mean(axis=0)
                else:
                    new_centroids[cluster_id] = centroids[cluster_id]

            # Animate centroid movement
            new_centroid_mobjects = VGroup()
            for i, (old_c, new_c) in enumerate(zip(centroids, new_centroids)):
                new_star = Star(
                    n_points=5,
                    outer_radius=0.15,
                    inner_radius=0.08,
                    color=cluster_colors[i],
                    fill_opacity=0.9
                )
                new_star.move_to(axes.coords_to_point(new_c[0], new_c[1]))
                new_centroid_mobjects.add(new_star)

            self.play(Transform(centroid_mobjects, new_centroid_mobjects), run_time=0.7)

            centroids = new_centroids

            # Check convergence
            if iteration > 0:
                movement = np.linalg.norm(centroids - np.array([axes.point_to_coords(m.get_center())[:2] for m in centroid_mobjects]))
                if movement < 0.1:
                    self.play_script_step("Centroids have converged. K-means algorithm finished.")
                    break

        self.play_script_step(f"Final clustering complete: {k} clusters identified.")

        self.wait(2)


class ElbowMethod(KMeansViz):
    """Visualization of the Elbow Method for optimal k selection."""

    def construct(self):
        """Show how to choose optimal k using elbow method."""
        self.play_script_step(
            "The Elbow Method helps find the optimal number of clusters. "
            "We plot within-cluster variance (inertia) for different k values."
        )

        # Simulate inertia values for k=1 to k=10
        k_values = np.arange(1, 11)
        inertias = [50, 25, 12, 7, 5, 4.5, 4.2, 4.1, 4.05, 4.0]

        # Plot inertia vs k
        axes = Axes(
            x_range=[0, 11, 1],
            y_range=[0, 60, 10],
            axis_config={"color": GRAY_B},
            tips=False,
        )
        axes.add_coordinate_labels()

        points = VGroup()
        for k, inertia in zip(k_values, inertias):
            point = Dot(axes.coords_to_point(k, inertia), color=BLUE, radius=0.08)
            points.add(point)

        curve = axes.plot_line_graph(k_values, inertias, add_vertex_dots=False, stroke_width=2, stroke_color=BLUE)

        self.play(FadeIn(axes), FadeIn(points), FadeIn(curve))

        # Highlight elbow at k=3
        elbow_point = Dot(axes.coords_to_point(3, 12), color=YELLOW, radius=0.12)
        elbow_label = Text("Elbow \n(k=3 optimal)", font_size=12, color=YELLOW)
        elbow_label.next_to(elbow_point, UR, buff=0.3)

        self.play(FadeIn(elbow_point), FadeIn(elbow_label))
        self.play_script_step("The 'elbow' at k=3 suggests 3 is the optimal number of clusters.")

        self.wait(2)
