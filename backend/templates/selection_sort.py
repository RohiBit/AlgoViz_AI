from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

config.media_dir = "./media"
config.video_dir = "./media"


class SelectionSortFullScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = "#020617"  # Deep blue background

        # =========================================================
        # 🔁 AI-REPLACEABLE CONTENT
        # =========================================================
        numbers = [64, 25, 12, 22, 11]

        intro_text = (
            "Selection Sort is a simple comparison-based sorting algorithm. "
            "It repeatedly selects the smallest element from the unsorted part "
            "and places it at the correct position."
        )

        idea_text = (
            "Unlike Bubble Sort, Selection Sort makes fewer swaps. "
            "Each pass selects exactly one minimum element."
        )

        pass_texts = [
            "First pass. We search for the smallest element in the entire array.",
            "Second pass. We now search in the remaining unsorted portion.",
            "Third pass. The sorted portion continues to grow.",
            "Fourth pass. Only one comparison remains."
        ]

        complexity_text = (
            "Selection Sort always performs the same number of comparisons. "
            "Its time complexity is order n squared."
        )

        # =========================================================
        # 🎬 TITLE
        # =========================================================
        title = Text(
            "Selection Sort Algorithm",
            font_size=48,
            gradient=(BLUE_B, TEAL_A)
        ).to_edge(UP)

        subtitle = Text(
            "Step-by-Step Visualization",
            font_size=26,
            color=GRAY_A
        ).next_to(title, DOWN)

        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle))
        self.wait(1)

        # =========================================================
        # 📦 ARRAY CREATION
        # =========================================================
        array = VGroup()
        for num in numbers:
            box = RoundedRectangle(
                width=1.3,
                height=1.3,
                corner_radius=0.2,
                color=BLUE_A
            )
            value = Text(str(num), font_size=36).move_to(box.get_center())
            array.add(VGroup(box, value))

        array.arrange(RIGHT, buff=0.35).move_to(ORIGIN)

        with self.voiceover(text=intro_text):
            self.play(
                LaggedStart(
                    *[FadeIn(cell, shift=UP * 0.5) for cell in array],
                    lag_ratio=0.2
                )
            )

        with self.voiceover(text=idea_text):
            pointer = Arrow(UP, DOWN, color=YELLOW).next_to(array[0], UP)
            self.play(Create(pointer))
            self.wait(1)
            self.play(FadeOut(pointer))

        # =========================================================
        # 🔁 SELECTION SORT PASSES
        # =========================================================
        n = len(array)

        for p in range(n - 1):
            pass_label = Text(
                f"Pass {p + 1}",
                font_size=30,
                color=YELLOW
            ).to_edge(LEFT)

            with self.voiceover(text=pass_texts[p]):
                self.play(FadeIn(pass_label))

            min_index = p
            array[min_index][0].set_color(ORANGE)

            for i in range(p + 1, n):
                highlight = SurroundingRectangle(
                    array[i],
                    color=YELLOW,
                    buff=0.15
                )
                self.play(Create(highlight), run_time=0.4)

                current_val = int(array[i][1].text)
                min_val = int(array[min_index][1].text)

                if current_val < min_val:
                    array[min_index][0].set_color(BLUE_A)
                    min_index = i
                    array[min_index][0].set_color(ORANGE)

                self.play(FadeOut(highlight), run_time=0.2)

            # Swap minimum with first unsorted element
            if min_index != p:
                self.play(
                    array[p].animate.shift(RIGHT * (min_index - p) * 1.65),
                    array[min_index].animate.shift(LEFT * (min_index - p) * 1.65),
                    run_time=1
                )
                array[p], array[min_index] = array[min_index], array[p]

            array[p][0].set_color(GREEN)
            self.play(FadeOut(pass_label))
            self.wait(0.3)

        array[-1][0].set_color(GREEN)

        # =========================================================
        # ⏱️ COMPLEXITY (NO OVERLAP)
        # =========================================================
        self.play(FadeOut(title), FadeOut(subtitle))

        complexity_label = Text(
            "Time Complexity: O(n²)",
            font_size=36,
            color=RED_A
        ).to_edge(UP)

        with self.voiceover(text=complexity_text):
            self.play(FadeIn(complexity_label, shift=DOWN))

        self.wait(2)

        # =========================================================
        # 🎯 END
        # =========================================================
        end_text = Text(
            "Final Sorted Array",
            font_size=32,
            color=GRAY_B
        ).next_to(array, DOWN)

        self.play(FadeIn(end_text))
        self.wait(2)