
def linear_equation(p, q):
    # ax + by + c = 0
    if p[0] == q[0]:
        a = 1.0
        b = 0.0
        c = float(-p[0])
    elif p[1] == q[1]:
        a = 0.0
        b = 1.0
        c = float(-p[1])
    else:
        slope = float(q[1]-p[1])/(q[0]-p[0])
        intercept = p[1] - slope*p[0]
        a = slope
        b = -1.0
        c = intercept
    
    return a, b, c

def quadratic_equation(a, b, c):

    x0, x1 = 0., 0.
    d = b**2 - 4*a*c
    if a == 0:
        if b == 0:
            return []
        x = -c / b
        return [x]
    if d == 0:
        x = -b / (2.0*a)
        return [x]
    if d < 0:
        return []
    else:
        x0 = (-b + d**0.5) / (2.0*a)
        x1 = (-b - d**0.5) / (2.0*a)

    return [x0, x1]

def cubic_equation(a,b,c,d):

    p = -b**2/(9.0*a**2) + c/(3.0*a)
    q = b**3/(27.0*a**3) - b*c/(6.0*a**2) + d/(2.0*a)
    t = complex(q**2+p**3)

    w =(-1.0 +1j*3.0**0.5)/2.0
    u = [0,0,0]
    u[0] = (-q +t**0.5)**(1.0/3.0)
    u[1] = u[0] * w
    u[2] = u[0] * w**2
    v = [0,0,0]
    v[0] = (-q -t**0.5)**(1.0/3.0)
    v[1] = v[0] * w
    v[2] = v[0] * w**2

    x_list = []
    for i in range(3):
        for j in range(3):
            if abs(u[i]*v[j] + p) < 0.0001:
                x = u[i] + v[j]
                if abs(x.imag) < 0.0000001:
                    x = x.real - b/(3.0*a)
                    x_list.append(x)

    return x_list



class Equations:

    def linear_equation(self, nodes):
        # ax + by + c = 0
        p0, p1 = nodes
        if p0[0] == p1[0]:
            a = 1.0
            b = 0.0
            c = float(-p0[0])
        elif p0[1] == p1[1]:
            a = 0.0
            b = 1.0
            c = float(-p0[1])
        else:
            slope = float(p1[1]-p0[1])/(p1[0]-p0[0])
            intercept = p0[1] - slope*p0[0]
            a = slope
            b = -1.0
            c = intercept
        
        return a, b, c

    def quadratic_equation(self, a, b, c):

        x0, x1 = 0., 0.
        d = b**2 - 4*a*c
        if a == 0:
            if b == 0:
                return []
            x = -c / b
            return [x]
        if d == 0:
            x = -b / (2.0*a)
            return [x]
        if d < 0:
            return []
        else:
            x0 = (-b + d**0.5) / (2.0*a)
            x1 = (-b - d**0.5) / (2.0*a)

        return [x0, x1]

    def cubic_equation(self, a,b,c,d):

        p = -b**2/(9.0*a**2) + c/(3.0*a)
        q = b**3/(27.0*a**3) - b*c/(6.0*a**2) + d/(2.0*a)
        t = complex(q**2+p**3)

        w =(-1.0 +1j*3.0**0.5)/2.0
        u = [0,0,0]
        u[0] = (-q +t**0.5)**(1.0/3.0)
        u[1] = u[0] * w
        u[2] = u[0] * w**2
        v = [0,0,0]
        v[0] = (-q -t**0.5)**(1.0/3.0)
        v[1] = v[0] * w
        v[2] = v[0] * w**2

        x_list = []
        for i in range(3):
            for j in range(3):
                if abs(u[i]*v[j] + p) < 0.0001:
                    x = u[i] + v[j]
                    if abs(x.imag) < 0.0000001:
                        x = x.real - b/(3.0*a)
                        x_list.append(x)

        return x_list


if __name__ == '__main__':

    ret = quadratic_equation(1,2,3) # 虚数解 []
    print(ret)