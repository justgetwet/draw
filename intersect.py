import math
from bezier import Bezier
# from equations import Equations
from array2d import array, norm, dot, cross2
# from affine import Array
from intersect_curveline import XcurveLine
from intersect_curves import Xcurves
from intersect_lines import Xlines

class Intersect(XcurveLine, Xcurves, Xlines):

    def intersections(self, nodes, othernodes):
        length = len(nodes) + len(othernodes)
        points, tvalues = [], []
        if length == 4:
            points, tvalues = self.intersection_of_two_lines(nodes, othernodes)
        elif length == 6:
            points, tvalues = self.intersections_of_curve_and_line(nodes, othernodes)
        elif length == 8:
            points, tvalues = self.intersections_of_two_curves(nodes, othernodes)
        else:
            print("intersections: nodes size error.")
    
        return points, tvalues

    def separate_nodes(self, nodes, tvalues, nodes_list=None):
        # t値のリストでnodesを分割する
        if not tvalues:
            nodes_list.append(nodes)
            return nodes_list
        
        if nodes_list is None:
            nodes_list = []
            new_tvalues = []            
            for i in range(len(tvalues)):
                if i==0:
                    new_tvalues.append(tvalues[0])
                else:
                    new_tvalue = (tvalues[i]-tvalues[i-1])/(1-tvalues[i-1])
                    new_tvalues.append(new_tvalue)
        else:
            new_tvalues = tvalues

        t = new_tvalues.pop(0)
        nodes0, nodes1 = self.split(nodes, t) # class Bezier
        nodes_list.append(nodes0)

        return self.separate_nodes(nodes1, new_tvalues, nodes_list)

    def separate_figure(self, figure, otherfigure):
        # otherfigureとの交点で分割したfiguerを返す
        nodes_and_tvalues = []
        points = []
        for nodes in figure:
            tvalues = []
            for othernodes in otherfigure:
                p, t = self.intersections(nodes, othernodes)
                if p:
                    points += p
                if t:
                    tvalues += t
            nodes_and_tvalues.append((nodes, sorted(tvalues)))

        separated_figure = []
        for nodes, tvalues in nodes_and_tvalues:
            if tvalues == []:
                separated_figure.append(nodes)
            else:
                nodes_list = self.separate_nodes(nodes, tvalues)
                separated_figure += nodes_list

        return tuple(points), tuple(separated_figure)
        
    def bar(self, nodes, t=0.1, length=256):
        # 内部にあるか判定するbar
        p = nodes[0]
        x, y = [], []
        if len(nodes) == 2:
            x, y = self.linear_bezier(nodes, t)
        if len(nodes) == 4:
            x, y = self.cubic_bezier(nodes, t)
        q = x[0], y[0]
        a = array(p) - array(q)
        b = array(q) + array([a[1], -a[0]]) * length

        return tuple(q), tuple(b)

    def is_inner(self, nodes, otherfigure):
        
        bar = self.bar(nodes)        
        points = []
        for othernodes in otherfigure:
            p, _ = self.intersections(bar, othernodes)
            points += p
            
        return len(points) % 2

    def combine_figures(self, figure, otherfigure):

        _, separated_figure = self.separate_figure(figure, otherfigure)
        _, separated_otherfigure = self.separate_figure(otherfigure, figure)
        
        separated_list = list(separated_figure)
        for nodes in separated_figure:
            if self.is_inner(nodes, otherfigure):
                separated_list.remove(nodes)
        
        separated_otherlist = list(separated_otherfigure)
        for nodes in separated_otherfigure:
            if self.is_inner(nodes, figure):
                separated_otherlist.remove(nodes)

        separated_figures = separated_list + separated_otherlist

        return separated_figures

    def cutout_figures(self, figure, otherfigure):
    
        _, separated_figure = self.separate_figure(figure, otherfigure)
        _, separated_otherfigure = self.separate_figure(otherfigure, figure)
        
        separated_list = list(separated_figure)
        for nodes in separated_figure:
            if self.is_inner(nodes, otherfigure):
                separated_list.remove(nodes)
        # inner parts of otherfigure
        separated_otherlist = []
        for nodes in separated_otherfigure:
            if self.is_inner(nodes, figure):
                separated_otherlist.append(nodes)

        separated_figures = separated_list + separated_otherlist

        return separated_figures
    
    def combine(self, figures, combi_figure=None):

        if not figures:
            return combi_figure
        
        if combi_figure is None:
            combi_figure = [figures.pop(0)]
        # print(math.dist(combi_figure[0][0], combi_figure[-1][-1]))
        # if math.dist(combi_figure[0][0], combi_figure[-1][-1]) < 0.0001:
        #     return combi_figure

        rm_nodes = None
        p = combi_figure[-1][-1]
        for nodes in figures:
            if math.dist(p, nodes[0]) < 0.0001:
                combi_figure.append(nodes)
                rm_nodes = nodes
            if math.dist(p, nodes[-1]) < 0.0001:
                combi_figure.append(nodes[::-1])
                rm_nodes = nodes

        if rm_nodes is not None:
            figures.remove(rm_nodes)

        return self.combine(figures, combi_figure)

    # def find_outside_nodes(self, figures, length=512):
    #     # 外側のnodesと、方向を見つける、分かりにくいコード
    #     direction = ""
    #     first_outside_nodes = ()
    #     for nodes in figures:
    #         p = array(self.t2point(nodes, 0.01))
    #         q = array(nodes[0])
    #         a = q - p
    #         h = length / math.dist(p, q)
    #         b = array([a[1], -a[0]]) * h
    #         c = array([-a[1], a[0]]) * h
    #         left_line = (tuple(p), tuple(p+b))
    #         right_line = (tuple(p), tuple(p+c))
    #         # print(math.dist(*left_line))
    #         othernodes_list = list(figures[::])
    #         othernodes_list.remove(nodes)
    #         ret_l, ret_r = [], []
    #         for othernodes in othernodes_list:
    #             _, left_t = self.intersections(left_line, othernodes)
    #             ret_l += left_t
    #             _, right_t = self.intersections(right_line, othernodes)
    #             ret_r += right_t
    #             if not len(ret_l) % 2:
    #                 first_outside_nodes = nodes
    #                 direction = "clockwise"
    #                 break
    #             if not len(ret_r) % 2:
    #                 first_outside_nodes = nodes
    #                 direction = "anti-clockwise"
    #                 break
    #         else:
    #             continue
    #         break

    #     return first_outside_nodes, direction

    # def combine_figures(self, figure, otherfigure):
    #     # 2つのnodesを合体させる
    #     figures = list(figure + otherfigure)
    #     nodes, direction = self.find_outside_nodes(figures)
    #     print(nodes)
    #     startpoint = nodes[0]
    #     cmb_figure = [nodes]
    #     nodes_list = []
    #     while True:
    #         if len(nodes_list) == 0:
    #             # print(nodes in figures)
    #             # print(nodes, "zzz", len(nodes_list))
    #             figures.remove(nodes)
    #         else:
    #             while nodes_list:
    #                 rm_nodes, _ = nodes_list.pop()
    #                 figures.remove(rm_nodes)
    #         for othernodes in figures:
    #             if math.dist(nodes[-1], othernodes[0]) < 0.0001:
    #                 nodes_list.append((othernodes, othernodes))
    #             elif math.dist(nodes[-1], othernodes[-1]) < 0.0001:
    #                 nodes_list.append((othernodes, othernodes[::-1]))
    #             else:
    #                 if len(figures) == 2:
    #                     print(nodes_list, nodes, "|", othernodes)
    #         if len(nodes_list) > 1:
    #             p = array(nodes[-1])
    #             q = array(self.t2point(nodes, 0.99))
    #             a = q - p
    #             rad_d = {}
    #             for _, othernodes in nodes_list:
    #                 p = array(othernodes[0])
    #                 q = array(self.t2point(othernodes, 0.01))
    #                 b = q - p
    #                 cos_theta = round(dot(a, b)/(norm(a)*norm(b)), 10)
    #                 # round 1.000000000000001の誤差をまるめる
    #                 # print(cos_theta)
    #                 r = math.acos(cos_theta)
    #                 if cross2(a, b) < 0:
    #                     r = 2 * math.pi - r
    #                 rad_d[r] = othernodes

    #             key = 0.
    #             if direction == "clockwise":
    #                 key = max(rad_d)
    #             if direction == "anti-clockwise":
    #                 key = min(rad_d)

    #             nodes = rad_d[key]
    #             # print(nodes, "xxx")
    #             cmb_figure.append(nodes)

    #         elif len(nodes_list) == 1:
    #             _, nodes = nodes_list[0]
    #             cmb_figure.append(nodes)

    #         if math.dist(nodes[-1], startpoint) < 0.0001:
    #             break
    #         # if len(figures) == 2:
    #         #     break

    #     return cmb_figure

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from figure import Figure

    fig = plt.figure(dpi=100, figsize=(4, 3))
    ax = plt.gca()
    ax.set_title("conbine")
    ax.set_xlim(0, 128)
    ax.set_ylim(0, 128)

    e = Figure()
    e.ell(40, 15, move=(45, 80))
    # e.show()
    e.rotate(20)
    x, y = e.plot()
    # ax.plot(x, y)

    r = Figure()
    r.rect(15, 40, move=(64, 64))
    x, y = r.plot()
    ax.plot(x, y)

    i = Intersect()
    c = Figure()
    efig = i.separate_figure(e.figure, r.figure)
    rfig = i.separate_figure(r.figure, e.figure)
    lst = i.combine_figures(efig, rfig)
    c.figure = lst
    x, y = c.plot()
    ax.plot(x, y)
    
    # for ls in ls1:
    #     c.figure = (ls,)
    #     x, y = c.plot()
    #     ax.plot(x, y)

    n1 = (8, 32), (32, 32)
    n2 = (32, 32), (32, 96), (96, 96), (96, 32)
    n3 = (96, 32), (120, 32)
    n4 = (120, 32), (128, 32), (128, 28), (120, 28)
    n5 = (120, 28), (8, 28)
    n6 = (8, 28), (0, 28), (0, 32), (8, 32)
    hat_data = [n1, n2, n3, n4, n5, n6]

    hat1 = Figure(hat_data).scale((0.9, 0.9)).rotate(10)
    # hat1 = Figure(hat_data).rotate(10)
    x, y = hat1.plot()
    # ax.plot(x, y, color="pink")

    hat2 = Figure(hat_data).scale((0.9, 0.9)).rotate(-20)
    x, y = hat2.plot()
    # ax.plot(x, y, color="cyan")

    # i = Intersect()
    # lst1 = i.separate_figure(hat1.figure, hat2.figure)
    # lst2 = i.separate_figure(hat2.figure, hat1.figure)
    # lst = i.combine_figures(lst1, lst2)

    # f = Figure()
    # f.figure = lst
    # x, y = f.plot()
    # ax.plot(x, y)



    # ls = ((82.58770483143633, 93.68080573302674), (80.17688355187624, 100.30448276095873), (65.9711280337156, 101.42670528659819), (49.0, 96.95984028868956)),
    # z = Figure()
    # z.figure = ls
    # x, y = z.plot()
    # ax.plot(x, y, color="red")

    plt.show()

    # nodes0 = (16, 32), (112, 96)
    # nodes0 = (16, 64), (32, 18), (64, 112), (112, 64)
    # x, y = Figure([nodes0]).plot()
    # ax.plot(x, y)

    # nodes1 = (16, 96), (112, 16)
    # # nodes1 = (16, 32), (32, 112), (64, 18), (112, 112)
    # x, y = Figure([nodes1]).plot()
    # ax.plot(x, y)

    # intercept = Intersect()
    # points, t = intercept.intersections(nodes0, nodes1)
    # for p in points:
    #     ax.plot(*p, "o")

    # plt.show()