from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

config.media_dir = "./media"
config.video_dir = "./media"


class StackFullScene(VoiceoverScene):

    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = "#020617"

        # ================= AI REPLACEABLE VALUES =================
        values = [10, 20, 30]

        intro_text = (
            "A stack is a linear data structure that follows "
            "Last In First Out principle."
        )

        lifo_text = (
            "Last In First Out means the last element pushed "
            "is the first element popped."
        )

        push_text = (
            "Push operation adds a new element to the top of the stack."
        )

        pop_text = (
            "Pop operation removes the top element from the stack."
        )

        peek_text = (
            "Peek operation returns the top element without removing it."
        )

        complexity_text = (
            "Push and pop operations take constant time, order one."
        )

        summary_text = (
            "Stack operations completed. Final stack shown on screen."
        )

        # ================= TITLE =================
        title = Text(
            "Stack Data Structure",
            font_size=48,
            gradient=(BLUE_B, TEAL_A)
        ).to_edge(UP)

        subtitle = Text(
            "LIFO Visualization",
            font_size=26,
            color=GRAY_A
        ).next_to(title, DOWN)

        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(1)

        # ================= CREATE STACK =================
        stack = VGroup(*[self.create_bucket(v) for v in values])
        stack.arrange(UP, buff=0).move_to(ORIGIN)

        top_label = Text("TOP", color=YELLOW)

        self.update_top_label(stack, top_label)

        with self.voiceover(text=intro_text):
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN) for b in stack], lag_ratio=0.2))
            self.play(FadeIn(top_label))

        self.wait(1)

        # ================= LIFO EXPLANATION =================
        with self.voiceover(text=lifo_text):
            self.highlight(stack[-1])  # TOP element

        self.wait(1)

        # ================= PUSH =================
        with self.voiceover(text=push_text):

            new_bucket = self.create_bucket(40)
            new_bucket.next_to(stack[-1], UP, buff=0)

            self.play(FadeIn(new_bucket, shift=UP))

            stack.add(new_bucket)
            stack.arrange(UP, buff=0).move_to(ORIGIN)

            self.update_top_label(stack, top_label)
            self.highlight(stack[-1])

        self.wait(1)

        # ================= POP =================
        with self.voiceover(text=pop_text):

            top_bucket = stack[-1]
            self.highlight(top_bucket)

            self.play(FadeOut(top_bucket, shift=UP))
            stack.remove(top_bucket)

            stack.arrange(UP, buff=0).move_to(ORIGIN)
            self.update_top_label(stack, top_label)

        self.wait(1)

        # ================= PEEK =================
        with self.voiceover(text=peek_text):
            self.highlight(stack[-1])  # TOP element

        self.wait(1)

        # ================= COMPLEXITY =================
        self.play(FadeOut(title), FadeOut(subtitle))

        complexity = Text(
            "Push: O(1)    Pop: O(1)",
            font_size=34,
            color=RED_A
        ).to_edge(UP)

        with self.voiceover(text=complexity_text):
            self.play(FadeIn(complexity))

        self.wait(2)

        # ================= SUMMARY =================
        summary = Text(
            "Final Stack State",
            font_size=30,
            color=GRAY_B
        ).to_edge(DOWN)

        with self.voiceover(text=summary_text):
            self.play(FadeIn(summary))

        self.wait(2)

    # ==========================================================
    # BUCKET STYLE NODE
    # ==========================================================
    def create_bucket(self, value):

        rect = Rectangle(width=2.5, height=1, color=BLUE_A)
        text = Text(str(value), font_size=32).move_to(rect.get_center())

        return VGroup(rect, text)

    # ==========================================================
    # UPDATE TOP LABEL
    # ==========================================================
    def update_top_label(self, stack, label):
        self.play(label.animate.next_to(stack[-1], RIGHT), run_time=0.4)

    # ==========================================================
    # HIGHLIGHT
    # ==========================================================
    def highlight(self, bucket):
        rect = bucket[0]
        original = rect.get_stroke_color()

        self.play(rect.animate.set_stroke(YELLOW, width=5))
        self.wait(0.6)
        self.play(rect.animate.set_stroke(original, width=2))