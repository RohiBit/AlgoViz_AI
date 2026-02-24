from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

config.media_dir = "./media"
config.video_dir = "./media"


class ArrayFullScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = "#020617"

        # ---------------- AI-REPLACEABLE CONTENT ----------------
        numbers = [10, 20, 30, 40, 50]

        intro_text = (
            "An array is a linear data structure that stores elements "
            "in contiguous memory locations."
        )

        index_text = (
            "Each element in an array is accessed using its index. "
            "Indexing always starts from zero."
        )

        access_text = (
            "We can access any element directly using its index. "
            "This makes array access extremely fast."
        )

        update_text = (
            "We can also update elements using their index position."
        )

        traversal_text = (
            "Traversal means visiting each element one by one."
        )

        complexity_text = (
            "Array access time complexity is order one, "
            "because elements are accessed directly."
        )

        summary_text = (
            "Arrays provide fast access, easy updates, "
            "and simple traversal using indices."
        )

        # ---------------- TITLE ----------------
        title = Text(
            "Array Data Structure",
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

        # ---------------- CREATE ARRAY WITH INDEX ----------------
        array = VGroup()

        for i, num in enumerate(numbers):
            box = RoundedRectangle(
                width=1.2,
                height=1.2,
                corner_radius=0.2,
                color=BLUE_A
            )

            value = Text(str(num), font_size=36)
            value.move_to(box.get_center())

            index = Text(str(i), font_size=24, color=YELLOW)
            index.next_to(box, DOWN, buff=0.15)

            cell = VGroup(box, value, index)
            array.add(cell)

        array.arrange(RIGHT, buff=0.5).move_to(ORIGIN)

        # ---------------- INTRODUCTION ----------------
        with self.voiceover(text=intro_text):
            self.play(
                LaggedStart(
                    *[FadeIn(cell, shift=UP * 0.5) for cell in array],
                    lag_ratio=0.2
                )
            )

        self.wait(1)

        # ---------------- INDEXING ----------------
        with self.voiceover(text=index_text):
            for cell in array:
                highlight = SurroundingRectangle(cell[2], color=YELLOW, buff=0.1)
                self.play(Create(highlight), run_time=0.4)
                self.play(FadeOut(highlight), run_time=0.2)

        self.wait(1)

        # ---------------- ACCESS ELEMENT ----------------
        with self.voiceover(text=access_text):
            highlight = SurroundingRectangle(array[2], color=GREEN, buff=0.1)
            self.play(Create(highlight))
            self.wait(1)
            self.play(FadeOut(highlight))

        self.wait(1)

        # ---------------- UPDATE ELEMENT ----------------
        with self.voiceover(text=update_text):
            highlight = SurroundingRectangle(array[1], color=RED, buff=0.1)

            new_value = Text("25", font_size=36)
            new_value.move_to(array[1][0].get_center())

            self.play(Create(highlight))
            self.play(Transform(array[1][1], new_value))
            self.play(FadeOut(highlight))

        self.wait(1)

        # ---------------- TRAVERSAL ----------------
        with self.voiceover(text=traversal_text):
            for cell in array:
                highlight = SurroundingRectangle(cell, color=YELLOW, buff=0.1)
                self.play(Create(highlight), run_time=0.4)
                self.play(FadeOut(highlight), run_time=0.2)

        self.wait(1)

        # ---------------- REMOVE TITLE BEFORE COMPLEXITY ----------------
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---------------- COMPLEXITY ----------------
        complexity_label = Text(
            "Access Time Complexity: O(1)",
            font_size=36,
            color=RED_A
        ).to_edge(UP)

        with self.voiceover(text=complexity_text):
            self.play(FadeIn(complexity_label, shift=DOWN))

        self.wait(2)

        # ---------------- SUMMARY ----------------
        summary = Text(
            "Array Demonstration Complete",
            font_size=30,
            color=GRAY_B
        ).next_to(array, DOWN)

        with self.voiceover(text=summary_text):
            self.play(FadeIn(summary))

        self.wait(2)