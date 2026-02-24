from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

config.media_dir = "./media"
config.video_dir = "./media"


class QueueFullScene(VoiceoverScene):

    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = "#020617"

        # ================= AI REPLACEABLE VALUES =================
        values = [10, 20, 30]

        intro_text = (
            "A queue is a linear data structure that follows "
            "First In First Out principle."
        )

        fifo_text = (
            "First In First Out means the first element inserted "
            "is the first element removed."
        )

        enqueue_text = (
            "Enqueue operation adds an element to the rear of the queue."
        )

        dequeue_text = (
            "Dequeue operation removes the element from the front."
        )

        pointer_text = (
            "Front points to the first element. Rear points to the last element."
        )

        complexity_text = (
            "Enqueue and dequeue operations take constant time, order one."
        )

        summary_text = (
            "Queue operations completed. Final queue shown on screen."
        )

        # ================= TITLE =================
        title = Text(
            "Queue Data Structure",
            font_size=48,
            gradient=(BLUE_B, TEAL_A)
        ).to_edge(UP)

        subtitle = Text(
            "FIFO Visualization",
            font_size=26,
            color=GRAY_A
        ).next_to(title, DOWN)

        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(1)

        # ================= CREATE QUEUE =================
        queue = VGroup(*[self.create_box(v) for v in values])
        queue.arrange(RIGHT, buff=0).move_to(ORIGIN)

        front_label = Text("Front", color=YELLOW)
        rear_label = Text("Rear", color=GREEN)

        self.update_labels(queue, front_label, rear_label)

        with self.voiceover(text=intro_text):
            self.play(LaggedStart(*[FadeIn(b, shift=UP) for b in queue], lag_ratio=0.2))
            self.play(FadeIn(front_label), FadeIn(rear_label))

        self.wait(1)

        # ================= FIFO EXPLANATION =================
        with self.voiceover(text=fifo_text):
            self.highlight(queue[0])  # front element

        self.wait(1)

        # ================= POINTER EXPLANATION =================
        with self.voiceover(text=pointer_text):
            self.highlight(queue[0])
            self.highlight(queue[-1])

        self.wait(1)

        # ================= ENQUEUE =================
        with self.voiceover(text=enqueue_text):

            new_box = self.create_box(40)
            new_box.next_to(queue[-1], RIGHT, buff=0)

            self.play(FadeIn(new_box, shift=RIGHT))

            queue.add(new_box)
            queue.arrange(RIGHT, buff=0).move_to(ORIGIN)

            self.update_labels(queue, front_label, rear_label)
            self.highlight(queue[-1])

        self.wait(1)

        # ================= DEQUEUE =================
        with self.voiceover(text=dequeue_text):

            first = queue[0]
            self.highlight(first)

            self.play(FadeOut(first, shift=LEFT))
            queue.remove(first)

            queue.arrange(RIGHT, buff=0).move_to(ORIGIN)
            self.update_labels(queue, front_label, rear_label)

        self.wait(1)

        # ================= COMPLEXITY =================
        self.play(FadeOut(title), FadeOut(subtitle))

        complexity = Text(
            "Enqueue: O(1)    Dequeue: O(1)",
            font_size=34,
            color=RED_A
        ).to_edge(UP)

        with self.voiceover(text=complexity_text):
            self.play(FadeIn(complexity))

        self.wait(2)

        # ================= SUMMARY =================
        summary = Text(
            "Final Queue State",
            font_size=30,
            color=GRAY_B
        ).to_edge(DOWN)

        with self.voiceover(text=summary_text):
            self.play(FadeIn(summary))

        self.wait(2)

    # ==========================================================
    # BOX CREATION
    # ==========================================================
    def create_box(self, value):
        rect = Rectangle(width=2.2, height=1, color=BLUE_A)
        text = Text(str(value), font_size=32).move_to(rect.get_center())
        return VGroup(rect, text)

    # ==========================================================
    # UPDATE FRONT & REAR LABELS
    # ==========================================================
    def update_labels(self, queue, front_label, rear_label):
        self.play(
            front_label.animate.next_to(queue[0], DOWN),
            rear_label.animate.next_to(queue[-1], DOWN),
            run_time=0.4
        )

    # ==========================================================
    # HIGHLIGHT BOX
    # ==========================================================
    def highlight(self, box):
        rect = box[0]
        original = rect.get_stroke_color()

        self.play(rect.animate.set_stroke(YELLOW, width=5))
        self.wait(0.5)
        self.play(rect.animate.set_stroke(original, width=2))