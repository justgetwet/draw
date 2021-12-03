import math
from equations import linear_equation, quadratic_equation, cubic_equation 

class XcurveLine:

    def coefficient(self, curve, line):
        p0, p1, p2, p3 = curve
        p, q = line
        a, b, c = linear_equation(p, q)
        f0 =      a * p0[0] + b * p0[1] + c
        f1 = 3 * (a * p1[0] + b * p1[1] + c)
        f2 = 3 * (a * p2[0] + b * p2[1] + c)
        f3 =      a * p3[0] + b * p3[1] + c

        return f0, f1, f2, f3

    def intersections_of_curve_and_line(self, nodes0, nodes1):

        if len(nodes0) == 4 and len(nodes1) == 2:
            curve, line = nodes0, nodes1
        elif len(nodes0) == 2 and len(nodes1) == 4:
            curve, line = nodes1, nodes0
        else:
            print("error: get_intersections_curvexline: ")
            return []

        p0, p1, p2, p3 = curve
        f0, f1, f2, f3 = self.coefficient(curve, line)

        a = -f0 + f1 - f2 + f3
        b = 3 * f0 - 2 * f1 + f2
        c = -3 * f0 + f1
        d = f0
    
        if a == 0:
            if b == 0:
                if c == 0: 
                    tlist = []
                else:
                    tlist = [-d/c]
            else:
                tlist = quadratic_equation(b,c,d)
        else:
            tlist = cubic_equation(a,b,c,d)

        _points = []
        _tlist = []
        for t in tlist:
            if t < 0 or 1 < t:
                continue
            x = (1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t**2*p2[0]+t**3*p3[0]
            y = (1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t**2*p2[1]+t**3*p3[1]
            _points.append((x,y))
            _tlist.append(t)
        # 線分上の点を選択
        index_of_points = []
        for i, p in enumerate(_points):
            min_x, max_x = min(line[0][0], line[1][0]), max(line[0][0], line[1][0])
            min_y, max_y = min(line[0][1], line[1][1]), max(line[0][1], line[1][1])
            if min_x < p[0] < max_x or min_y < p[1] < max_y:
                index_of_points.append(i)
        if not index_of_points:
            return [], []
        
        points = [_points[i] for i in index_of_points]

        tvalues = []
        if len(nodes0) == 4:
            tvalues = sorted([_tlist[i] for i in index_of_points])
        elif len(nodes0) == 2:
            line_tlist = [math.dist(line[0], p)/math.dist(*line) for p in points]
            tvalues = sorted(line_tlist)

        return points, tvalues

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from bezier import Bezier

    fig = plt.figure(dpi=100, figsize=(4, 3))
    ax = plt.gca()
    ax.set_title("intersection")
    ax.set_xlim(0, 128)
    ax.set_ylim(0, 128)

    b = Bezier()

    nodes0 = (30, 61), (125, 61)
    x, y = b.linear_bezier(nodes0)
    ax.plot(x, y)

    nodes1 = (16, 64), (32, 18), (64, 112), (112, 60)
    x, y = b.cubic_bezier(nodes1)
    ax.plot(x, y)

    c = XlineCurve()
    p, t= c.intersections_of_line_and_curve(nodes0, nodes1)
    print(p, t)
    for q in p:
        ax.plot(*q, "bo")

    plt.show()