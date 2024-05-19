from manim import *
import manim
from math import e, pi
import math
from PIL import Image

def disp_sub(self, lang):
    if lang.lower() == "en":
        written, phon = "Subscribe", "/səbˈskraɪb/"
        sub_pic = SVGMobject("/Users/dn/Documents/pics/svg/subscribe.svg")
        sub_scale = 0.8 
    elif lang.lower() == "fr":
        written, phon = "Abonnez-vous", "/abɔne vu/"
        sub_pic = ImageMobject("/Users/dn/Documents/pics/png/sabonner.png")
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
            
