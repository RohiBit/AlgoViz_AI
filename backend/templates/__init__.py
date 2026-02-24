"""
AlgoViz Templates Module - Organized Collection of Manim Visualization Classes

This module exports all visualization classes organized by topic:
- Data Structures: AVL Trees, Binary Trees, Red-Black Trees, B-Trees, Graph Search
- Machine Learning 2D: Linear Regression, Logistic Regression, SVM, K-Means, Decision Trees, Random Forests, KNN
- Machine Learning 3D: Gradient Descent
- Base: Reusable AlgoVizBaseScene class

Usage:
    from backend.templates import AVLTreeViz, LinearRegressionViz
    from backend.templates import AlgoVizBaseScene
    
    # Access specific classes
    scene = AVLTreeViz()
    viz = LinearRegressionViz()

Author: AlgoViz AI
License: MIT
"""

# Base class and utilities
from .base import AlgoVizBaseScene

# Data Structure Visualizations
from .avl_tree import AVLTreeViz
from .binary_tree import BinaryTreeViz
from .rbtree import RBTreeViz
from .btree import BTreeViz, BTreePlus
from .graph_search import GraphSearchViz

# Machine Learning 2D Visualizations
from .linear_regression import LinearRegressionViz
from .logistic_regression import LogisticRegressionViz
from .svm import SVMViz, SVMRegression
from .kmeans import KMeansViz, ElbowMethod
from .decision_tree import DecisionTreeViz, RandomForestViz
from .random_forest import RandomForestViz as RandomForestVizModule
from .knn import KNNViz

# Machine Learning 3D Visualizations
from .gradient_descent_3d import GradientDescent3DViz, RosenbrockGradientDescent


__all__ = [
    # Base class
    "AlgoVizBaseScene",
    
    # Data Structures
    "AVLTreeViz",
    "BinaryTreeViz",
    "RBTreeViz",
    "BTreeViz",
    "BTreePlus",
    "GraphSearchViz",
    
    # Machine Learning 2D
    "LinearRegressionViz",
    "LogisticRegressionViz",
    "SVMViz",
    "SVMRegression",
    "KMeansViz",
    "ElbowMethod",
    "DecisionTreeViz",
    "RandomForestViz",
    "KNNViz",
    
    # Machine Learning 3D
    "GradientDescent3DViz",
    "RosenbrockGradientDescent",
]


__version__ = "1.0.0"
__author__ = "AlgoViz AI"
__license__ = "MIT"
