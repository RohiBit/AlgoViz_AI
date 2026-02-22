from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

config.media_dir = "./media"
config.video_dir = "./media"


class BubbleSortFullScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = "#020617"

        # ---------------- AI-REPLACEABLE CONTENT ----------------
        numbers = [5, 1, 4, 2, 8]

        intro_text = (
            "Bubble Sort is a simple comparison-based sorting algorithm. "
            "It repeatedly compares adjacent elements and swaps them if needed."
        )

        idea_text = (
            "It is called Bubble Sort because larger elements gradually bubble "
            "up to the end of the array."
        )

        pass_texts = [
            "First pass. The goal is to move the largest element to the end.",
            "Second pass. We ignore the last sorted element.",
            "Third pass. Only a few comparisons remain.",
            "Fourth pass. The array is now sorted."
        ]

        optimization_text = (
            "If a full pass completes without any swaps, "
            "the algorithm can stop early."
        )

        complexity_text = (
            "Bubble Sort has a time complexity of order n squared, "
            "due to its nested loops."
        )

        # ---------------- TITLE ----------------
        title = Text(
            "Bubble Sort Algorithm",
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

        # ---------------- ARRAY ----------------
        array = VGroup()
        for num in numbers:
            box = RoundedRectangle(
                width=1.2,
                height=1.2,
                corner_radius=0.2,
                color=BLUE_A
            )
            value = Text(str(num), font_size=36).move_to(box.get_center())
            array.add(VGroup(box, value))

        array.arrange(RIGHT, buff=0.3).move_to(ORIGIN)

        with self.voiceover(text=intro_text):
            self.play(
                LaggedStart(
                    *[FadeIn(cell, shift=UP * 0.5) for cell in array],
                    lag_ratio=0.2
                )
            )

        with self.voiceover(text=idea_text):
            bubble = Circle(radius=0.25, color=TEAL_A, fill_opacity=0.4)
            bubble.move_to(array[0].get_center())
            self.play(FadeIn(bubble))
            self.play(bubble.animate.shift(RIGHT * 5), run_time=3)
            self.play(FadeOut(bubble))

        # ---------------- SORTING PASSES ----------------
        n = len(array)

        for p in range(n - 1):
            pass_label = Text(
                f"Pass {p + 1}",
                font_size=30,
                color=YELLOW
            ).to_edge(LEFT)

            with self.voiceover(text=pass_texts[p]):
                self.play(FadeIn(pass_label))

            for i in range(n - p - 1):
                highlight = SurroundingRectangle(
                    VGroup(array[i], array[i + 1]),
                    color=YELLOW,
                    buff=0.15
                )

                self.play(Create(highlight), run_time=0.4)

                a = int(array[i][1].text)
                b = int(array[i + 1][1].text)

                if a > b:
                    self.play(
                        array[i].animate.shift(RIGHT * 1.5),
                        array[i + 1].animate.shift(LEFT * 1.5),
                        run_time=0.8
                    )
                    array[i], array[i + 1] = array[i + 1], array[i]

                self.play(FadeOut(highlight), run_time=0.2)

            array[n - p - 1][0].set_color(GREEN)
            self.play(FadeOut(pass_label))

        # ---------------- OPTIMIZATION ----------------
        opt_box = RoundedRectangle(
            width=7,
            height=2,
            corner_radius=0.3,
            color=GREEN
        ).to_edge(DOWN)

        opt_text = Text(
            "No swaps → Stop early",
            font_size=30,
            color=GREEN
        ).move_to(opt_box.get_center())

        with self.voiceover(text=optimization_text):
            self.play(Create(opt_box))
            self.play(Write(opt_text))

        self.wait(1)

        # ---------------- FIXED PART (IMPORTANT) ----------------
        # Remove title BEFORE showing complexity
        self.play(FadeOut(title), FadeOut(subtitle))

        complexity_label = Text(
            "Time Complexity: O(n²)",
            font_size=36,
            color=RED_A
        ).to_edge(UP)

        with self.voiceover(text=complexity_text):
            self.play(FadeIn(complexity_label, shift=DOWN))

        self.wait(2)

        # ---------------- END ----------------
        end_text = Text(
            "Final Sorted Array",
            font_size=32,
            color=GRAY_B
        ).next_to(array, DOWN)

        self.play(FadeIn(end_text))
        self.wait(2)