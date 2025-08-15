# Fully corrected example scenes from the ManimGL documentation page.
# Compatible with ManimGL v1.7.2+

from manimlib import *
import numpy as np
import math

# --------------------------------------------------
# Scene 1: InteractiveDevelopment
# --------------------------------------------------
class InteractiveDevelopment(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        square = Square()

        self.play(ShowCreation(square))
        self.wait()

        # NOTE: To use self.embed(), run manimgl without the -w (write) flag.
        # For example: `manimgl your_file.py InteractiveDevelopment -p`
        # This opens an iPython terminal where you can interactively code.
        self.embed()

        # The following lines are examples of what you can type in the shell.
        self.play(ReplacementTransform(square, circle))
        self.wait()
        self.play(circle.animate.stretch(4, 0))
        self.play(Rotate(circle, 90 * DEGREES))
        self.play(circle.animate.shift(2 * RIGHT).scale(0.25))

        text = Text("""
            In general, using the interactive shell
            is very helpful when developing new scenes
        """)
        self.play(Write(text))

# --------------------------------------------------
# Scene 2: AnimatingMethods
# --------------------------------------------------
class AnimatingMethods(Scene):
    def construct(self):
        grid = Tex(r"\pi").get_grid(10, 10, height=4)
        self.add(grid)

        self.play(grid.animate.shift(LEFT))
       
        self.play(grid.animate.set_color(YELLOW))
        self.wait()
        self.play(grid.animate.set_submobject_colors_by_gradient(BLUE, GREEN))
        self.wait()
        self.play(grid.animate.set_height(TAU - MED_SMALL_BUFF))
        self.wait()

        self.play(grid.animate.apply_complex_function(np.exp), run_time=5)
        self.wait()

        self.play(
            grid.animate.apply_function(
                lambda p: [
                    p[0] + 0.5 * math.sin(p[1]),
                    p[1] + 0.5 * math.sin(p[0]),
                    p[2]
                ]
            ),
            run_time=5,
        )
        self.wait()

# --------------------------------------------------
# Scene 3: TextExample
# --------------------------------------------------
class TextExample(Scene):
    def construct(self):
        text = Text("Here is a text", font="Consolas", font_size=90)
        difference = Text(
            """
            The most important difference between Text and TexText is that\n
            you can change the font more easily, but can't use the LaTeX grammar
            """,
            font="Arial", font_size=24,
            t2c={"Text": BLUE, "TexText": BLUE, "LaTeX": ORANGE}
        )
        VGroup(text, difference).arrange(DOWN, buff=1)
        self.play(Write(text))
        self.play(FadeIn(difference, UP))
        self.wait(3)

        fonts = Text(
            "And you can also set the font according to different words",
            font="Arial",
            t2f={"font": "Consolas", "words": "Consolas"},
            t2c={"font": BLUE, "words": GREEN}
        )
        fonts.set_width(FRAME_WIDTH - 1)
        slant = Text(
            "And the same as slant and weight",
            font="Consolas",
            t2s={"slant": ITALIC},
            t2w={"weight": BOLD},
            t2c={"slant": ORANGE, "weight": RED}
        )
        VGroup(fonts, slant).arrange(DOWN, buff=0.8)
        self.play(FadeOut(text), FadeOut(difference, shift=DOWN))
        self.play(Write(fonts))
        self.wait()
        self.play(Write(slant))
        self.wait()

# --------------------------------------------------
# Scene 4: TexTransformExample (Corrected)
# --------------------------------------------------
class TexTransformExample(Scene):
    def construct(self):
        to_isolate = ["B", "C", "=", "(", ")"]
        lines = VGroup(
            Tex("A^2", "+", "B^2", "=", "C^2"),
            Tex("A^2", "=", "C^2", "-", "B^2"),
            Tex("A^2 = (C + B)(C - B)", isolate=["A^2", *to_isolate]),
            Tex("A = \\sqrt{(C + B)(C - B)}", isolate=["A", *to_isolate])
        )
        lines.arrange(DOWN, buff=LARGE_BUFF)
        for line in lines:
            line.set_color_by_tex_to_color_map({
                "A": BLUE,
                "B": TEAL,
                "C": GREEN,
            })

        play_kw = {"run_time": 2}
        self.add(lines[0])
        self.play(
            TransformMatchingTex(
                lines[0].copy(), lines[1],
                path_arc=90 * DEGREES,
            ),
            **play_kw
        )
        self.wait()

        self.play(
            TransformMatchingTex(lines[1].copy(), lines[2]),
            **play_kw
        )
        self.wait()
        
        self.play(FadeOut(lines[2]))
        self.play(
            TransformMatchingTex(
                lines[1].copy(), lines[2],
                key_map={
                    "C^2": "C",
                    "B^2": "B",
                }
            ),
            **play_kw
        )
        self.wait()

        new_line2 = Tex("A^2 = (C + B)(C - B)", isolate=["A", *to_isolate])
        new_line2.replace(lines[2])
        new_line2.match_style(lines[2])

        self.play(
            TransformMatchingTex(
                new_line2, lines[3],
            ),
            **play_kw
        )
        
        self.wait(3)
        self.play(FadeOut(lines, RIGHT))

        source = Text("the morse code", height=1)
        target = Text("here come dots", height=1)

        self.play(Write(source))
        self.wait()
        kw = {"run_time": 3, "path_arc": PI / 2}
        self.play(TransformMatchingShapes(source, target, **kw))
        self.wait()
        self.play(TransformMatchingShapes(target, source, **kw))
        self.wait()

# --------------------------------------------------
# Scene 5: UpdatersExample
# --------------------------------------------------
class UpdatersExample(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE_E, 1)

        brace = always_redraw(Brace, square, UP)

        text, number = label = VGroup(
            Text("Width = "),
            DecimalNumber(
                0,
                show_ellipsis=True,
                num_decimal_places=2,
                include_sign=True,
            )
        )
        label.arrange(RIGHT)

        always(label.next_to, brace, UP)
        f_always(number.set_value, square.get_width)
        
        self.add(square, brace, label)

        self.play(
            square.animate.scale(2),
            rate_func=there_and_back,
            run_time=2,
        )
        self.wait()
        self.play(
            square.animate.set_width(5, stretch=True),
            run_time=3,
        )
        self.wait()
        self.play(
            square.animate.set_width(2),
            run_time=3
        )
        self.wait()

        now = self.time
        w0 = square.get_width()
        square.add_updater(
            lambda m: m.set_width(w0 * math.cos(self.time - now))
        )
        self.wait(4 * PI)

# --------------------------------------------------
# Scene 6: CoordinateSystemExample
# --------------------------------------------------
class CoordinateSystemExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=(-1, 10),
            y_range=(-2, 2, 0.5),
            height=6,
            width=10,
            axis_config={
                "stroke_color": GREY_A,
                "stroke_width": 2,
            },
            y_axis_config={
                "include_tip": False,
            }
        )
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=1,
        )
        self.add(axes)

        dot = Dot(color=RED)
        dot.move_to(axes.c2p(0, 0))
        self.play(FadeIn(dot, scale=0.5))
        self.play(dot.animate.move_to(axes.c2p(3, 2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(5, 0.5)))
        self.wait()

        h_line = always_redraw(lambda: axes.get_h_line(dot.get_left()))
        v_line = always_redraw(lambda: axes.get_v_line(dot.get_bottom()))

        self.play(
            ShowCreation(h_line),
            ShowCreation(v_line),
        )
        self.play(dot.animate.move_to(axes.c2p(3, -2)))
        self.wait()
        self.play(dot.animate.move_to(axes.c2p(1, 1)))
        self.wait()

        f_always(dot.move_to, lambda: axes.c2p(1, 1))
        self.play(
            axes.animate.scale(0.75).to_corner(UL),
            run_time=2,
        )
        self.wait()
        self.play(FadeOut(VGroup(axes, dot, h_line, v_line)))

# --------------------------------------------------
# Scene 7: GraphExample
# --------------------------------------------------
class GraphExample(Scene):
    def construct(self):
        axes = Axes((-3, 10), (-1, 8))
        axes.add_coordinate_labels()

        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        sin_graph = axes.get_graph(lambda x: 2 * math.sin(x), color=BLUE)
        relu_graph = axes.get_graph(lambda x: max(x, 0), use_smoothing=False, color=YELLOW)
        step_graph = axes.get_graph(lambda x: 2.0 if x > 3 else 1.0, discontinuities=[3], color=GREEN)

        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)")
        relu_label = axes.get_graph_label(relu_graph, Text("ReLU"))
        step_label = axes.get_graph_label(step_graph, Text("Step"), x=4)

        self.play(ShowCreation(sin_graph), FadeIn(sin_label, RIGHT))
        self.wait(2)
        self.play(ReplacementTransform(sin_graph, relu_graph), FadeTransform(sin_label, relu_label))
        self.wait()
        self.play(ReplacementTransform(relu_graph, step_graph), FadeTransform(relu_label, step_label))
        self.wait()

        parabola = axes.get_graph(lambda x: 0.25 * x**2)
        parabola.set_stroke(BLUE)
        self.play(FadeOut(step_graph), FadeOut(step_label), ShowCreation(parabola))
        self.wait()

        dot = Dot(color=RED)
        dot.move_to(axes.i2gp(2, parabola))
        self.play(FadeIn(dot, scale=0.5))

        x_tracker = ValueTracker(2)
        f_always(
            dot.move_to,
            lambda: axes.i2gp(x_tracker.get_value(), parabola)
        )

        self.play(x_tracker.animate.set_value(4), run_time=3)
        self.play(x_tracker.animate.set_value(-2), run_time=3)
        self.wait()

# --------------------------------------------------
# Scene 8: SurfaceExample
# --------------------------------------------------
class SurfaceExample(Scene):
    # NOTE: This is a 3D scene, so it requires the ThreeDCamera
    CONFIG = {
        "camera_class": ThreeDCamera,
    }

    def construct(self):

        """  
        IMPORTANT NOTE HERE: IF THIS FAILS, CREATE A "downloads" FOLDER IN THE SAME DIRECTORY AS manim_doc_examples.py.
        """
        surface_text = Text("For 3d scenes, try using surfaces")
        surface_text.fix_in_frame()
        surface_text.to_edge(UP)
        self.add(surface_text)
        self.wait(0.1)

        torus1 = Torus(r1=1, r2=1)
        torus2 = Torus(r1=3, r2=1)
        sphere = Sphere(radius=3, resolution=torus1.resolution)

        day_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Whole_world_-_land_and_oceans.jpg/1280px-Whole_world_-_land_and_oceans.jpg"
        night_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/The_earth_at_night.jpg/1280px-The_earth_at_night.jpg"

        surfaces = [
            TexturedSurface(surface, day_texture, night_texture)
            for surface in [sphere, torus1, torus2]
        ]

        for mob in surfaces:
            mob.shift(IN)
            mob.mesh = SurfaceMesh(mob)
            mob.mesh.set_stroke(BLUE, 1, opacity=0.5)

        frame = self.camera.frame
        frame.set_euler_angles(theta=-30 * DEGREES, phi=70 * DEGREES)
        surface = surfaces[0]

        self.play(FadeIn(surface), ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3))
        for mob in surfaces:
            mob.add(mob.mesh)
        surface.save_state()
        self.play(Rotate(surface, PI / 2), run_time=2)
        for mob in surfaces[1:]:
            mob.rotate(PI / 2)

        self.play(Transform(surface, surfaces[1]), run_time=3)
        self.play(
            Transform(surface, surfaces[2]),
            frame.animate.increment_phi(-10 * DEGREES),
            frame.animate.increment_theta(-20 * DEGREES),
            run_time=3
        )
        frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))

        light_text = Text("You can move around the light source")
        light_text.move_to(surface_text).fix_in_frame()
        self.play(FadeTransform(surface_text, light_text))
        
        light = self.camera.light_source
        self.add(light)
        light.save_state()
        self.play(light.animate.move_to(3 * IN), run_time=5)
        self.play(light.animate.shift(10 * OUT), run_time=5)

        drag_text = Text("Try moving the mouse while pressing d or s")
        drag_text.move_to(light_text).fix_in_frame()
        self.play(FadeTransform(light_text, drag_text))
        self.wait()
# --------------------------------------------------
# Scene 9: OpeningManimExample
# --------------------------------------------------
class OpeningManimExample(Scene):
    def construct(self):
        intro_words = Text("""
            The original motivation for manim was to 
            better illustrate mathematical functions
            as transformations.
        """)
        intro_words.to_edge(UP)

        self.play(Write(intro_words))
        self.wait(2)

        grid = NumberPlane((-10, 10), (-5, 5))
        matrix = [[1, 1], [0, 1]]
        
        matrix_mob = IntegerMatrix(matrix)
        matrix_mob.add_background_rectangle()

        linear_transform_words = VGroup(
            Text("This is what the matrix"),
            matrix_mob,
            Text("looks like")
        )
        linear_transform_words.arrange(RIGHT)
        linear_transform_words.to_edge(UP)
        linear_transform_words.set_stroke(BLACK, 10)

        self.play(
            ShowCreation(grid),
            FadeTransform(intro_words, linear_transform_words)
        )
        self.wait()
        self.play(grid.animate.apply_matrix(matrix), run_time=3)
        self.wait()

        c_grid = ComplexPlane()
        moving_c_grid = c_grid.copy()
        moving_c_grid.prepare_for_nonlinear_transform()
        c_grid.set_stroke(BLUE_E, 1)
        c_grid.add_coordinate_labels(font_size=24)
        
        # to ensure valid LaTeX syntax.
        complex_map_words = Tex(r"\text{Or thinking of the plane as} \mathbb{C} \text{ ,this is the map} z \rightarrow z^2")
        complex_map_words.to_corner(UR)
        complex_map_words.set_stroke(BLACK, 5)

        self.play(
            FadeOut(grid),
            Write(c_grid, run_time=3),
            FadeIn(moving_c_grid),
            FadeTransform(linear_transform_words, complex_map_words),
        )
        self.wait()
        self.play(
            moving_c_grid.animate.apply_complex_function(lambda z: z**2),
            run_time=6,
        )
        self.wait(2)