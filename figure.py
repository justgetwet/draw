import copy
import math
import tkinter
from bezier import Bezier
from affine import Affine
from intersect import Intersect

class Figure(Affine, Intersect):

    STEPS = 100

    def __init__(self, figure=None):
        if figure is None:
            self._figure = (((0.,0.), (1.,1.)),)
        else:
            self._figure = figure

    @property
    def figure(self):
        return self._figure

    @figure.setter
    def figure(self, figure):
        self._figure = figure

    def copy(self):
        return copy.deepcopy(self)

    def ell(self, a, b, move=(0., 0.)):
        m = 4 / 3 * (2 ** 0.5 - 1) * a
        n = 4 / 3 * (2 ** 0.5 - 1) * b
        q1 = (a, 0), (a, n), (m, b), (0, b)
        q2 = (0, b), (-m, b), (-a, n), (-a, 0)
        q3 = (-a, 0), (-a, -n), (-m, -b), (0, -b)
        q4 = (0, -b), (m, -b), (a, -n), (a, 0)
        ellipse = q1, q2, q3, q4

        if not move == (0., 0.):
            q = [self.affine_translate(p, move) for p in sum(ellipse, ())]
            ellipse = tuple(tuple(q[i:i+4]) for i in range(0, 15, 4))
        
        self._figure = ellipse

    def rect(self, a, b, move=(0., 0.)):

        rect = ((a, b), (-a, b)), ((-a, b), (-a, -b)), ((-a, -b), (a, -b)), ((a, -b), (a, b))
        
        if not move == (0., 0.):
            q = [self.affine_translate(p, move) for p in sum(rect, ())]
            rect = tuple(tuple(q[i:i + 2]) for i in range(0, 7, 2))

        self._figure = rect


    def show(self, width=256, height=256):
        root = tkinter.Tk()
        root.geometry(f"{width}x{height}+{150}+{150}")
        canvas = tkinter.Canvas(root,width=width,height=height)
        canvas.pack()

        x, y = self.plot()
        plot = tuple(zip(x, y))
        canvas.create_line(plot)

        root.mainloop()

    def plot(self, steps=STEPS):
        x, y = [], []
        for nodes in self.figure:
            line = [], []
            if len(nodes) == 2:
                line = self.linear_bezier(nodes, steps=steps)
            if len(nodes) == 4:
                line = self.cubic_bezier(nodes, steps=steps)
            x += line[0]
            y += line[1]

        return x, y

    def reflection(self, y_range):
        figure = tuple(tuple((p[0], y_range-p[1]) for p in nodes) for nodes in self._figure)
        self.figure = figure
        return self

    # def tkplot(self):
    #     x, y = self.plot()
    #     return tuple(zip(x, y))

    def to_dic(self, key):
        return { key: self.figure }

    def centerpoint(self):
        # k 個の点 x1, x2, xk ∈ Rn の成す有限集合の幾何中心(wikipedia)
        x, y = self.plot(steps=20)
        p = sum(x), sum(y)
        cp = self.array(p) / len(x)
        return tuple(cp)

    def move(self, m=(0., 0.)):
        figure = []
        for nodes in self.figure:
            move_nodes = tuple(self.affine_translate(p, m) for p in nodes)
            figure.append(move_nodes)
        self.figure = tuple(figure)
        return self
    
    def scale(self, scale=(0., 0.)):
        cx, cy = self.centerpoint()
        figure = []
        for nodes in self._figure:
            origin_nodes = [self.affine_translate(p, (-cx, -cy)) for p in nodes]
            scale_nodes = tuple(self.affine_scale(p, scale, (cx, cy)) for p in origin_nodes)
            figure.append(scale_nodes)
        self.figure = tuple(figure)
        return self

    def reflect(self, axis="x"):
        cx, cy = self.centerpoint()
        rx, ry = 1, -1
        if axis == "y":
            rx, ry = -1, 1
        figure = []
        for nodes in self._figure:
            origin_nodes = [self.affine_translate(p, (-cx, -cy)) for p in nodes]
            reflect_nodes = tuple(self.affine_scale(p, (rx, ry), (cx, cy)) for p in origin_nodes)
            figure.append(reflect_nodes)
        self.figure = tuple(figure)
        return self

    def rotate(self, angle=0.):
        rad = math.radians(angle)
        cx, cy = self.centerpoint()
        figure = []
        for nodes in self._figure:
            origin_nodes = [self.affine_translate(p, (-cx, -cy)) for p in nodes]
            rotate_nodes = tuple(self.affine_rotate(p, rad, (cx, cy)) for p in origin_nodes)
            figure.append(rotate_nodes)
        self.figure = tuple(figure)
        return self

    def shear(self, shear=(0., 0.)):
        cx, cy = self.centerpoint()
        shear = [math.radians(d) for d in shear]
        figure = []
        for nodes in self._figure:
            origin_nodes = [self.affine_translate(p, (-cx, -cy)) for p in nodes]
            shear_nodes = tuple(self.affine_shear(p, shear, (cx, cy)) for p in origin_nodes)
            figure.append(shear_nodes)
        self.figure = tuple(figure)
        return self

    def _join(self, other):
        c, d = self.figure[-1][-2:]
        rad1 = math.atan2(c[1]-d[1], c[0]-d[0])
        a, b = other.figure[0][:2]
        rad2 = math.atan2(b[1]-a[1], b[0]-a[0])
        deg = math.degrees(rad1 - rad2 + math.pi)
        other.rotate(deg)
        e, _ = other.figure[0][:2]
        mx, my = d[0]-e[0], d[1]-e[1]
        other.move((mx, my))
        self.figure = self.figure + other.figure
        return self

    def reverse(self):
        self.figure = tuple(nodes[::-1] for nodes in self._figure)[::-1]
        return self

    def join(self, other, joint="tail_to_head"):
        
        is_reverse = False
        if joint == "tail_to_head":
            pass
        elif joint == "tail_to_tail":
            other.reverse()
        elif joint == "head_to_head":
            self.reverse()
            is_reverse = True
        elif joint == "head_to_tail":
            other.reverse()
            self.reverse()
            is_reverse = True
        else:
            print("error")

        self._join(other)
        if is_reverse:
            self.reverse()

        return self
    
    def length_of_figure(self, figure, steps=1000):
        lengths = []
        for nodes in figure:
            length = 0.
            q = None
            for t in [s / steps for s in range(steps + 1)]:
                if q is None:
                    q = self.split(nodes, t)[0][0]
                p = self.split(nodes, t)[0][-1]
                length += math.dist(q, p)
                q = p
            lengths.append(length)

        return lengths

    def cut(self, t=0.5, leave="head", steps=STEPS):
        lengths = self.length_of_figure(self._figure)
        cut_size = sum(lengths) * t
        idx = 0
        nodes0, nodes1 = [], []
        for i, length in enumerate(lengths):
            cut_size -= length
            if cut_size < 0:
                c_length = length + cut_size
                nodes = self._figure[i]
                q = None
                n_length = 0.
                for t in [s / steps for s in range(steps + 1)]:
                    p = self.split(nodes, t)[0][-1]
                    if q is not None:
                        n_length += math.dist(q, p)
                    q = p
                    if n_length > c_length:
                        nodes0, nodes1 = self.split(nodes, t)
                        idx = i
                        break
                else:
                    continue
                break
            else:
                continue
            break
    
        if leave == "head":
            self.figure = self._figure[:idx] + (nodes0,)
        if leave == "tail":
            self.figure = (nodes1,) + self._figure[idx+1:]

        return self

    def combi(self, other):
        
        figures = self.combine_figures(self.figure, other.figure)
        self.figure = self.combine(figures)

        return self

    def close(self):
        figure = []
        q = self._figure[-1][-1]
        for nodes in self._figure:
            p = nodes[0]
            if q == p:
                figure.append(nodes)
            elif q != p and math.dist(q, p) < 0.0001:
                figure.append(q + nodes[1:])
            elif q != p and math.dist(q, p) > 0.0001:
                figure.append((q, p))
                figure.append(nodes)
            else:
                pass
            q = nodes[-1]
        self.figure = figure
        return self

def write_svg(filename, dic, width=256, height=256, reverse=False):
    tags = []
    for key, figure in dic.items():
        if reverse:
            figure = [[(p[0], height - p[1]) for p in nodes] for nodes in figure.fugure]
        path = ""
        for nodes in figure:
            if not path:
                p0_x, p0_y = nodes[0]
                path += f"M {p0_x} {p0_y} "
            if len(nodes) == 2:
                p1_x, p1_y = nodes[1]
                path += f"L {p1_x} {p1_y} "
            if len(nodes) == 4:
                p1_x, p1_y, p2_x, p2_y, p3_x, p3_y = sum(nodes[1:], ())
                path += f"C {p1_x} {p1_y} {p2_x} {p2_y} {p3_x} {p3_y} "
        if p0_x == p3_x and p0_y == p3_y:
            path += "z"
        tag = f"    <path class='{key}' d='" + path + "' fill='none' stroke='black' />"
        tags.append(tag)
    
    txt = "<html>\n<head>\n"
    txt += "    <link rel='stylesheet' href='icon.css'/>\n</head>\n"
    txt += f"<svg width='{width}' height='{height}' viewBox='0 0 {width} {height}' xmlns='http://www.w3.org/2000/svg' version='1.1'>\n"
    for tag in tags:
        txt += tag + "\n"
    txt += "</svg>\n"
    txt += "</html>"

    with open(filename, mode='w') as f:
        f.write(txt)


def show_tk(*figures, width=256, height=256):
    root = tkinter.Tk()
    root.geometry(f"{width}x{height}+{150}+{150}")
    canvas = tkinter.Canvas(root,width=width,height=height)
    canvas.pack()
    for figure in figures:
        x, y = figure.plot()
        p = tuple(zip(x, y))
        canvas.create_line(p)

    root.mainloop()

if __name__ == '__main__':

    # from Figure import show_tk, write_svg

    circle = Figure()
    circle.ell(126, 126, (128, 128))

    m = 150, 85
    body = Figure()
    body.ell(60, 50)
    body.move(m)
    body.cut(leave="tail")

    b = Figure()
    b.ell(60, 30)
    b.move(m)
    b.cut(leave="head")

    body.join(b)
    body.scale((0.9, 0.9))
    body.rotate(26)
    

    reg1 = Figure()
    t1 = ((128, 64+8), (96, 64-30+8), (64, 64+30+8), (32, 64+6))
    t2 = ((32, 64+6),(32-6, 64+6-6), (32-6, 64-6), (32, 64))
    reg1.figure = (t1, t2, ((32, 64), (64, 64+30), (96, 64-30), (128, 64)))
    reg1.rotate(-70)
    reg1.scale((1.2, 1.2))
    reg1.move((54+10, 112))
    # reg1.show()
    # show_tk(circle, e1)
    reg2 = reg1.copy()
    reg2.move((0, 12))
    reg2.scale((1., 1.2))
    reg2.close()

    reg1.move((28-6, 6))
    reg1.rotate(-10)
    reg1.close()

    reg3 = Figure()
    t1 = ((128, 64+8), (96, 64+30+8), (64, 64+30+8), (32, 64+6))
    t2 = ((32, 64+6),(32-6, 64+6-6), (32-6, 64-6), (32, 64))
    reg3.figure = (t1, t2, ((32, 64), (64, 64+30), (96, 64+30), (128, 64)))
    reg3.rotate(-112)
    reg3.reflect("y")
    reg3.move((36, 88))
    reg3.reflect("y")
    reg3.scale((1.2, 0.8))
    reg3.rotate(90)
    reg3.move((-21, -36))
    reg3.close()

    reg4 = Figure()
    t1 = ((178, 64+6+1), (96, 64+9), (64, 64+9-6), (32, 64+6))
    t2 = ((32, 64+6),(32-6, 64+6), (32-6, 64), (32, 64))
    t3 = ((32, 64), (64, 64-6), (96, 64), (178, 64-1))
    reg4.figure = (t1, t2, t3)
    reg4.move((20, 129))
    reg4.rotate(-66) 
    reg4.close()

    f = "./test.svg"
    dic = {"circle": circle.figure, 
        "reg1": reg1.figure, 
        "reg2": reg2.figure,
        "reg3": reg3.figure,
        "reg4": reg4.figure,
        "body": body.figure,
        }
    write_svg(f, dic)

    # h1 = (25, 150), (60, 150)
    # h2 = (60, 150), (60, 55), (190, 55), (190, 150)
    # h3 = (190, 150), (225, 150)
    # h4 = (225, 150), (250, 150), (250, 155), (225, 155)
    # h5 = (225, 155), (25, 155)
    # h6 = (25, 155), (0, 155), (0, 150), (25, 150)
    # hat_reflect = [h1, h2, h3, h4, h5, h6]

    # h1 = (25, 105), (60, 105)
    # h2 = (60, 105), (60, 200), (190, 200), (190, 105)
    # h3 = (190, 105), (225, 105)
    # h4 = (225, 105), (250, 105), (250, 100), (225, 100)
    # h5 = (225, 100), (25, 100)
    # h6 = (25, 100), (0, 100), (0, 105), (25, 105)

    # hat_data = (h1, h2, h3, h4, h5, h6)

    # # hat = Figure(hat_data)
    # hat = Figure()
    # hat.figure = hat_data

    # # hat.reflect().move((0, 33.3))

    # # hat.move((0, 20))
    # # hat.scale((0.9, 0.9))
    # # hat.rotate(60)
    # # hat.reflect(axis="x")
    # # hat.shear((30, 30))
    # import matplotlib.pyplot as plt
    
    # fig = plt.figure(dpi=100, figsize=(4, 4))
    # ax = plt.gca()
    # ax.set_title("a hat")
    # ax.set_xlim(0, 256)
    # ax.set_ylim(0, 256)

    # x, y = hat.plot()
    # # ax.plot(x, y)

    # hatt = Figure([h1, h2, h3])
    # x, y = hatt.plot()
    # # ax.plot(x, y)
    
    # hatt.cut(t=0.7, leave="tail")
    # x, y = hatt.plot()
    # # ax.plot(x, y)
    # print(hat.test())
    # h = hat.figure[:-1]
    # hatt = Figure(h)
    # x, y = hatt.close().plot()
    # ax.plot(x, y)
    # cp = hatt.centerpoint()
    # ax.plot(*cp, "ro")
    # plt.show()

    #   x, y = Figure().shape().plot()
    #   ax.plot(x, y)

    # fig1 = Figure([h2]).move((-30, 10))
    # x, y = fig1.plot()
    # ax.plot(x, y)

    # fig4 = Figure([h4])

    # fig2 = Figure([h6]).rotate(30).scale((0.7, 1.3))
    # x, y = fig2.plot()
    # ax.plot(x, y)

    # fig1.join(fig4, joint="head_to_head").move((0, 30))
    # x, y = fig1.plot()
    # ax.plot(x, y)
    # ax.plot(x[0], y[0], "o")
    
    # x, y = hat.plot()
    # ax.plot(x, y, color="brown")

    # cx, cy = hat.centerpoint()
    # ax.plot(cx, cy, "o", color="red")

    # d = Draw()
    # print(d.split(h1, 0.25))

    # import tkinter
    # root = tkinter.Tk()
    # root.title("a hat")
    # canvas = tkinter.Canvas(root,width=256,height=256)
    # canvas.pack()

    # # plot = hat.reflection(256).tkplot()
    # plot = Figure(hat_reflect).tkplot()
    # canvas.create_line(plot)

    # root.mainloop()

    # plt.show()
    # plt.savefig('straight.png')
    