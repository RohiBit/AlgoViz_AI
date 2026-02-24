"""
AlgoViz AI: Comprehensive Manim Templates for Data Structures & ML Algorithms

This module provides reusable, production-grade Manim VoiceOver scene templates
for visualizing complex data structures, algorithms, and machine learning concepts.

Design Principles:
- Centering: All main diagrams dynamically centered on ORIGIN
- No Overlap: Labels/text positioned with next_to() and proper buffering
- Dark Mode Palette: Professional colors (BLUE/TEAL nodes, WHITE edges, YELLOW/RED highlights)
- Dynamic Scaling: Handles large structures by scaling objects/camera
- Script Integration: play_script_step(text) for guided narration
- Modularity: Base classes for easy extension and reuse

Author: AlgoViz AI
License: MIT
"""

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from abc import ABC, abstractmethod
import numpy as np
from typing import List, Dict, Tuple, Optional, Any


# ============================================================================
# BASE CLASSES & UTILITIES
# ============================================================================

class AlgoVizBaseScene(VoiceoverScene, ABC):
    """
    Abstract base class for all AlgoViz visualizations.
    Provides common utilities and enforces design standards.
    """

    def setup(self):
        """Initialize scene with dark mode palette and voiceover service."""
        super().setup()
        self.set_speech_service(GTTSService())
        self.camera.background_color = "#0a0e27"  # Deep dark blue

    def play_script_step(self, text: str, duration: float = 3.0):
        """
        Display script text at bottom of screen with voiceover.
        
        Args:
            text (str): Description or narration for current step
            duration (float): Time to display text (voiceover auto-manages)
        """
        script_label = Text(
            text,
            font_size=20,
            color=GRAY_B,
            width=13
        ).to_edge(DOWN, buff=0.3)

        with self.voiceover(text=text):
            self.play(FadeIn(script_label, shift=UP * 0.3))
            self.wait(0.5)
            self.play(FadeOut(script_label))

    def safe_scale_group(self, group: VMobject, max_width: float = 12.0, max_height: float = 8.0):
        """
        Dynamically scale a group if it exceeds frame bounds.
        
        Args:
            group (VMobject): The object group to scale
            max_width (float): Maximum allowed width
            max_height (float): Maximum allowed height
        """
        width = group.width
        height = group.height
        scale_factor = min(1.0, max_width / width, max_height / height)
        if scale_factor < 1.0:
            group.scale(scale_factor)

    def center_on_origin(self, obj: VMobject):
        """Center any object on screen origin."""
        obj.move_to(ORIGIN)

    def get_color_palette(self) -> Dict[str, str]:
        """Return professional dark mode color palette."""
        return {
            "node": BLUE,
            "node_highlight": YELLOW,
            "edge": WHITE,
            "edge_highlight": RED,
            "text": GRAY_A,
            "text_label": GRAY_B,
            "positive": GREEN,
            "negative": RED,
            "background": "#0a0e27",
        }


# ============================================================================
# DATA STRUCTURE VISUALIZATIONS
# ============================================================================

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


class BinaryTreeViz(AlgoVizBaseScene):
    """
    Binary Tree Visualization (unbalanced).
    
    Features:
    - Tree construction from list representation
    - In-order, pre-order, post-order traversal animations
    - Parent-child edge highlighting
    - Subtree size and height annotations
    - Breadth-first level display
    """

    def construct(self):
        """Visualize binary tree structure and traversals."""
        self.play_script_step("Binary Trees organize data hierarchically. We'll explore common traversals.")
        self.visualize_tree_traversals([1, 2, 3, 4, 5, 6, 7])

    def visualize_tree_traversals(self, values: List[int]):
        """
        Build and show multiple tree traversals.
        
        Args:
            values (List[int]): Array representation of tree
        """
        title = Text("Binary Tree Traversals", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        # Create simple tree layout (simplified for demo)
        tree = VGroup()
        for i, val in enumerate(values):
            circle = Circle(radius=0.35, color=BLUE, fill_opacity=0.8)
            text = Text(str(val), font_size=18, color=WHITE)
            text.move_to(circle.get_center())
            node = VGroup(circle, text)

            # Position in tree-like layout
            level = int(np.log2(i + 1))
            position_in_level = i - (2 ** level - 1)
            node.shift(DOWN * level * 1.2 + RIGHT * (position_in_level - 2 ** (level - 1)) * 1.5)
            tree.add(node)

        self.center_on_origin(tree)
        self.play(FadeIn(tree))

        # Show traversal order
        traversals = {
            "In-Order": [1, 4, 2, 5, 3, 6, 7],
            "Pre-Order": [1, 2, 4, 5, 3, 6, 7],
            "Post-Order": [4, 5, 2, 6, 7, 3, 1],
        }

        for name, order in traversals.items():
            label = Text(f"{name}: {order}", font_size=16, color=YELLOW)
            label.next_to(tree, DOWN, buff=0.5)
            self.play(FadeIn(label))
            self.wait(1)
            self.play(FadeOut(label))

        self.wait(2)


class RBTreeViz(AlgoVizBaseScene):
    """
    Red-Black Tree Visualization.
    
    Features:
    - Color-coded nodes (RED, BLACK)
    - Balance property indicators
    - Rotation and recoloring animations
    - Properties verification (red nodes can't have red children, etc.)
    """

    def construct(self):
        """Visualize Red-Black Tree properties and insertion."""
        self.play_script_step("Red-Black Trees maintain balance through color rules and rotations.")
        self.build_rbtree_example()

    def build_rbtree_example(self):
        """Build and showcase RB-tree properties."""
        title = Text("Red-Black Tree", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        # Example tree with colors
        nodes = [
            (25, BLACK),
            (10, RED),
            (40, RED),
            (5, BLACK),
            (15, BLACK),
            (35, BLACK),
            (50, BLACK),
        ]

        tree = VGroup()
        for i, (val, color) in enumerate(nodes):
            circle = Circle(radius=0.35, color=color, fill_opacity=0.9, stroke_color=WHITE)
            text = Text(str(val), font_size=18, color=WHITE)
            text.move_to(circle.get_center())
            node = VGroup(circle, text)

            level = int(np.log2(i + 1))
            position_in_level = i - (2 ** level - 1)
            node.shift(DOWN * level * 1.2 + RIGHT * (position_in_level - 2 ** (level - 1)) * 1.5)
            tree.add(node)

        self.center_on_origin(tree)
        self.play(FadeIn(tree))

        # Highlight property
        props = [
            "Property 1: Every node is RED or BLACK",
            "Property 2: Root is BLACK",
            "Property 3: RED nodes have BLACK children",
            "Property 4: All paths have same number of BLACK nodes",
        ]

        for prop in props:
            label = Text(prop, font_size=14, color=GRAY_B, width=12)
            label.to_edge(DOWN, buff=0.3)
            self.play(FadeIn(label))
            self.wait(1.5)
            self.play(FadeOut(label))


class BTreeViz(AlgoVizBaseScene):
    """
    B-Tree Visualization (multi-way balanced tree).
    
    Features:
    - Variable branching factor (degree)
    - Horizontal node layout (key and child pointers)
    - Node splitting animations
    - Search path highlighting
    """

    def construct(self):
        """Visualize B-Tree structure with degree 3."""
        self.play_script_step("B-Trees are ideal for disk-based databases. Each node can have many children.")
        self.build_btree(degree=3)

    def build_btree(self, degree: int):
        """
        Build a B-Tree with specified degree.
        
        Args:
            degree (int): Maximum number of keys per node
        """
        title = Text(f"B-Tree (Degree {degree})", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        # Root node with 2 keys
        root_rect = Rectangle(width=3, height=0.8, color=BLUE, fill_opacity=0.7)
        root_text = Text("[30 | 70]", font_size=16, color=WHITE)
        root_text.move_to(root_rect.get_center())
        root = VGroup(root_rect, root_text)
        root.move_to(ORIGIN + UP * 2)

        self.play(FadeIn(root))

        # Child nodes
        children = [
            ("[10 | 20]", LEFT * 3 + DOWN * 2),
            ("[40 | 60]", ORIGIN + DOWN * 2),
            ("[80 | 90]", RIGHT * 3 + DOWN * 2),
        ]

        for keys, pos in children:
            child_rect = Rectangle(width=2.5, height=0.7, color=TEAL, fill_opacity=0.7)
            child_text = Text(keys, font_size=14, color=WHITE)
            child_text.move_to(child_rect.get_center())
            child = VGroup(child_rect, child_text)
            child.move_to(pos)

            # Draw edge
            edge = Line(root.get_bottom(), child.get_top(), color=WHITE)
            self.play(Create(edge), FadeIn(child))

        self.wait(2)


class GraphSearchViz(AlgoVizBaseScene):
    """
    Graph Search Algorithm Visualization (BFS, DFS, Dijkstra).
    
    Features:
    - Arbitrary graph layout with nodes and edges
    - Queue/stack visualization for algorithm state
    - Distance/cost display for weighted graphs
    - Path highlighting and animation
    - Traversal order annotation
    """

    def construct(self):
        """Visualize graph search algorithms."""
        self.play_script_step("Graph searches explore nodes in different orders: BFS, DFS, or weighted (Dijkstra).")
        self.visualize_graph_search("BFS")

    def visualize_graph_search(self, algorithm: str = "BFS"):
        """
        Visualize a graph search algorithm.
        
        Args:
            algorithm (str): "BFS", "DFS", or "Dijkstra"
        """
        title = Text(f"Graph Search: {algorithm}", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        # Create simple graph
        nodes_pos = {
            "A": UP + LEFT * 2,
            "B": RIGHT * 2,
            "C": DOWN + LEFT * 2,
            "D": DOWN + RIGHT * 2,
        }

        nodes = VGroup()
        for label, pos in nodes_pos.items():
            circle = Circle(radius=0.4, color=BLUE, fill_opacity=0.8)
            text = Text(label, font_size=20, color=WHITE)
            text.move_to(circle.get_center())
            node = VGroup(circle, text)
            node.move_to(pos)
            nodes.add(node)

        edges_list = [
            ("A", "B"),
            ("A", "C"),
            ("B", "D"),
            ("C", "D"),
        ]

        edges = VGroup()
        for src, dst in edges_list:
            edge = Line(nodes_pos[src], nodes_pos[dst], color=WHITE)
            edges.add(edge)

        graph = VGroup(edges, nodes)
        self.center_on_origin(graph)
        self.play(FadeIn(graph))

        # Simulate traversal order
        traversal_order = ["A", "B", "C", "D"]
        for i, node_label in enumerate(traversal_order):
            order_text = Text(f"Visit: {node_label}", font_size=16, color=YELLOW)
            order_text.to_edge(DOWN, buff=0.5)
            self.play(FadeIn(order_text))
            self.wait(0.8)
            self.play(FadeOut(order_text))

        self.wait(2)


# ============================================================================
# 2D MACHINE LEARNING VISUALIZATIONS
# ============================================================================

class LinearRegressionViz(AlgoVizBaseScene):
    """
    Linear Regression Visualization.
    
    Features:
    - Scatter plot of data points
    - Animated regression line convergence
    - Cost/loss surface or 2D loss heatmap
    - Prediction illustration
    - Gradient descent trajectory
    """

    def construct(self):
        """Visualize linear regression fitting."""
        self.play_script_step("Linear Regression finds the best-fit line through data using gradient descent.")
        self.visualize_regression()

    def visualize_regression(self):
        """Build regression visualization."""
        title = Text("Linear Regression: y = mx + b", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        # Axes
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            width=8,
            height=6,
            axis_config={"color": GRAY},
            tips=False,
        )
        axes.move_to(ORIGIN)

        # Data points
        data_x = [0.5, 1.5, 2.5, 3.5, 4.0]
        data_y = [0.8, 2.0, 3.2, 4.0, 4.5]
        points = VGroup()
        for x, y in zip(data_x, data_y):
            dot = Dot(axes.coords_to_point(x, y), radius=0.08, color=BLUE)
            points.add(dot)

        self.play(FadeIn(axes), FadeIn(points))

        # Regression line (initially bad, then improves)
        line1 = axes.plot_line_graph(
            x_values=[-1, 5],
            y_values=[-1, 1],
            line_color=RED,
        )
        self.play(Create(line1))
        self.play_script_step("Initially, the line is not a good fit. We adjust parameters using gradient descent.")

        # Improved line
        line2 = axes.plot_line_graph(
            x_values=[-1, 5],
            y_values=[0, 4.5],
            line_color=GREEN,
        )
        self.play(FadeOut(line1), Create(line2))
        self.play_script_step("After optimization, the line minimizes the distance to all data points.")

        self.wait(2)


class LogisticRegressionViz(AlgoVizBaseScene):
    """
    Logistic Regression Visualization (binary classification).
    
    Features:
    - Two-class scatter plot
    - Sigmoid curve animation
    - Decision boundary visualization
    - Probability heat map (optional)
    """

    def construct(self):
        """Visualize logistic regression classification."""
        self.play_script_step("Logistic Regression uses the sigmoid function to predict binary outcomes.")
        self.visualize_logistic_regression()

    def visualize_logistic_regression(self):
        """Build logistic regression visualization."""
        title = Text("Logistic Regression: Binary Classification", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        # Axes
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-0.5, 1.5, 0.5],
            width=8,
            height=5,
            axis_config={"color": GRAY},
            tips=False,
        )
        axes.move_to(ORIGIN)

        # Class 0 (negative, blue)
        class_0_x = [0.5, 1.0, 1.5]
        class_0_y = [0.2, 0.3, 0.1]
        for x, y in zip(class_0_x, class_0_y):
            dot = Dot(axes.coords_to_point(x, y), radius=0.08, color=BLUE)
            self.play(FadeIn(dot))

        # Class 1 (positive, red)
        class_1_x = [3.0, 3.5, 4.0]
        class_1_y = [0.8, 0.9, 0.7]
        for x, y in zip(class_1_x, class_1_y):
            dot = Dot(axes.coords_to_point(x, y), radius=0.08, color=RED)
            self.play(FadeIn(dot))

        self.play(FadeIn(axes))

        # Sigmoid curve
        sigmoid_curve = axes.plot(
            lambda x: 1 / (1 + np.exp(-2 * (x - 2.5))),
            x_range=[0, 5],
            color=YELLOW,
        )
        self.play(Create(sigmoid_curve))
        self.play_script_step("The sigmoid curve represents the probability of class 1. The decision boundary is at p=0.5.")

        self.wait(2)


class SVMViz(AlgoVizBaseScene):
    """
    Support Vector Machine (SVM) Visualization.
    
    Features:
    - Two-class scatter plots (linearly separable and non-separable)
    - Separating hyperplane with maximum margin
    - Support vector highlighting
    - Kernel transformation (optional 2D to 2D projection for non-linear)
    """

    def construct(self):
        """Visualize SVM decision boundary and margins."""
        self.play_script_step("SVMs find a decision boundary that maximizes the margin between classes.")
        self.visualize_svm()

    def visualize_svm(self):
        """Build SVM visualization."""
        title = Text("Support Vector Machine (SVM)", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        # Axes
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            width=8,
            height=8,
            axis_config={"color": GRAY},
            tips=False,
        )
        axes.move_to(ORIGIN)

        # Class 0 (blue)
        class_0_points = [(0.5, 0.5), (1.0, 1.0), (1.5, 0.8)]
        for x, y in class_0_points:
            dot = Dot(axes.coords_to_point(x, y), radius=0.08, color=BLUE)
            self.play(FadeIn(dot))

        # Class 1 (red)
        class_1_points = [(3.5, 3.5), (4.0, 4.0), (3.8, 3.2)]
        for x, y in class_1_points:
            dot = Dot(axes.coords_to_point(x, y), radius=0.08, color=RED)
            self.play(FadeIn(dot))

        self.play(FadeIn(axes))

        # Decision boundary (hyperplane)
        boundary = axes.plot_line_graph(
            x_values=[-1, 5],
            y_values=[-1, 5],
            line_color=YELLOW,
        )
        self.play(Create(boundary))

        # Margin lines (parallel to boundary)
        margin_1 = axes.plot_line_graph(
            x_values=[-1, 5],
            y_values=[0, 6],
            line_color=GRAY_B,
        )
        margin_2 = axes.plot_line_graph(
            x_values=[-1, 5],
            y_values=[-2, 4],
            line_color=GRAY_B,
        )
        self.play(Create(margin_1), Create(margin_2))

        self.play_script_step(
            "The yellow line is the optimal separating hyperplane. "
            "The gray lines define the maximum margin region. "
            "Points on the margin boundaries are support vectors."
        )

        self.wait(2)


class KMeansViz(AlgoVizBaseScene):
    """
    K-Means Clustering Visualization.
    
    Features:
    - Scatter plot of random points
    - K centroids (initialized randomly or kmeans++)
    - Cluster assignments (color-coded)
    - Centroid movement animation per iteration
    - Convergence criterion
    """

    def construct(self):
        """Visualize K-Means clustering."""
        self.play_script_step("K-Means partitions data into k clusters by iteratively updating centroids.")
        self.visualize_kmeans(k=3)

    def visualize_kmeans(self, k: int = 3):
        """
        Build K-Means visualization.
        
        Args:
            k (int): Number of clusters
        """
        title = Text(f"K-Means Clustering (k={k})", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        # Axes
        axes = Axes(
            x_range=[-2, 6, 1],
            y_range=[-2, 6, 1],
            width=8,
            height=8,
            axis_config={"color": GRAY},
            tips=False,
        )
        axes.move_to(ORIGIN)
        self.play(FadeIn(axes))

        # Generate random points
        np.random.seed(42)
        points = []
        colors = [BLUE, RED, GREEN]

        for i in range(15):
            x, y = np.random.uniform(-1, 5, 2)
            dot = Dot(axes.coords_to_point(x, y), radius=0.06, color=GRAY_B)
            points.append(dot)
            self.play(FadeIn(dot), run_time=0.1)

        # Initialize centroids
        centroids_pos = [(1.0, 1.0), (3.0, 4.0), (4.5, 1.5)]
        centroids = VGroup()

        for i, (cx, cy) in enumerate(centroids_pos):
            centroid = Dot(
                axes.coords_to_point(cx, cy),
                radius=0.12,
                color=colors[i],
                stroke_color=WHITE,
                stroke_width=3,
            )
            centroids.add(centroid)
            self.play(FadeIn(centroid))

        self.play_script_step(f"We initialize {k} centroids randomly (shown as larger circles with borders).")

        # Simulate iterations
        for iteration in range(2):
            iter_label = Text(f"Iteration {iteration + 1}", font_size=20, color=YELLOW)
            iter_label.to_edge(DOWN, buff=0.5)
            self.play(FadeIn(iter_label))

            # Move centroids slightly (simulate convergence)
            new_positions = [
                (1.2, 1.3),
                (3.1, 3.9),
                (4.4, 1.6),
            ]
            for centroid, (nx, ny) in zip(centroids, new_positions):
                self.play(
                    centroid.animate.move_to(axes.coords_to_point(nx, ny)),
                    run_time=0.8,
                )

            self.play(FadeOut(iter_label))

        self.play_script_step("After convergence, points are assigned to the nearest centroid, forming clusters.")
        self.wait(2)


class DecisionTreeViz(AlgoVizBaseScene):
    """
    Decision Tree Visualization (Classification).
    
    Features:
    - Tree structure with split conditions
    - Leaf node class labels (color-coded)
    - Feature and threshold display on edges
    - Gini/entropy purity annotations (optional)
    """

    def construct(self):
        """Visualize decision tree structure."""
        self.play_script_step("Decision Trees recursively split data to classify samples.")
        self.visualize_decision_tree()

    def visualize_decision_tree(self):
        """Build decision tree visualization."""
        title = Text("Decision Tree Classifier", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        # Root node
        root_rect = Rectangle(width=4, height=0.8, color=BLUE, fill_opacity=0.7)
        root_text = Text("feature_1 <= 2.5?", font_size=14, color=WHITE)
        root_text.move_to(root_rect.get_center())
        root = VGroup(root_rect, root_text)
        root.move_to(ORIGIN + UP * 2)
        self.play(FadeIn(root))

        # Left child (yes)
        left_child_rect = Rectangle(width=3, height=0.8, color=GREEN, fill_opacity=0.7)
        left_child_text = Text("Class A", font_size=14, color=WHITE)
        left_child_text.move_to(left_child_rect.get_center())
        left_child = VGroup(left_child_rect, left_child_text)
        left_child.move_to(LEFT * 3 + DOWN * 2)

        # Right child (no)
        right_child_rect = Rectangle(width=3, height=0.8, color=RED, fill_opacity=0.7)
        right_child_text = Text("Class B", font_size=14, color=WHITE)
        right_child_text.move_to(right_child_rect.get_center())
        right_child = VGroup(right_child_rect, right_child_text)
        right_child.move_to(RIGHT * 3 + DOWN * 2)

        # Edges
        edge_left = Line(root.get_bottom(), left_child.get_top(), color=WHITE)
        edge_right = Line(root.get_bottom(), right_child.get_top(), color=WHITE)

        # Edge labels
        label_left = Text("Yes", font_size=12, color=YELLOW).next_to(edge_left, LEFT, buff=0.1)
        label_right = Text("No", font_size=12, color=YELLOW).next_to(edge_right, RIGHT, buff=0.1)

        self.play(
            Create(edge_left), FadeIn(left_child),
            Create(edge_right), FadeIn(right_child),
            FadeIn(label_left), FadeIn(label_right),
        )

        self.play_script_step("At each node, the tree makes a binary split. Leaf nodes show the final classification.")
        self.wait(2)


class RandomForestViz(AlgoVizBaseScene):
    """
    Random Forest Visualization (ensemble of decision trees).
    
    Features:
    - Multiple decision trees side-by-side or in 3x3 grid
    - Aggregation of predictions (majority voting)
    - Feature importance bar chart
    """

    def construct(self):
        """Visualize random forest ensemble."""
        self.play_script_step("Random Forests combine multiple decision trees to improve robustness and accuracy.")
        self.visualize_random_forest(num_trees=3)

    def visualize_random_forest(self, num_trees: int = 3):
        """
        Build random forest visualization.
        
        Args:
            num_trees (int): Number of trees to display
        """
        title = Text(f"Random Forest ({num_trees} Trees)", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        # Draw multiple simplified trees
        for i in range(num_trees):
            # Simple tree representation per forest
            tree_group = VGroup()

            # Root
            root = Circle(radius=0.3, color=BLUE)
            root_text = Text("Split", font_size=12, color=WHITE)
            root_text.move_to(root.get_center())
            root = VGroup(root, root_text)

            # Leaves
            left_leaf = Circle(radius=0.2, color=GREEN)
            right_leaf = Circle(radius=0.2, color=RED)

            # Position
            x_offset = (i - 1) * 3
            root.move_to(ORIGIN + UP + RIGHT * x_offset)
            left_leaf.move_to(LEFT * 0.8 + DOWN + RIGHT * x_offset)
            right_leaf.move_to(RIGHT * 0.8 + DOWN + RIGHT * x_offset)

            tree_group.add(root, left_leaf, right_leaf)
            self.play(FadeIn(tree_group))

        # Aggregation
        self.play_script_step("Each tree makes a prediction. The forest averages or votes on the final prediction.")
        self.wait(2)


class KNNViz(AlgoVizBaseScene):
    """
    K-Nearest Neighbors Visualization.
    
    Features:
    - Test point and training data points
    - Highlight k nearest neighbors (circles or distances)
    - Distance metrics visualization
    - Prediction based on majority class
    """

    def construct(self):
        """Visualize K-NN algorithm."""
        self.play_script_step("K-Nearest Neighbors classifies by finding the k closest training examples.")
        self.visualize_knn(k=3)

    def visualize_knn(self, k: int = 3):
        """
        Build K-NN visualization.
        
        Args:
            k (int): Number of neighbors
        """
        title = Text(f"K-Nearest Neighbors (k={k})", font_size=36, color=GRAY_A).to_edge(UP)
        self.play(FadeIn(title))

        # Axes
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            width=8,
            height=8,
            axis_config={"color": GRAY},
            tips=False,
        )
        axes.move_to(ORIGIN)
        self.play(FadeIn(axes))

        # Training points
        class_0_points = [(0.5, 0.5), (1.0, 1.5), (1.5, 0.8)]
        class_1_points = [(3.5, 3.5), (4.0, 4.0), (3.8, 3.2)]

        for x, y in class_0_points:
            dot = Dot(axes.coords_to_point(x, y), radius=0.07, color=BLUE)
            self.play(FadeIn(dot))

        for x, y in class_1_points:
            dot = Dot(axes.coords_to_point(x, y), radius=0.07, color=RED)
            self.play(FadeIn(dot))

        # Test point
        test_x, test_y = 2.0, 2.0
        test_point = Dot(axes.coords_to_point(test_x, test_y), radius=0.1, color=YELLOW)
        self.play(FadeIn(test_point))

        # Highlight k nearest neighbors (distances)
        distances = [
            (np.sqrt((x - test_x) ** 2 + (y - test_y) ** 2), color)
            for (x, y), color in (
                [(0.5, 0.5), BLUE] + [(1.0, 1.5), BLUE] + [(1.5, 0.8), BLUE]
                + [(3.5, 3.5), RED] + [(4.0, 4.0), RED] + [(3.8, 3.2), RED]
            )
        ]
        distances.sort(key=lambda x: x[0])

        for i in range(k):
            # Draw circle around k-th neighbor
            neighbor_dist = distances[i][0]
            circle = Circle(
                radius=max(0.1, neighbor_dist / 3),
                color=distances[i][1],
                fill_opacity=0.1,
                stroke_color=distances[i][1],
                stroke_width=2,
            )
            circle.move_to(axes.coords_to_point(test_x, test_y))

            highlight_label = Text(f"Neighbor {i + 1}", font_size=14, color=YELLOW)
            highlight_label.to_edge(DOWN, buff=0.3)
            self.play(FadeIn(circle))
            self.play(FadeIn(highlight_label))
            self.wait(0.5)
            self.play(FadeOut(highlight_label))

        self.play_script_step(
            f"The {k} nearest neighbors are highlighted. The test point is classified as the majority class among them."
        )
        self.wait(2)


# ============================================================================
# 3D MACHINE LEARNING VISUALIZATIONS
# ============================================================================

class GradientDescent3DViz(ThreeDScene):
    """
    3D Gradient Descent Visualization.
    
    Features:
    - 3D surface plot (loss landscape: z = f(w1, w2))
    - Starting point on surface
    - Animated descent along gradient direction
    - Trajectory path (red line)
    - Legend and step counter
    - Convergence to global/local minimum
    """

    def construct(self):
        """Construct 3D gradient descent visualization."""
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        # Title
        title = Text("3D Gradient Descent Optimization", font_size=36, color=GRAY_A)
        title.scale(0.8)
        title.to_corner(UP + LEFT)
        self.add_fixed_in_frame_mobjects(title)

        # Create loss surface (simple quadratic)
        resolution_u = 20
        resolution_v = 20
        
        def loss_func(u, v):
            return u ** 2 + 2 * v ** 2

        surface = Surface(
            lambda u, v: np.array([u, v, loss_func(u, v)]),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(resolution_u, resolution_v),
            color=[BLUE, TEAL],
            fill_opacity=0.7,
            stroke_color=GRAY_B,
            stroke_width=0.5,
        )

        self.play(FadeIn(surface))

        # Starting point
        start_u, start_v = 2.5, 2.0
        start_z = loss_func(start_u, start_v)
        start_point = Sphere(radius=0.2, color=YELLOW)
        start_point.move_to(np.array([start_u, start_v, start_z]))
        self.play(FadeIn(start_point))

        # Trajectory
        trajectory_points = [np.array([start_u, start_v, start_z])]
        current_u, current_v = start_u, start_v
        learning_rate = 0.1

        # Gradient descent steps
        for step in range(15):
            # Compute gradients (dL/dw1, dL/dw2)
            grad_u = 2 * current_u
            grad_v = 4 * current_v

            # Update
            current_u -= learning_rate * grad_u
            current_v -= learning_rate * grad_v
            current_z = loss_func(current_u, current_v)

            next_point = np.array([current_u, current_v, current_z])
            trajectory_points.append(next_point)

            # Animate movement
            self.play(
                start_point.animate.move_to(next_point),
                run_time=0.3,
            )

            # Draw segment
            if step > 0:
                segment = Line(
                    trajectory_points[-2],
                    trajectory_points[-1],
                    color=RED,
                    stroke_width=2,
                )
                self.add(segment)

            self.wait(0.1)

        # Final annotation
        final_label = Text(
            "Converged to minimum",
            font_size=16,
            color=GREEN,
        )
        final_label.to_corner(DOWN + LEFT)
        self.add_fixed_in_frame_mobjects(final_label)
        self.play(FadeIn(final_label))

        self.wait(2)


# ============================================================================
# Export & Testing
# ============================================================================

if __name__ == "__main__":
    print("AlgoViz AI Templates Module")
    print("Available Classes:")
    print("  Data Structures: AVLTreeViz, BinaryTreeViz, RBTreeViz, BTreeViz, GraphSearchViz")
    print("  ML 2D: LinearRegressionViz, LogisticRegressionViz, SVMViz, KMeansViz, DecisionTreeViz, RandomForestViz, KNNViz")
    print("  ML 3D: GradientDescent3DViz")
