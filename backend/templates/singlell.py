from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

config.media_dir = "./media"
config.video_dir = "./media"


class SinglyLinkedListFullScene(VoiceoverScene):

    def construct(self):
        self.set_speech_service(GTTSService())
        self.camera.background_color = "#020617"

        # ================= AI-REPLACEABLE CONTENT =================
        values = [10, 20, 30]

        intro_text = (
            "A singly linked list is a linear data structure where each node "
            "contains data and a pointer to the next node."
        )

        node_text = (
            "Each node has two parts. The left side stores data. "
            "The right side stores the next pointer."
        )

        traversal_text = (
            "Traversal means visiting each node from head to last node."
        )

        insert_begin_text = (
            "To insert at beginning, we create a new node, "
            "point it to the old head, and update the head."
        )

        insert_end_text = (
            "To insert at end, we connect the last node pointer "
            "to the new node."
        )

        delete_text = (
            "To delete a node, we change the previous node pointer "
            "to skip that node."
        )

        complexity_text = (
            "Traversal takes order n time. "
            "Insertion at beginning takes order one time."
        )

        summary_text = (
            "Singly linked list supports dynamic memory "
            "and efficient insertion operations."
        )

        # ================= TITLE =================
        title = Text(
            "Singly Linked List",
            font_size=48,
            gradient=(BLUE_B, TEAL_A)
        ).to_edge(UP)

        subtitle = Text(
            "Step-by-Step Visualization",
            font_size=26,
            color=GRAY_A
        ).next_to(title, DOWN)

        self.play(FadeIn(title), FadeIn(subtitle))
        self.wait(1)

        # ================= INITIAL LIST =================
        nodes = VGroup(*[self.create_node(v) for v in values])
        nodes.arrange(RIGHT, buff=1.5).move_to(ORIGIN)
        self.auto_fit(nodes)

        self.arrows = self.create_arrows(nodes)

        head = Text("Head", font_size=28, color=YELLOW).next_to(nodes[0], UP)

        with self.voiceover(text=intro_text):
            self.play(
                LaggedStart(*[FadeIn(n, shift=UP) for n in nodes], lag_ratio=0.2),
                LaggedStart(*[Create(a) for a in self.arrows], lag_ratio=0.2),
                FadeIn(head)
            )

        self.wait(1)

        # ================= NODE STRUCTURE =================
        with self.voiceover(text=node_text):
            self.highlight(nodes[0][0], GREEN)
            self.highlight(nodes[0][1], RED)

        self.wait(1)

        # ================= TRAVERSAL =================
        with self.voiceover(text=traversal_text):
            for node in nodes:
                self.highlight(node[0], YELLOW)

        self.wait(1)

        # ================= INSERT AT BEGINNING =================
        with self.voiceover(text=insert_begin_text):

            new_node = self.create_node(5)
            self.play(FadeIn(new_node, shift=UP))

            nodes = VGroup(new_node, *nodes)
            self.rebuild(nodes)

            self.play(head.animate.next_to(nodes[0], UP))
            self.highlight(nodes[0][0], GREEN)

        self.wait(1)

        # ================= INSERT AT END =================
        with self.voiceover(text=insert_end_text):

            self.highlight(nodes[-1][1], RED)

            end_node = self.create_node(40)
            self.play(FadeIn(end_node, shift=UP))

            nodes = VGroup(*nodes, end_node)
            self.rebuild(nodes)

            self.highlight(nodes[-1][0], GREEN)

        self.wait(1)

        # ================= DELETE NODE =================
        with self.voiceover(text=delete_text):

            delete_node = nodes[2]
            self.highlight(delete_node[0], RED)

            prev_node = nodes[1]
            self.highlight(prev_node[1], YELLOW)

            # REMOVE VISUALLY FIRST
            self.play(FadeOut(delete_node))

            # REMOVE FROM STRUCTURE
            nodes = VGroup(*[n for i, n in enumerate(nodes) if i != 2])

            # REBUILD WITHOUT OLD ARROWS
            self.rebuild(nodes)

        self.wait(1)

        # ================= COMPLEXITY =================
        self.play(FadeOut(title), FadeOut(subtitle))

        complexity = Text(
            "Traversal: O(n)      Insertion: O(1)",
            font_size=34,
            color=RED_A
        ).to_edge(UP)

        with self.voiceover(text=complexity_text):
            self.play(FadeIn(complexity))

        self.wait(2)

        # ================= SUMMARY =================
        summary = Text(
            "Singly Linked List Demonstration Complete",
            font_size=30,
            color=GRAY_B
        ).to_edge(DOWN)

        with self.voiceover(text=summary_text):
            self.play(FadeIn(summary))

        self.wait(2)

    # ==========================================================
    # REBUILD FUNCTION (CRITICAL FIX)
    # ==========================================================
    def rebuild(self, nodes):

        # REMOVE OLD ARROWS
        if hasattr(self, "arrows"):
            self.play(FadeOut(self.arrows))

        nodes.arrange(RIGHT, buff=1.5).move_to(ORIGIN)
        self.auto_fit(nodes)

        # CREATE NEW ARROWS
        self.arrows = self.create_arrows(nodes)

        self.play(
            LaggedStart(*[Create(a) for a in self.arrows], lag_ratio=0.15)
        )

    # ==========================================================
    # NODE CREATION
    # ==========================================================
    def create_node(self, value):

        data = Rectangle(width=1.2, height=1, color=BLUE_A)
        pointer = Rectangle(width=0.8, height=1, color=TEAL_A)
        pointer.next_to(data, RIGHT, buff=0)

        text = Text(str(value), font_size=30).move_to(data.get_center())

        return VGroup(data, pointer, text)

    # ==========================================================
    # ARROW CREATION
    # ==========================================================
    def create_arrows(self, nodes):

        arrows = VGroup()

        for i in range(len(nodes) - 1):
            arrows.add(
                Arrow(
                    nodes[i].get_right(),
                    nodes[i+1].get_left(),
                    buff=0.15,
                    stroke_width=3,
                    color=WHITE
                )
            )

        return arrows

    # ==========================================================
    # AUTO FIT (PREVENT OUT OF FRAME)
    # ==========================================================
    def auto_fit(self, nodes):
        max_width = config.frame_width - 1
        if nodes.width > max_width:
            nodes.scale_to_fit_width(max_width)

    # ==========================================================
    # BORDER HIGHLIGHT
    # ==========================================================
    def highlight(self, obj, color):
        original = obj.get_stroke_color()
        self.play(obj.animate.set_stroke(color, width=5))
        self.wait(0.5)
        self.play(obj.animate.set_stroke(original, width=2))