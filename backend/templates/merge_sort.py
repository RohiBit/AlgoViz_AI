from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class MergeSortTreeFinal(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = WHITE

        # --------------------------------------------------
        # Helper: array node (NO nesting across levels)
        # --------------------------------------------------
        def array_node(values, pos, stroke=BLACK):
            boxes = VGroup()
            for v in values:
                box = RoundedRectangle(
                    width=0.9,
                    height=0.6,
                    corner_radius=0.08,
                    stroke_color=stroke,
                    stroke_width=2,
                    fill_color=WHITE,
                    fill_opacity=1
                )
                txt = Text(str(v), font_size=26, color=BLACK)
                txt.move_to(box.get_center())
                boxes.add(VGroup(box, txt))
            boxes.arrange(RIGHT, buff=0.15)
            boxes.move_to(pos)
            return boxes

        # --------------------------------------------------
        # Helper: arrow
        # --------------------------------------------------
        def connect(parent, child):
            return Arrow(
                parent.get_bottom(),
                child.get_top(),
                buff=0.1,
                stroke_width=2,
                color=BLACK
            )

        # --------------------------------------------------
        # TITLE (INTRO ONLY)
        # --------------------------------------------------
        title = Text("Merge Sort Algorithm", font_size=40, color=BLACK)
        subtitle = Text("Divide → Conquer → Merge", font_size=24, color=GRAY_D).next_to(title, DOWN)

        with self.voiceover(
            text="Merge Sort is a divide and conquer sorting algorithm."
        ):
            self.play(FadeIn(title), FadeIn(subtitle))
            self.wait(1)

        self.play(FadeOut(title), FadeOut(subtitle))

        # --------------------------------------------------
        # LEVEL 0 (ROOT)
        # --------------------------------------------------
        level0 = array_node([38, 27, 43, 10], UP * 3)

        with self.voiceover(
            text="We start with the complete array."
        ):
            self.play(FadeIn(level0))
            self.wait(1)

        # --------------------------------------------------
        # LEVEL 1 (FIRST SPLIT)
        # --------------------------------------------------
        left1 = array_node([38, 27], UP * 1.5 + LEFT * 2)
        right1 = array_node([43, 10], UP * 1.5 + RIGHT * 2)

        arrows_l1 = VGroup(
            connect(level0, left1),
            connect(level0, right1)
        )

        with self.voiceover(
            text="We divide the array into two halves."
        ):
            self.play(
                level0.animate.set_opacity(0.3),
                FadeIn(left1),
                FadeIn(right1),
                Create(arrows_l1)
            )
            self.wait(1)

        # --------------------------------------------------
        # LEVEL 2 (SPLIT TO SINGLE ELEMENTS)
        # --------------------------------------------------
        l2a = array_node([38], DOWN * 0.2 + LEFT * 3)
        l2b = array_node([27], DOWN * 0.2 + LEFT * 1)

        r2a = array_node([43], DOWN * 0.2 + RIGHT * 1)
        r2b = array_node([10], DOWN * 0.2 + RIGHT * 3)

        arrows_l2 = VGroup(
            connect(left1, l2a),
            connect(left1, l2b),
            connect(right1, r2a),
            connect(right1, r2b)
        )

        with self.voiceover(
            text="Each half is divided again until we reach single elements."
        ):
            self.play(
                left1.animate.set_opacity(0.3),
                right1.animate.set_opacity(0.3),
                FadeIn(l2a), FadeIn(l2b),
                FadeIn(r2a), FadeIn(r2b),
                Create(arrows_l2)
            )
            self.wait(1)

        # --------------------------------------------------
        # MERGE LEFT SIDE
        # --------------------------------------------------
        merge_left = array_node([27, 38], DOWN * 1.8 + LEFT * 2, stroke=GREEN)
        arrow_ml = connect(l2a, merge_left)

        with self.voiceover(
            text="We now merge elements by comparing and ordering them."
        ):
            self.play(
                l2a.animate.set_opacity(0.3),
                l2b.animate.set_opacity(0.3),
                FadeIn(merge_left),
                Create(arrow_ml)
            )
            self.wait(1)

        # --------------------------------------------------
        # MERGE RIGHT SIDE
        # --------------------------------------------------
        merge_right = array_node([10, 43], DOWN * 1.8 + RIGHT * 2, stroke=GREEN)
        arrow_mr = connect(r2a, merge_right)

        self.play(
            r2a.animate.set_opacity(0.3),
            r2b.animate.set_opacity(0.3),
            FadeIn(merge_right),
            Create(arrow_mr)
        )
        self.wait(1)

        # --------------------------------------------------
        # FINAL MERGE
        # --------------------------------------------------
        final = array_node([10, 27, 38, 43], DOWN * 3, stroke=GREEN)

        arrows_final = VGroup(
            connect(merge_left, final),
            connect(merge_right, final)
        )

        with self.voiceover(
            text="Finally, we merge the two sorted halves to get the final sorted array."
        ):
            self.play(
                merge_left.animate.set_opacity(0.3),
                merge_right.animate.set_opacity(0.3),
                FadeIn(final),
                Create(arrows_final)
            )
            self.wait(2)

        # --------------------------------------------------
        # COMPLEXITY
        # --------------------------------------------------
        complexity = Text(
            "Time: O(n log n)     Space: O(n)",
            font_size=24,
            color=BLACK
        ).to_edge(DOWN)

        with self.voiceover(
            text="Merge Sort always runs in n log n time and uses extra space."
        ):
            self.play(FadeIn(complexity))
            self.wait(2)