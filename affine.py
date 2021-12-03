import math

class Array:

    def __init__(self, value):
        if isinstance(value, (Array, tuple, list)):
            if len(value) == 2:
                self._value = tuple(float(i) for i in value)
                self._i = 0
            else:
                raise ValueError("Array: Tow dimensions are required.")
        else:
            raise ValueError("Array: Tuple or List is required.")

    @property
    def value(self):
        return self._value

    def __iter__(self):
        # イテレータ list(), tuple()に対応
        return iter(self.value)

    def __next__(self):
        # イテレータ処理
        if self._i == len(self.value):
            raise StopIteration()
        value = self.value[self._i]
        self._i += 1

        return value

    def __len__(self):
        return len(self.value)

    def __str__(self):
        # print出力用
        return str(self.value)

    def __getitem__(self, i):
        # []でアクセスしたときの処理
        return self.value[i]

    def __add__(self, other):
        return self.array(tuple(x + y for x, y in zip(self.value, other.value)))

    def __sub__(self, other):
        return self.array(tuple(x - y for x, y in zip(self.value, other.value)))

    def __mul__(self, other):
        # array * 2
        return self.array(tuple(x * other for x in self.value))

    def __rmul__(self, other):
        # matrix * array (A * x) or 2 * array
        arr = None
        if isinstance(other, (tuple, list)):
            if [len(x) for x in other] == [2, 2]:
                arr = self.array(tuple(sum(a*b for a,b in zip(v, self.value)) for v in other))
            else:
                raise ValueError("2x2 List is required.")
        elif isinstance(other, (int, float)):
            arr = self.array(tuple(x * other for x in self.value))
        else:
            raise ValueError("2x2 List or Int or Float is required.")

        return arr

    def __truediv__(self, other):
        # array / 2
        return self.array(tuple(x / other for x in self.value))

    @staticmethod
    def array(p):
        return Array(p)

    @staticmethod
    def norm(p, q=None):
        if q is None:
            return (p[0]**2.0 + p[1]**2.0)**0.5
        else:
            return ((q[0]-p[0])**2.0 + (q[1]-p[1])**2.0)**0.5

    @staticmethod
    def dot(p, q):
        return p[0]*q[0] + p[1]*q[1]

    @staticmethod
    def cross2(p, q):
        a1, a2, a3 = *p, 0
        b1, b2, b3 = *q, 0
        vec = a2*a3-a3*b2, a3*b1-a1*b3, a1*b2-a2*b1

        return vec[2]

class Affine(Array):

    def affine_translate(self, p, move=(0., 0.)):
        x = self.array(p)
        b = self.array(move)
        A = [[1., 0.], 
            [0., 1.]]
        return tuple(A*x + b)

    def affine_scale(self, p, scale=(0., 0.), move=(0., 0.)):
        x = self.array(p)
        b = self.array(move)
        cx, cy = scale
        A = [[cx, 0.],
            [0., cy]]

        return tuple(A*x + b)

    def affine_rotate(self, p, rad=0., move=(0., 0.)):
        x = self.array(p)
        b = self.array(move)
        A = [[math.cos(rad), -math.sin(rad)],
            [math.sin(rad), math.cos(rad)]]

        return tuple(A*x + b)

    def affine_shear(self, p, shear=(0., 0.), move=(0., 0.)):
        x = self.array(p)
        b = self.array(move)
        sx, sy = shear
        A = [[1., math.tan(sx)], 
            [math.tan(sy), 1.]]
        
        return tuple(A*x + b)

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    
    fig = plt.figure(dpi=100, figsize=(4, 3))
    ax = plt.gca()
    ax.set_title("affine test")
    ax.set_xlim(0, 128)
    ax.set_ylim(0, 128)

    aff = Affine()

    a = (10, 10)
    b = aff.affine_translate(a, move=(10, 10))
    c = aff.affine_scale(b, scale=(3, 3))
    d = aff.affine_rotate(c, rad=math.pi/6)
    e = aff.affine_shear(c, shear=(math.pi/12, math.pi/12), move=(10, 10))
    
    ax.plot(*a, "ro")
    ax.plot(*b, "bo")
    ax.plot(*c, "x")
    ax.plot(*d, "*")
    ax.plot(*e, "s")
    
    plt.show()

