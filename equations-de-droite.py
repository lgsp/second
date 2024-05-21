from manim import *
import manim
from math import e, pi
import math
from PIL import Image

def disp_sub(self, lang):
    if lang.lower() == "en":
        written, phon = "Subscribe", "/səbˈskraɪb/"
        sub_pic = SVGMobject("/Users/digitalnomad/Documents/pics/svg/subscribe.svg")
        sub_scale = 0.8 
    elif lang.lower() == "fr":
        written, phon = "Abonnez-vous", "/abɔne vu/"
        sub_pic = ImageMobject("/Users/digitalnomad/Documents/pics/png/sabonner.png")
        sub_scale = 0.45
    elif lang.lower() == "ru":
        written, phon = "Подпишитесь", "/pɐd'piʂitʲɪsʲ/"

    sub = Paragraph(written, phon, line_spacing=0.5)
    self.play(GrowFromCenter(sub))
    self.wait(.5)
    self.play(FadeOut(sub))
    self.add(sub_pic.scale(sub_scale))
    self.wait(.5)

    
def disp_full_part_full(self, full, part, images, lang, full_scale=1):
    self.play(Write(full.scale(full_scale), run_time = 5))
    self.wait(.5)
    self.play(FadeOut(full))

    for img in images:
        pic = ImageMobject(img)
        self.add(pic.scale(0.25))
        self.wait(.5)
        self.remove(pic)
        
    self.play(Write(part.scale(full_scale), run_time = 3))
    self.wait(.5)
        
    self.play(ReplacementTransform(part, full), run_time=3)
    self.wait(.5)
    self.play(FadeOut(full))
    
    disp_sub(self, lang)


    
def inbox_msg(*inboxes, font_size):
    msg_text = ""
    for inbox in inboxes:
        msg_text += r"\mbox{" + f"{inbox}" + r"} \\"
    msg = MathTex(
        msg_text,
        tex_template=TexFontTemplates.french_cursive,
        font_size=font_size
    )
    return msg



def get_regular_polygon(n_gon):
    angle = (360 / n_gon) * DEGREES
    poly_n_gon = RegularPolygon(
        n = n_gon,
        start_angle = angle,
        color = RED
    )
    return poly_n_gon    



def replace_and_write(self, old, new, pos_ref, duration, **lines_and_scales):
    to_be_continued = False
    m, n = len(old), len(new)
    min_mn = m
    keys = lines_and_scales.keys()
    
    if m < n:
        to_be_continued = True
        min_mn = m
    elif m > n:
        self.play(*[FadeOut(old[i]) for i in range(n, m)])
        to_be_continued = False
        min_mn = n
    else: min_mn = m
    
    if lines_and_scales == {}:
        self.play(
            ReplacementTransform(
                old[0], new[0].next_to(pos_ref, 3 * DOWN)
            ),
            *[
                ReplacementTransform(
                    old[i],
                    new[i].next_to(new[i-1], DOWN)
                ) for i in range(1, min_mn)
            ]
        )
        if to_be_continued:
            self.play(
                *[
                    Write(new[i].next_to(new[i-1], DOWN)
                          ) for i in range(min_mn, n)
                ]
            )
    else:
        self.play(
            *[
                ReplacementTransform(
                old[0],
                new[0].scale(
                    lines_and_scales['0']
                ).next_to(pos_ref, 3 * DOWN)
                ) for i in range(1) if '0' in keys
              ],
            *[
                ReplacementTransform(
                old[0],
                new[0].next_to(pos_ref, 3 * DOWN)
                ) for i in range(1) if '0' not in keys
              ],
            *[
                ReplacementTransform(
                    old[i],
                    new[i].scale(
                        lines_and_scales[str(i)]
                    ).next_to(new[i - 1], DOWN)
                ) for i in range(1, min_mn) if str(i) in keys
            ],
            *[
                ReplacementTransform(
                    old[i],
                    new[i].next_to(new[i-1], DOWN)
                ) for i in range(1, min_mn) if str(i) not in keys
            ],
        )
        if to_be_continued:
            self.play(
                *[
                    Write(
                        new[i].scale(
                            lines_and_scales[str(i)]).next_to(
                                new[i - 1], DOWN)
                    ) for i in range(min_mn, n) if str(i) in keys
                ],
                *[
                    Write(
                        new[i].next_to(new[i - 1], DOWN)
                    ) for i in range(min_mn, n) if not str(i) in keys
                ],
            )
    
    self.wait(duration)


    
    
def cursive_msg(phrase, sep, font_size=40):
    inboxes = phrase.split(sep)
    msg = inbox_msg(*inboxes, font_size=font_size)
    return msg



def targets_to_write(text, ref, size=1, direction=DOWN):
    #text = [Text(t) for t in text if isinstance(t, str)]
    n = len(text)
    # Create a list of target objects
    targets = [text[0].next_to(ref, size * direction)]
    targets += [
        text[i].next_to(
            text[i - 1],
            size * direction
        ) for i in range(1, n)
    ]
    return text

def disp_calculations(self, previous_mobj, calcs, next2obj, direction):
            """
            This function replace previous_mobj with calcs next2obj
            
            previous_mobj: mobj to replace
            calcs: calculations to display
            next2obj: obj nearby to display
            direction: direction from next2obj
            """
            if previous_mobj:
                self.play(
                    ReplacementTransform(
                        previous_mobj,
                        calcs[0].next_to(next2obj, direction)
                    )
                )
            else:
                self.play(
                    Write(calcs[0].next_to(next2obj, direction))
                )
            self.wait(2)
            for i in range(len(calcs) - 1):
                self.play(
                    ReplacementTransform(
                        calcs[i],
                        calcs[i+1].next_to(next2obj, direction)
                    )
                )
                self.wait(2)

def disp_tex_list(self, previous_mobj, tex_list, next2obj, direction):
            """
            This function replace previous_mobj with tex_list next2obj
            
            previous_mobj: mobj to replace
            tex_list: list with Tex mobjs to display
            next2obj: obj nearby to display
            direction: direction from next2obj
            """
            if previous_mobj:
                self.play(
                    ReplacementTransform(
                        previous_mobj,
                        tex_list[0].next_to(next2obj, direction)
                    )
                )
            else:
                self.play(
                    Write(tex_list[0].next_to(next2obj, direction))
                )
            self.wait(2)
            for i in range(len(tex_list) - 1):
                self.play(
                    Write(
                        tex_list[i+1].next_to(tex_list[i], direction)
                    )
                )
                self.wait(2)
                
##################################################
# Équations de droites
##################################################

# Droites verticales
class Verticales(Scene):
    def construct(self):
        msg1 = "Droites verticales"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        ax = Axes().add_coordinates().scale(0.85).next_to(title1, 2 * DOWN)
        ax_labels = ax.get_axis_labels(
            Tex(r"abscisses \(x\)"),
            Tex(r"ordonnées \(y\)")
        ).scale(0.85)
        self.play(
            Create(ax),
            Create(ax_labels)
        )
        self.wait()
        
        # dots with respect to the axes
        A = Dot(ax.coords_to_point(-2, 2), color=BLUE)
        B = Dot(ax.coords_to_point(-2, -2), color=BLUE)
        C = Dot(ax.coords_to_point(-2, 0), color=RED)
        self.play(
            Write(A),
            Write(B)
        )
        self.wait()

        A_label = Tex("A", color=BLUE).next_to(A, UL).scale(0.85)
        B_label = Tex("B", color=BLUE).next_to(B, DL).scale(0.85)
        C_label = Tex("C", color=RED).next_to(C, UL).scale(0.85)
        self.play(
            Write(A_label),
            Write(B_label)
        )
        self.wait()
        
        A_lines = ax.get_lines_to_point(ax.c2p(-2, 2))
        B_lines = ax.get_lines_to_point(ax.c2p(-2, -2))

        q1 = Title("Quelle pourrait être l'équation de la droite (AB) ?")
        self.play(
            ReplacementTransform(title1, q1),
            Write(A_lines),
            Write(B_lines)
        )
        self.wait(2)

        q2 = Title("Le point C appartient-il à la droite (AB) ?")
        self.play(
            ReplacementTransform(q1, q2),
            *[Write(o) for o in [C, C_label]]
        )
        self.wait(2)

        
        q3 = Title("Quel est le point commun entre A, B et C ?")
        self.play(ReplacementTransform(q2, q3))
        self.wait(2)

        rep = [
            r"\(x_A = x_B = x_C = -2\)",
            r"\((AB) : \, x = -2\)"
        ]

        rep_tex = [Tex(r) for r in rep]
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=rep_tex,
            next2obj=B_label,
            direction=DOWN
        )

        box = SurroundingRectangle(rep_tex[-1], color=RED)
        self.play(
            Indicate(rep_tex[-1], color=RED),
        )
        self.wait()

        self.play(
            Circumscribe(rep_tex[-1], color=RED),
        )
        self.wait()

        ab_eq = VGroup(rep_tex[-1], box)
        self.play(
            ab_eq.animate.next_to(C_label, 3 * LEFT),
            FadeOut(rep_tex[0])
        )
        self.wait()

        ab_curve = ax.plot_implicit_curve(
            lambda x, y: x + 2, color=RED
        )
        self.play(
            Write(ab_curve)
        )
        self.wait()

        
        M = Dot(ax.coords_to_point(-2, -4), color=ORANGE)
        y = ValueTracker(-2.65)
        pointer = Vector(RIGHT).next_to(M, LEFT)

        M.add_updater(lambda z: z.set_y(y.get_value()))
        pointer.add_updater(lambda z: z.set_y(y.get_value()))
        ab_eq.add_updater(lambda z: z.set_y(y.get_value()))
        
        self.play(
            Write(M),
            Write(pointer.next_to(M, LEFT)),
            ab_eq.animate.next_to(pointer, 0.5 * LEFT)
        )
        self.wait()
        self.play(
            y.animate.set_value(2.45),
            run_time=2
        )
        self.wait()

        t4 = Title(r"Si \(M(x;y)\in(AB)\) alors \(x = -2\)")
        self.play(
            ReplacementTransform(q3, t4),
            y.animate.set_value(-2.65),
            run_time=2
        )
        self.wait()

        x_vals = list(range(-1, 7))
        ab_tex = [Tex(r"(AB)\,:\,x = " + f"{x}") for x in x_vals]
        boxes = [SurroundingRectangle(e, color=RED) for e in ab_tex]
        ab_eqs = VGroup(*[
            VGroup(ab_tex[i], boxes[i]) for i in range(len(boxes))
        ])
        A_dots = [Dot(ax.coords_to_point(x, 2), color=BLUE) for x in x_vals]
        B_dots = [Dot(ax.coords_to_point(x, -2), color=BLUE) for x in x_vals]
        A_lin_updates = [ax.get_lines_to_point(ax.c2p(x, 2)) for x in x_vals]
        B_lin_updates = [ax.get_lines_to_point(ax.c2p(x, -2)) for x in x_vals]

        C_dots = [Dot(ax.coords_to_point(x, 0), color=RED) for x in x_vals]
        M_dots = [Dot(ax.coords_to_point(x, -4), color=ORANGE) for x in x_vals]
        ab_curves = [ax.plot_implicit_curve(
            lambda x, y: x - xv, color=RED
        ) for xv in x_vals]

        titles = [
            Title(
                r"Si \(M(x;y)\in(AB)\) alors \(x = " + f"{x}\)"
            ) for x in x_vals
        ]
        
        for i in range(len(x_vals)):
            if i == 0:
                self.play(
                    ReplacementTransform(t4, titles[0]),
                    A.animate.move_to(A_dots[i]),
                    A_label.animate.next_to(A, UL),
                    ReplacementTransform(A_lines, A_lin_updates[i]),
                    B.animate.move_to(B_dots[i]),
                    B_label.animate.next_to(B, DL),
                    ReplacementTransform(B_lines, B_lin_updates[i]),
                    C.animate.move_to(C_dots[i]),
                    C_label.animate.next_to(C, LEFT),
                    M.animate.move_to(M_dots[i]),
                    pointer.animate.next_to(M, LEFT),
                    ab_curve.animate.move_to(ab_curves[i]),
                    ReplacementTransform(
                        ab_eq,
                        ab_eqs[i].next_to(pointer, 0.5 * LEFT)
                    ),
                )
                ab_eqs[i].add_updater(lambda z: z.set_y(y.get_value()))
                self.wait()
            else:
                self.play(
                    ReplacementTransform(titles[i-1], titles[i]),
                    A.animate.move_to(A_dots[i]),
                    A_label.animate.next_to(A, 0.5 * UL),
                    ReplacementTransform(A_lin_updates[i-1], A_lin_updates[i]),
                    B.animate.move_to(B_dots[i]),
                    B_label.animate.next_to(B, 0.5 * DL),
                    ReplacementTransform(B_lin_updates[i-1], B_lin_updates[i]),
                    C.animate.move_to(C_dots[i]),
                    C_label.animate.next_to(C, 0.5 * LEFT),
                    ab_curve.animate.move_to(ab_curves[i]),
                    M.animate.move_to(M_dots[i]),
                    pointer.animate.next_to(M, LEFT),
                    ReplacementTransform(
                        ab_eqs[i-1],
                        ab_eqs[i].next_to(pointer, 0.5 * LEFT)
                    ),
                )
                ab_eqs[i].add_updater(lambda z: z.set_y(y.get_value()))
                self.wait()
                
            self.play(
                y.animate.set_value(2.45),
                run_time=2
            )
            self.wait()
            
            self.play(
                y.animate.set_value(-2.65),
                run_time=2
            )
            self.wait()
            


# Droites horizontales
class Horizontales(Scene):
    def construct(self):
        msg1 = "Droites horizontales"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        ax = Axes().add_coordinates().scale(0.85).next_to(title1, 2 * DOWN)
        ax_labels = ax.get_axis_labels(
            Tex(r"abscisses \(x\)"),
            Tex(r"ordonnées \(y\)")
        ).scale(0.85)
        self.play(
            Create(ax),
            Create(ax_labels)
        )
        self.wait()
        
        # dots with respect to the axes
        A = Dot(ax.coords_to_point(-2, -2), color=BLUE)
        B = Dot(ax.coords_to_point(2, -2), color=BLUE)
        C = Dot(ax.coords_to_point(0, -2), color=RED)
        self.play(
            Write(A),
            Write(B)
        )
        self.wait()

        A_label = Tex("A", color=BLUE).next_to(A, UL).scale(0.85)
        B_label = Tex("B", color=BLUE).next_to(B, UR).scale(0.85)
        C_label = Tex("C", color=RED).next_to(C, UL).scale(0.85)
        self.play(
            Write(A_label),
            Write(B_label)
        )
        self.wait()
        
        A_lines = ax.get_lines_to_point(ax.c2p(-2, -2))
        B_lines = ax.get_lines_to_point(ax.c2p(2, -2))

        q1 = Title("Quelle pourrait être l'équation de la droite (AB) ?")
        self.play(
            ReplacementTransform(title1, q1),
            Write(A_lines),
            Write(B_lines)
        )
        self.wait(2)

        q2 = Title("Le point C appartient-il à la droite (AB) ?")
        self.play(
            ReplacementTransform(q1, q2),
            *[Write(o) for o in [C, C_label]]
        )
        self.wait(2)

        
        q3 = Title("Quel est le point commun entre A, B et C ?")
        self.play(ReplacementTransform(q2, q3))
        self.wait(2)

        rep = [
            r"\(   y_A = y_B = y_C = -2\)",
            r"\((AB) : \, y = -2\)"
        ]

        rep_tex = [Tex(r) for r in rep]
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=rep_tex,
            next2obj=ax_labels[1],
            direction=DOWN
        )

        box = SurroundingRectangle(rep_tex[-1], color=RED)
        self.play(
            Indicate(rep_tex[-1], color=RED),
        )
        self.wait()

        self.play(
            Circumscribe(rep_tex[-1], color=RED),
        )
        self.wait()

        ab_eq = VGroup(rep_tex[-1], box)
        self.play(
            FadeOut(rep_tex[0])
        )
        self.wait()

        ab_curve = ax.plot(
            lambda x: -2, color=RED
        )
        self.play(
            Write(ab_curve)
        )
        self.wait()

        
        M = Dot(ax.coords_to_point(-5, -2), color=ORANGE)
        x = ValueTracker(-5)
        pointer = Vector(UP).next_to(M, DOWN)

        M.add_updater(lambda z: z.set_x(x.get_value()))
        pointer.add_updater(lambda z: z.set_x(x.get_value()))
        ab_eq.add_updater(lambda z: z.set_x(x.get_value()))
        
        self.play(
            Write(M),
            Write(pointer.next_to(M, DOWN)),
            ab_eq.animate.next_to(pointer, 0.5 * DOWN)
        )
        self.wait()
        self.play(
            x.animate.set_value(5),
            run_time=2
        )
        self.wait()

        t4 = Title(r"Si \(M(x;y)\in(AB)\) alors \(y = -2\)")
        self.play(
            ReplacementTransform(q3, t4),
            x.animate.set_value(-5),
            run_time=2
        )
        self.wait()

        y_vals = list(range(-1, 4))
        ab_tex = [Tex(r"(AB)\,:\,y = " + f"{y}") for y in y_vals]
        boxes = [SurroundingRectangle(e, color=RED) for e in ab_tex]
        ab_eqs = VGroup(*[
            VGroup(ab_tex[i], boxes[i]) for i in range(len(boxes))
        ])
        A_dots = [Dot(ax.coords_to_point(-2, y), color=BLUE) for y in y_vals]
        B_dots = [Dot(ax.coords_to_point(2, y), color=BLUE) for y in y_vals]
        A_lin_updates = [ax.get_lines_to_point(ax.c2p(-2, y)) for y in y_vals]
        B_lin_updates = [ax.get_lines_to_point(ax.c2p(2, y)) for y in y_vals]

        C_dots = [Dot(ax.coords_to_point(0, y), color=RED) for y in y_vals]
        M_dots = [Dot(ax.coords_to_point(-5, y), color=ORANGE) for y in y_vals]
        ab_curves = [ax.plot(
            lambda x: yv, color=RED
        ) for yv in y_vals]

        titles = [
            Title(
                r"Si \(M(x;y)\in(AB)\) alors \(y = " + f"{y}\)"
            ) for y in y_vals
        ]
        
        for i in range(len(y_vals)):
            if i == 0:
                self.play(
                    ReplacementTransform(t4, titles[0]),
                    A.animate.move_to(A_dots[i]),
                    A_label.animate.next_to(A, UL),
                    ReplacementTransform(A_lines, A_lin_updates[i]),
                    B.animate.move_to(B_dots[i]),
                    B_label.animate.next_to(B, UR),
                    ReplacementTransform(B_lines, B_lin_updates[i]),
                    C.animate.move_to(C_dots[i]),
                    C_label.animate.next_to(C, LEFT),
                    M.animate.move_to(M_dots[i]),
                    pointer.animate.next_to(M, DOWN),
                    ab_curve.animate.move_to(ab_curves[i]),
                    ReplacementTransform(
                        ab_eq,
                        ab_eqs[i].next_to(pointer, 0.5 * DOWN)
                    ),
                )
                ab_eqs[i].add_updater(lambda z: z.set_x(x.get_value()))
                self.wait()
            else:
                self.play(
                    ReplacementTransform(titles[i-1], titles[i]),
                    A.animate.move_to(A_dots[i]),
                    A_label.animate.next_to(A, 0.5 * UL),
                    ReplacementTransform(A_lin_updates[i-1], A_lin_updates[i]),
                    B.animate.move_to(B_dots[i]),
                    B_label.animate.next_to(B, 0.5 * UR),
                    ReplacementTransform(B_lin_updates[i-1], B_lin_updates[i]),
                    C.animate.move_to(C_dots[i]),
                    C_label.animate.next_to(C, 0.5 * LEFT),
                    ab_curve.animate.move_to(ab_curves[i]),
                    M.animate.move_to(M_dots[i]),
                    pointer.animate.next_to(M, DOWN),
                    ReplacementTransform(
                        ab_eqs[i-1],
                        ab_eqs[i].next_to(pointer, 0.5 * DOWN)
                    ),
                )
                ab_eqs[i].add_updater(lambda z: z.set_x(x.get_value()))
                self.wait()
                
            self.play(
                x.animate.set_value(5),
                run_time=2
            )
            self.wait()
            
            self.play(
                x.animate.set_value(-5),
                run_time=2
            )
            self.wait()
            
            

# Droites obliques
class Obliques(Scene):
    def construct(self):
        msg1 = "Droites obliques"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        ax = Axes().add_coordinates().scale(0.85).next_to(title1, 2 * DOWN)
        ax_labels = ax.get_axis_labels(
            Tex(r"abscisses \(x\)"),
            Tex(r"ordonnées \(y\)")
        ).scale(0.85)
        self.play(
            Create(ax),
            Create(ax_labels)
        )
        self.wait()
        
        # dots with respect to the axes
        A = Dot(ax.coords_to_point(-2, -2), color=BLUE)
        B = Dot(ax.coords_to_point(2, 3), color=BLUE)
        C = Dot(ax.coords_to_point(2, -2), color=RED)

        self.play(
            Write(A),
            Write(B)
        )
        self.wait()

        A_label = Tex("A", color=BLUE).next_to(A, LEFT).scale(0.85)
        B_label = Tex("B", color=BLUE).next_to(B, RIGHT).scale(0.85)
        C_label = Tex("C", color=RED).next_to(C, RIGHT).scale(0.85)

        self.play(
            Write(A_label),
            Write(B_label)
        )
        self.wait()
        
        A_lines = ax.get_lines_to_point(ax.c2p(-2, -2))
        B_lines = ax.get_lines_to_point(ax.c2p(2, 3))
        C_lines = ax.get_lines_to_point(ax.c2p(2, -2))
        vector_AC = Arrow(A, C, color=RED)
        AC_line = Line(A, C, color=RED)
        CB_line = Line(C, B, color=RED)
        vector_CB = Arrow(C, B, color=RED)
        AB_lines = [A_lines, B_lines]
        ABC_lines = [AC_line, CB_line]
        ABC_vects = [vector_AC, vector_CB]
        
        q1 = Title("Quelle pourrait être l'équation de la droite (AB) ?")
        self.play(
            ReplacementTransform(title1, q1),
            *[Write(l) for l in AB_lines]
        )
        self.wait(2)

        q2 = Title("Le point C appartient-il à la droite (AB) ?")
        self.play(
            ReplacementTransform(q1, q2),
            *[Write(o) for o in [C, C_label]]
        )
        self.wait(2)

        self.play(
            *[Write(l) for l in ABC_vects]
        )
        self.wait(2)
        
        q3 = Title("Quelle est la relation entre A, B et C ?")
        self.play(ReplacementTransform(q2, q3))
        self.wait(2)

        rep = [
            r"\(x_B = x_C = 3\)",
            r"\(y_A = y_C = -2\)",
            r"\((AB) : y = mx + p\)",
            r"\(y_B = mx_B + p\)",
            r"\(y_A = mx_A + p\)",
            r"\(\dfrac{y_B - y_A}{x_B - x_A} = \dfrac{5}{4} = 1,25\)",
            r"\(p = y_B - mx_B\)",
            r"\(p = 3 - 1,25\times 2\)",
            r"\(p = 0,5\)",
            r"\((AB) : y = \dfrac{5}{4}x + \dfrac{1}{2}\)"
        ]

        rep_tex = [Tex(r) for r in rep]
        disp_calculations(
            self,
            previous_mobj=None,
            calcs=rep_tex,
            next2obj=C_label,
            direction=RIGHT
        )

        box = SurroundingRectangle(rep_tex[-1], color=GREEN)
        self.play(
            Indicate(rep_tex[-1], color=GREEN),
        )
        self.wait()

        self.play(
            Circumscribe(rep_tex[-1], color=GREEN),
        )
        self.wait()

        ab_eq = VGroup(rep_tex[-1], box)

        def affine(x): return 1.25 * x + 0.5
        
        ab_curve = ax.plot(affine, color=GREEN)
        
        self.play(
            Write(ab_curve),
            ab_eq.animate.next_to(A, DL)
        )
        self.wait()

        t = ValueTracker(-7)
        initial_point = [
            ax.coords_to_point(
                t.get_value(),
                affine(t.get_value())
            )
        ]
        M = Dot(point=initial_point, color=ORANGE)
        M.add_updater(
            lambda x: x.move_to(
                ax.c2p(
                    t.get_value(),
                    affine(t.get_value())
                )
            )
        )
        
        pointer = Vector(RIGHT).next_to(M, LEFT)
        
        
        self.play(
            Write(M),
            Write(pointer.next_to(M, LEFT)),
            ab_eq.animate.next_to(pointer, 1.5 * RIGHT),
        )
        self.wait()

        pointer.add_updater(
            lambda x: x.move_to(
                ax.c2p(
                    t.get_value() - 1,
                    affine(t.get_value())
                )
            )
        )
        
        ab_eq.add_updater(
            lambda x: x.move_to(
                ax.c2p(
                    t.get_value() + 4,
                    affine(t.get_value())
                )
            )
        )

        t4 = Title(r"Si \(M(x;y)\in(AB)\) alors \(y = 1,25x + 0,5\)")
        self.play(
            ReplacementTransform(q3, t4),
            t.animate.set_value(6),
            pointer.animate.next_to(M, LEFT),
            ab_eq.animate.next_to(M, 2 * RIGHT),
            run_time = 10
        )
        self.wait(2)

        self.play(
            t.animate.set_value(-7),
            pointer.animate.next_to(M, LEFT),
            ab_eq.animate.next_to(M, 2 * RIGHT),
            run_time = 10
        )
        self.wait(2)
        



class Cartesian(Scene):
    def construct(self):
        msg1 = "Équations cartésiennes de droites"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        ax = Axes().add_coordinates().scale(0.85).next_to(title1, 2 * DOWN)
        ax_labels = ax.get_axis_labels(
            Tex(r"abscisses \(x\)"),
            Tex(r"ordonnées \(y\)")
        ).scale(0.85)
        self.play(
            Create(ax),
            Create(ax_labels)
        )
        self.wait()
        
        # dots with respect to the axes
        A = Dot(ax.coords_to_point(-5, -2), color=BLUE)
        B = Dot(ax.coords_to_point(1, 2), color=BLUE)
        C = Dot(ax.coords_to_point(-5, 2), color=RED)
        
        self.play(
            *[Write(d) for d in [A, B, C]]
        )
        self.wait()

        A_label = Tex("A", color=BLUE).next_to(A, LEFT).scale(0.85)
        B_label = Tex("B", color=BLUE).next_to(B, RIGHT).scale(0.85)
        C_label = Tex("C", color=RED).next_to(C, LEFT).scale(0.85)

        self.play(
            Write(A_label),
            Write(B_label),
            Write(C_label),
        )
        self.wait()
        
        A_lines = ax.get_lines_to_point(ax.c2p(-5, -2))
        B_lines = ax.get_lines_to_point(ax.c2p(1, 2))
        C_lines = ax.get_lines_to_point(ax.c2p(-5, 2))
        
        q1 = Title("Quelle pourrait être l'équation de la droite (AB) ?")
        self.play(
            ReplacementTransform(title1, q1),
            *[Write(l) for l in [A_lines, B_lines, C_lines]]
        )
        self.wait(2)

        vector_AC = Arrow(A, C, color=RED)
        vector_CB = Arrow(C, B, color=RED)
        vects = [vector_AC, vector_CB]
        q2 = Title(
            r"Quelles sont les coordonnées du vecteur \(\overrightarrow{AB}\) ?"
        )
        self.play(
            ReplacementTransform(q1, q2),
            *[Write(v) for v in vects]
        )
        self.wait(2)
        
        
        def affine(x): return (2/3) * x + (4/3)
        
        ab_curve = ax.plot(affine, color=GREEN)

        q3 = Title("Comment exprimer la droite (AB) vectoriellement ?")
        self.play(
            ReplacementTransform(q2, q3),
            Write(ab_curve),
        )
        self.wait()

        t = ValueTracker(-7)
        initial_point = [
            ax.coords_to_point(
                t.get_value(),
                affine(t.get_value())
            )
        ]
        M = Dot(point=initial_point, color=ORANGE)
        M.add_updater(
            lambda x: x.move_to(
                ax.c2p(
                    t.get_value(),
                    affine(t.get_value())
                )
            )
        )
        
        q4 = Title("La droite (AB) est l'ensemble des points \(M(x ; y)\) vérifiant :")
        rep = [
            r"\(\overrightarrow{AM} = k\overrightarrow{AB}\)",
            r"\(\det(\overrightarrow{AM} = \overrightarrow{AB}) = 0\)",
            r"\(x_{\overrightarrow{AM}}y_{\overrightarrow{AB}} - x_{\overrightarrow{AB}}y_{\overrightarrow{AM}} = 0\)",
            r"\(4x - 6y + 8 = 0\)",
            r"\((AB) : 2x - 3y + 4 = 0\)"
        ]

        rep_tex = [Tex(r).scale(0.75) for r in rep]
        disp_calculations(
            self,
            previous_mobj=None,
            calcs=rep_tex,
            next2obj=C_label,
            direction=UP
        )

        box = SurroundingRectangle(rep_tex[-1], color=GREEN)
        self.play(
            ReplacementTransform(q3, q4),
            Indicate(rep_tex[-1], color=GREEN),
        )
        self.wait()

        self.play(
            Circumscribe(rep_tex[-1], color=GREEN),
        )
        self.wait()

        ab_eq = VGroup(rep_tex[-1], box)
        
        self.play(
            Write(M),
        )
        self.wait()

        
        ab_eq.add_updater(
            lambda x: x.move_to(
                ax.c2p(
                    t.get_value() + 4,
                    affine(t.get_value())
                )
            )
        )

        t4 = Title(r"Si \(M(x;y)\in(AB)\) alors \(2x - 3y + 4 = 0\)")
        self.play(
            ReplacementTransform(q4, t4),
            t.animate.set_value(6),
            ab_eq.animate.next_to(M, 2 * RIGHT),
            run_time = 10
        )
        self.wait(2)

        self.play(
            t.animate.set_value(-7),
            ab_eq.animate.next_to(M, 2 * RIGHT),
            run_time = 10
        )
        self.wait(2)
        


        
class Determinant(Scene):
    def construct(self):
        msg1 = "Déterminant et équations de droites"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        
        rep = [
            r"On considère une droite une droite \(\mathcal{D}\) "
            r"passant par un point A ",
            r"et dirigée par un vecteur \(\vec{u}\).",
            r"Cette droite est donc l'ensemble des points M tels que ",
            r"les vecteurs \(\overrightarrow{AM}\) et \(\vec{u}\) "
            r"sont colinéaires.",
            r"Formellement on écrit \(\overrightarrow{AM} = k\vec{u}\) "
            r"où \(k\in\mathbb{R}\).",
        ]

        rep_tex = [Tex(r) for r in rep]
        repVGroup = VGroup(*rep_tex)
        
        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=rep_tex,
            next2obj=title1,
            direction=DOWN
        )
        
        rep1 = [
            r"D'où le système d'équations : ",
            r"\((E_1) : x_{\overrightarrow{AM}} = kx_{\vec{u}}\)",
            r"\((E_2) : y_{\overrightarrow{AM}} = ky_{\vec{u}}\)",
            r"On obtient ainsi deux expressions du rapport ",
            r"de proportionnalité \(k\in\mathbb{R}\)",
            r"\((E_1) : k = \dfrac{x_{\overrightarrow{AM}}}{x_{\vec{u}}}\)",
            r"\((E_2) : k = \dfrac{y_{\overrightarrow{AM}}}{y_{\vec{u}}}\)"
        ]
        
        rep1_tex = [Tex(r) for r in rep1]
        rep1VGroup = VGroup(*rep1_tex)
        
        disp_tex_list(self, 
            previous_mobj=repVGroup,
            tex_list=rep1_tex,
            next2obj=title1,
            direction=DOWN
        )

        rep2 = [
            r"Normalement ça devrait vous rappeler le théorème de Thalès",
            r"En faisant un produit en croix on obtient : ",
            r"\(x_{\overrightarrow{AM}}y_{\vec{u}} - x_{\vec{u}}y_{\overrightarrow{AM}} = 0\)",
            r"C'est ce produit en croix qu'on nomme déterminant.",
            r"\(\det(\overrightarrow{AM}, \vec{u}) = \begin{vmatrix}"
            r"x_{\overrightarrow{AM}}&x_{\vec{u}}\\"
            r"y_{\overrightarrow{AM}}&y_{\vec{u}}\end{vmatrix}\)",
            r"D'où les équivalences :",
            r"\(\vec{u}\) et \(\vec{v}\) sont colinéaires ",
            r"équivalent à \(\det(\vec{u}, \vec{v}) = 0\)"
        ]

        rep2_tex = [Tex(r) for r in rep2]
        rep2VGroup = VGroup(*rep2_tex)
        
        disp_tex_list(self, 
            previous_mobj=rep1VGroup,
            tex_list=rep2_tex,
            next2obj=title1,
            direction=DOWN
        )

        
        
        rep3 = [
            r"Prenons un exemple concret avec \(A(-5 ; -2)\) ",
            r"et \(\vec{u}\begin{pmatrix}6\\4\end{pmatrix}\).",
            r"Calculons le déterminant : ",
            r"\(\det(\overrightarrow{AM}, \vec{u}) = \begin{vmatrix}"
            r"x - (-5)&6\\ y - (-2)&4\end{vmatrix}\)",
            r"\(\det(\overrightarrow{AM}, \vec{u}) = 0\iff "
            r"4(x + 5) - 6(y + 2) = 0\)",
            r"D'où une équation cartésienne de la droite "
            r"\(4x + 20 - 6y - 12 = 0\)",
        ]

        rep3_tex = [Tex(r) for r in rep3]
        rep3VGroup = VGroup(*rep3_tex)
        
        disp_tex_list(self, 
            previous_mobj=rep2VGroup,
            tex_list=rep3_tex,
            next2obj=title1,
            direction=DOWN
        )

        rep4 = [
            r"Ainsi la droite passant par \(A(-5 ; -2)\) ",
            r"et dirigée par \(\vec{u}\begin{pmatrix}6\\4\end{pmatrix}\)",
            r"admet pour équations cartésiennes :",
            r"\(4x - 6y + 8 = 0\iff 2x - 3y + 4 = 0\)",
        ]

        rep4_tex = [Tex(r) for r in rep4]
        rep4VGroup = VGroup(*rep4_tex)
        
        disp_tex_list(self, 
            previous_mobj=rep3VGroup,
            tex_list=rep4_tex,
            next2obj=title1,
            direction=DOWN
        )

        
        
        
class Subscribe(Scene):
    def construct(self):
        msg1 = "Abonnez-vous"
        title1 = Title(f"{msg1}")
        self.add(title1.scale(1))
        self.wait(2)

        credits_txt = [
            r"Animations réalisées par Laurent Garnier",
            r"Vous pouvez me contactez par mail "
            r"prenom.nom.superprofATgmail.com",
            r"si vous souhaitez travailler avec moi.",
            r"Merci pour votre attention."
        ]
        dCredits = [Tex(d).scale(0.75) for d in credits_txt]
        dCVGroup = VGroup(*dCredits)
        

        disp_tex_list(self, 
            previous_mobj=None,
            tex_list=dCredits,
            next2obj=title1,
            direction=DOWN
        )

        self.wait(2)

        disp_sub(self, lang="FR")
