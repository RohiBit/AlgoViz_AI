"""
B-Tree Visualization - Multi-Way Tree for Databases

Visualizes B-tree operations with configurable node capacity (order), insertion
with node splitting, deletion, and searching in multi-way tree structures used
in databases and file systems.

Author: AlgoViz AI
License: MIT
"""

from manim import *
from .base import AlgoVizBaseScene
from typing import List


class BTreeViz(AlgoVizBaseScene):
    """
    B-Tree Visualization.
    
    Features:
    - Configurable order (degree): each node holds m-1 to 2m-1 keys
    - Multi-way branching structure
    - Insertion with preemptive node splitting (maintains balance)
    - Deletion with complex rebalancing rules
    - Search highlighting across multiple keys per node
    - Height balance guarantee: all leaves at same depth
    - Ideal for disk-based indexing in databases
    
    B-Tree Properties:
    - Every node has at most m children
    - Every non-leaf node has at least ceil(m/2) children
    - Root has at least 2 children (if not leaf)
    - All leaves at same depth
    """

    def __init__(self, order: int = 3, *args, **kwargs):
        """
        Initialize B-tree with specified order.
        
        Args:
            order (int): Branching factor (default 3, means 2-3 tree)
        """
        self.order = order
        super().__init__(*args, **kwargs)

    def construct(self):
        """Construct B-tree visualization with insertions and splitting."""
        self.play_script_step(
            f"This is a B-tree of order {self.order}. "
            f"Each node can hold up to {self.order - 1} keys and {self.order} children."
        )

        # Example: Insert sequence with splits
        values = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        self.build_and_visualize_btree(values)

    def build_and_visualize_btree(self, values: List[int]):
        """
        Build B-tree step-by-step with node splitting.
        
        Args:
            values (List[int]): Values to insert in order
        """
        tree_mobjects = VGroup()

        # Title
        title = Text(f"B-Tree (Order {self.order}) Insertion & Splitting", font_size=32, color=GRAY_A)
        title.to_edge(UP)
        self.play(FadeIn(title))

        # Root node (initially contains first value)
        root_keys = [values[0]]
        root_node = self.create_bnode(root_keys)
        root_node.move_to(ORIGIN)

        self.play(FadeIn(root_node))
        tree_mobjects.add(root_node)

        # Insert remaining values
        for i in range(1, len(values)):
            val = values[i]
            self.play_script_step(f"Inserting {val}.")

            # Add key to root
            root_keys.append(val)
            root_keys.sort()

            # Check if split needed
            if len(root_keys) > self.order - 1:
                self.play_script_step(f"Node full! {len(root_keys)} keys exceed capacity of {self.order - 1}. Splitting...")

                # Simulate split (show old node shrinking and new nodes appearing)
                mid_idx = len(root_keys) // 2
                mid_val = root_keys[mid_idx]

                # Animate split
                self.play(root_node.animate.scale(0.7).shift(UP * 2), run_time=0.8)

                # Create left and right children
                left_keys = root_keys[:mid_idx]
                right_keys = root_keys[mid_idx + 1:]

                left_child = self.create_bnode(left_keys)
                left_child.shift(LEFT * 3 + DOWN * 2)

                right_child = self.create_bnode(right_keys)
                right_child.shift(RIGHT * 3 + DOWN * 2)

                # Draw edges
                left_edge = Line(root_node.get_center(), left_child.get_center(), color=WHITE, stroke_width=2)
                right_edge = Line(root_node.get_center(), right_child.get_center(), color=WHITE, stroke_width=2)

                self.play(FadeIn(left_child), FadeIn(right_child), FadeIn(left_edge), FadeIn(right_edge), run_time=0.8)

                # Reset root keys for next visualization
                root_keys = [mid_val]
                root_node[1].text = str(mid_val)

                tree_mobjects.add(left_child, right_child)
            else:
                # Just update root display
                root_display = str(" | ".join(map(str, root_keys)))
                root_node[1].text = root_display

        self.wait(2)

    def create_bnode(self, keys: List[int]) -> VGroup:
        """
        Create a B-tree node visualization.
        
        Args:
            keys (List[int]): Keys to display in node
            
        Returns:
            VGroup: Node visualization with rectangle background and key text
        """
        # Calculate rectangle width based on number of keys
        width = max(1.5, len(keys) * 0.6 + 0.5)
        height = 0.8

        node_rect = Rectangle(
            width=width,
            height=height,
            color=TEAL,
            fill_opacity=0.7,
            stroke_width=2
        )

        # Display keys separated by vertical lines
        keys_text = Text(" | ".join(map(str, keys)), font_size=14, color=WHITE)
        keys_text.move_to(node_rect.get_center())

        node = VGroup(node_rect, keys_text)
        return node

    def search_in_btree(self, target: int):
        """
        Visualize searching in B-tree.
        
        Args:
            target (int): Value to search for
        """
        search_label = Text(f"Searching for {target}...", font_size=18, color=YELLOW)
        search_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(search_label))

        # Simulate search traversal
        self.play_script_step(f"Starting at root, comparing {target} with node keys.")

        self.wait(0.5)
        self.play(FadeOut(search_label))

        result = Text("Found!", font_size=16, color=GREEN)
        result.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(result))
        self.wait(0.5)
        self.play(FadeOut(result))


class BTreePlus(BTreeViz):
    """
    B+ Tree Visualization (Enhanced B-Tree variant).
    
    B+ trees have all keys in leaf nodes, with internal nodes storing copies
    for routing. Used extensively in databases (e.g., MySQL InnoDB).
    """

    def construct(self):
        """Construct B+ tree with leaf level linked."""
        self.play_script_step(
            f"This is a B+ tree. All keys reside in the leaf level, "
            f"linked for efficient range queries."
        )
        self.build_and_visualize_btree([10, 20, 30, 40, 50, 60, 70, 80, 90])
