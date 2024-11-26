from manim import *

class DijkstraVisualization(Scene):
    def construct(self):
        # Define graph nodes and positions
        positions = {
            "A": LEFT + UP,
            "B": RIGHT + UP,
            "C": RIGHT + DOWN,
            "D": LEFT + DOWN,
        }
        edges = [
            ("A", "B", 1),
            ("A", "C", 4),
            ("B", "C", 2),
            ("B", "D", 5),
            ("C", "D", 1),
        ]

        # Create graph visualization
        nodes = {name: Dot(positions[name], radius=0.15, color=BLUE).set_z_index(1) for name in positions}
        node_labels = {name: Text(name).next_to(nodes[name], UP) for name in nodes}
        edges_mobjects = []
        weights_mobjects = []

        for edge in edges:
            n1, n2, weight = edge
            line = Line(positions[n1], positions[n2], color=WHITE)
            mid_point = (positions[n1] + positions[n2]) / 2
            weight_text = Text(str(weight), font_size=24).move_to(mid_point).set_z_index(1)
            edges_mobjects.append(line)
            weights_mobjects.append(weight_text)

        # Add nodes and edges to the scene
        self.play(
            *[FadeIn(node) for node in nodes.values()],
            *[Write(label) for label in node_labels.values()],
            *[Create(edge) for edge in edges_mobjects],
            *[Write(weight) for weight in weights_mobjects],
        )
        self.wait(1)

        # Dijkstra algorithm visualization
        distances = {node: float('inf') for node in nodes}
        distances["A"] = 0
        visited = set()

        def visit_node(node):
            # Highlight current node
            self.play(nodes[node].animate.set_color(GREEN), run_time=0.5)
            visited.add(node)

        def relax_edge(start, end, weight):
            new_dist = distances[start] + weight
            if new_dist < distances[end]:
                distances[end] = new_dist
                # Highlight updated edge and value
                edge = next(e for e in edges_mobjects if {start, end} == {e.get_start(), e.get_end()})
                self.play(edge.animate.set_color(YELLOW), run_time=0.5)

        # Perform algorithm step-by-step
        visit_node("A")
        relax_edge("A", "B", 1)
        relax_edge("A", "C", 4)

        visit_node("B")
        relax_edge("B", "C", 2)
        relax_edge("B", "D", 5)

        visit_node("C")
        relax_edge("C", "D", 1)

        visit_node("D")
        self.wait(1)

        # Final distances
        distance_texts = [
            Text(f"{node}: {distances[node]}", font_size=24).to_edge(DOWN).shift(UP * i)
            for i, node in enumerate(distances)
        ]
        self.play(*[Write(text) for text in distance_texts])
        self.wait(2)
