"""
AlgoViz AI: Base Classes and Utilities for Manim Visualizations

This module provides the foundation for all AlgoViz visualization templates.
Includes the abstract base scene class and common utility functions.

Author: AlgoViz AI
License: MIT
"""

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from abc import ABC, abstractmethod
import numpy as np
from typing import Dict


class AlgoVizBaseScene(VoiceoverScene, ABC):
    """
    Abstract base class for all AlgoViz visualizations.
    Provides common utilities and enforces design standards.
    
    Design Principles:
    - Centering: All main diagrams dynamically centered on ORIGIN
    - No Overlap: Labels/text positioned with next_to() and proper buffering
    - Dark Mode Palette: Professional colors (BLUE/TEAL nodes, WHITE edges, YELLOW/RED highlights)
    - Dynamic Scaling: Handles large structures by scaling objects/camera
    - Script Integration: play_script_step(text) for guided narration
    - Modularity: Base classes for easy extension and reuse
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
