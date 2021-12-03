import unittest
from intersect import Intersect

class TestSepareteFigure(unittest.TestCase):

    def test_sepate_nodes(self):
        x = Intersect()
        nodes0 = (8.0, 64.0), (32.0, 8.0), (78.0, 120.0), (120.0, 64.0)
        nodes1 = (8.0, 26.0), (32.0, 78.0), (78.0, 120.0), (120.0, 32.0)
        points, tvalues = x.intersections(nodes0, nodes1)
        nodes_list = x.separate_nodes(nodes0, tvalues)

        self.assertEqual(2, len(points))
        self.assertEqual(3, len(nodes_list))

    # def test_sparate_figure(self):
    #     pass


if __name__ == '__main__':

    # unittest.main()

    import matplotlib.pyplot as plt
    from figure import Figure

    fig = plt.figure(dpi=100, figsize=(4, 3))
    ax = plt.gca()
    ax.set_title("separate figure")
    ax.set_xlim(0, 128)
    ax.set_ylim(0, 128)

    ict = Intersect()

    # nodes0 = (8.0, 64.0), (32.0, 8.0), (78.0, 120.0), (120.0, 64.0)
    # nodes1 = (8.0, 26.0), (32.0, 78.0), (78.0, 120.0), (120.0, 32.0)
    # points, tvalues = ict.intersections(nodes0, nodes1)
    # nodes_list = ict.separate_nodes(nodes0, tvalues)

    ell = Figure()
    ell.ell(30, 20, move=(64, 72))
    x, y = ell.plot()
    # ax.plot(x, y)

    rect = Figure()
    rect.rect(20, 30, move=(64, 42))
    x, y = rect.plot()
    # ax.plot(x, y)

    points, nodes_list = ict.separate_figure(ell.figure, rect.figure)
    
    # for nodes in nodes_list:
    #     x, y = Figure((nodes,)).plot()
    #     ax.plot(x, y)

    # for p in points:
    #     ax.plot(*p, "x")

    nodes = nodes_list[2]
    bar = ict.bar(nodes)

    x, y = Figure((nodes, )).plot()
    # ax.plot(x, y)

    x, y = Figure((bar,)).plot()
    # ax.plot(x, y)    

    res = ict.is_inner(nodes, rect.figure)
    print(res)

    x, y = ell.plot()
    # ax.plot(x, y)
    
    figures = ict.combine_figures(ell.figure, rect.figure)
    # figures = ict.cutout_figures(rect.figure, ell.figure)
    f = ict.combine(figures)
    x, y = Figure(f).plot()
    ax.plot(x, y)

    plt.show()
