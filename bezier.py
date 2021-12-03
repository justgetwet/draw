from equations import quadratic_equation

class Bezier:

    STEPS = 100

    def linear_bezier(self, nodes, t_value=None, steps=STEPS):
        p0, p1 = nodes

        t_values = [t_value]
        if t_value is None:
            t_values = [s / steps for s in range(steps + 1)]

        x, y = [], []
        for t in t_values:
            x.append((1-t)*p0[0] + t*p1[0])
            y.append((1-t)*p0[1] + t*p1[1])

        return x, y

    def cubic_bezier(self, nodes, t_value=None, steps=STEPS):
        p0, p1, p2, p3 = nodes
        
        t_values = [t_value]
        if t_value is None:
            t_values = [s / steps for s in range(steps + 1)]

        x, y = [], []
        for t in t_values:
            x.append((1-t)**3*p0[0]+3*t*(1-t)**2*p1[0]+3*t**2*(1-t)*p2[0]+t**3*p3[0])
            y.append((1-t)**3*p0[1]+3*t*(1-t)**2*p1[1]+3*t**2*(1-t)*p2[1]+t**3*p3[1])

        return x, y

    def de_casteljau(self, nodes, t):
        q = []
        prev_p = None
        for p in nodes:
            if prev_p is not None:
                x = (1-t)*prev_p[0] + t*p[0]
                y = (1-t)*prev_p[1] + t*p[1]
                q.append((x, y))
            prev_p = p

        if len(q) == 1:
            return [q]

        return [q] + self.de_casteljau(q, t)

    def split(self, nodes, t=0.5):

        points = [nodes] + self.de_casteljau(nodes, t)
        nodes0 = tuple(p[0] for p in points)
        nodes1 = tuple(p[-1] for p in points)[::-1]
        
        return nodes0, nodes1

    def bounding(self, nodes):
        """ the bounding box (left, bottom, right, top) """
        if len(nodes) == 2:
            p, q = nodes
            x, y = (p[0], q[0]), (p[1], q[1])
            return min(x), min(y), max(x), max(y)

        p0, p1, p2, p3 = nodes
        bounds = [[], []]
        bounds[0] += p0[0], p3[0]
        bounds[1] += p0[1], p3[1]
        
        for i in [0, 1]:

            f = lambda t: (1-t)**3*p0[i]+3*t*(1-t)**2*p1[i]+3*t**2*(1-t)*p2[i]+t**3*p3[i]
            a = float(-3 * p0[i] + 9 * p1[i] - 9 * p2[i] + 3 * p3[i])  # -3*p0 + 9*p1 - 9*p2 + 3*p3
            b = float(6 * p0[i] - 12 * p1[i] + 6 * p2[i])  # 6*p0 - 12*p1 + 6*p2
            c = float(-3 * p0[i] + 3 * p1[i])  # -3*p0 + 3*p1

            t_list = quadratic_equation(a, b, c)
            for t in t_list:
                if 0.0 < t < 1.0:
                    p = f(t)
                    bounds[i].append(p)

        return min(bounds[0]), min(bounds[1]), max(bounds[0]), max(bounds[1])

    def boundingbox(self, nodes):

        left, bottom, right, top = self.bounding(nodes)
        
        return (left, bottom), (left, top), (right, top), (right, bottom) 


if __name__ == '__main__':


    import matplotlib.pyplot as plt
    from bezier import Bezier

    fig = plt.figure(dpi=100, figsize=(4, 3))
    ax = plt.gca()
    ax.set_title("intersection")
    ax.set_xlim(0, 128)
    ax.set_ylim(0, 128)
    
    b = Bezier()
    nodes = (8, 128), (128, 192), (128, 64), (248, 128)
    nodes = (16, 64), (32, 18), (64, 112), (112, 64)
    x, y = b.cubic_bezier(nodes)
    ax.plot(x, y)

    bound = b.boundingbox(nodes)
    for p in bound:
        ax.plot(*p, ".")

    plt.show()

    # import tkinter

    # root = tkinter.Tk()
    # root.title("bezier")
    # canvas = tkinter.Canvas(root,width=256,height=256)
    # canvas.pack()

    # b = Bezier()
    # nodes = (8, 128), (128, 192), (128, 64), (248, 128)
    
    # x, y = b.cubic_bezier(nodes) 
    # p = tuple(zip(x, y))
    # canvas.create_line(p)

    # x, y = b.linear_bezier(nodes[:2]) 
    # p = tuple(zip(x, y))
    # canvas.create_line(p)

    # x, y = b.linear_bezier(nodes[2:]) 
    # p = tuple(zip(x, y))
    # canvas.create_line(p)

    # root.mainloop()