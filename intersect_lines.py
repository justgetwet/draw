from array2d import array, norm, cross2
import numpy as np
import math

class Xlines:
    
    def is_intersect(self, nodes0, nodes1):

        a, b = [array(p) for p in nodes0]
        c, d = [array(p) for p in nodes1]
        # ab case
        AB = b - a
        AC = c - a
        AD = d - a
        # cd case
        CD = d - c
        CA = a - c
        CB = b - c

        ab_case = cross2(AB, AC) * cross2(AB, AD) < 0
        cd_case = cross2(CD, CA) * cross2(CD, CB) < 0
        parallel = cross2(AB, CD) == 0
        # print(ab_case, cd_case, not_parallel)
        return (ab_case and cd_case) and not parallel

    def distance_from_point_to_line(self, nodes, p):

        a, b = [array(q) for q in nodes]
        AB = b - a
        AP = array(p) - a

        return abs(cross2(AB, AP) / norm(a, b))

    def _intersection_of_two_lines(self, nodes0, nodes1):

        p, t = [], []
        if self.is_intersect(nodes0, nodes1):      
            a, b = [array(q) for q in nodes0]
            c, d = [array(q) for q in nodes1]
            nc = self.distance_from_point_to_line(nodes0, c)
            nd = self.distance_from_point_to_line(nodes0, d)
            rat = nd / (nc+nd)
            if cross2(b-a, d-c) < 0:
                rat = nc / (nc+nd)
            t.append(rat)
            p.append(tuple((1-rat)*a + rat*b))

        return p, t

    def intersection_of_two_lines(self, nodes0, nodes1):
            # 内積を用いた交点計算
        # dot = lambda p, q : sum([px*qx for px,qx in zip(p,q)])
        # normarize = lambda x: x[0]/math.dist(x[0],x[1]), x[1]/math.dist(x[0],x[1])
        if not self.is_intersect(nodes0, nodes1):
            return [], []
        dot = lambda p, q: np.dot(p, q)
        normarize = lambda x: x / np.linalg.norm(x)
        a, b = nodes0
        c, d = nodes1
        A, B = np.array(a), np.array(b)
        C, D = np.array(c), np.array(d)
        AB = B - A
        CD = D - C
        n1 = normarize(AB)
        n2 = normarize(CD)
        w1 = dot(n1, n2)
        w2 = 1 - w1 * w1

        AC = C - A
        d1 = (dot(n1, AC) - w1 * dot(n2, AC)) / w2
        d2 = (w1 * dot(n1, AC) - dot(n2, AC)) / w2

        p1 = A + d1*n1
        p2 = C + d2*n2

        return [tuple(p1)], [d1/math.dist(a, b)]


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from bezier import Bezier

    fig = plt.figure(dpi=100, figsize=(4, 3))
    ax = plt.gca()
    ax.set_title("intersection")
    ax.set_xlim(0, 128)
    ax.set_ylim(0, 128)
    
    c = Xlines()
    b = Bezier()
    node0 = (3, 6), (100, 120)
    node1 = (3, 90), (100, 6)

    x, y = b.linear_bezier(node0)
    ax.plot(x, y)

    x, y = b.linear_bezier(node1)
    ax.plot(x, y)

    p = (98, 98)
    ax.plot(*p, "ro")

    res = c.is_intersect(node0, node1)
    print(res)

    res = c.distance_from_point_to_line(node1, p)
    print(res)

    q, t = c.intersection_of_two_lines(node0, node1)
    print(q, t)
    ax.plot(*q[0], "bo")

    plt.show()
