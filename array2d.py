
class Array:

  def __init__(self, x):
    if isinstance(x, (Array, tuple, list)):
      if len(x) == 2:
        self.value = tuple(float(i) for i in x)
        self._i = 0
      else:
        raise ValueError("Array: Tow dimensions are required.")
    else:
      raise ValueError("Array: Tuple or List is required.")

  def __iter__(self):
    # イテレータ list(), tuple()に対応
    return iter(self.value)

  def __next__(self):
    # イテレータ処理
    if self._i == len(self.value):
      raise StopIteration()
    values = self.value[self._i]
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
    return Array(tuple(x + y for x, y in zip(self.value, other.value)))

  def __sub__(self, other):
    return Array(tuple(x - y for x, y in zip(self.value, other.value)))

  def __mul__(self, other):
    # array * 2
    return Array(tuple(x * other for x in self.value))

  def __rmul__(self, other):
    # matrix * array (A * x) or 2 * array
    arr = None
    if isinstance(other, (tuple, list)):
      if [len(x) for x in other] == [2, 2]:
        arr = Array(tuple(sum(a*b for a,b in zip(v, self.value)) for v in other))
      else:
        raise ValueError("2x2 List is required.")
    elif isinstance(other, (int, float)):
      arr = Array(tuple(x * other for x in self.value))
    else:
      raise ValueError("2x2 List or Int or Float is required.")

    return arr

  def __truediv__(self, other):
    # array / 2
    return Array(tuple(x / other for x in self.value))

def array(p):
  return Array(p)

def norm(p, q=None):
  n = 0.
  if q == None:
    a, b = p
    n = (a**2.0 + b**2.0)**0.5
  else:
    n = ((q[0]-p[0])**2.0 + (q[1]-p[1])**2.0)**0.5
  return n

def dot(p, q):
  return p[0]*q[0] + p[1]*q[1]

def cross2(p, q):
  a1, a2, a3 = *p, 0
  b1, b2, b3 = *q, 0
  vec = a2*a3-a3*b2, a3*b1-a1*b3, a1*b2-a2*b1
  return vec[2]


if __name__ == '__main__':

  import matplotlib.pyplot as plt
  import math

  a = array([2, 4])
  b = array((6, 7))
  print(a, b)
  c = a + b
  print(c)
  d = b - a
  print(d)
  e = d / 3
  print(e)
  f = 5 * e
  print(f)
  print(f[0])
  g = tuple(f)
  print(type(f), type(g), g)
  print(f * 3.3)
  A = [[1, 0], [0, 1]]
  print(A * a)

  theta = dot(a, b)/(norm(a)*norm(b))
  print(theta)
  r = math.acos(theta)
  print(math.degrees(r))

  fig = plt.figure(dpi=100, figsize=(4,3))
  ax = fig.gca()

  ax.plot([0, a[0]], [0, a[1]])
  ax.plot([0, b[0]], [0, b[1]])

  ax.annotate(text="", xy=a, xytext=(0, 0), arrowprops=dict(
    arrowstyle="-|>",
    facecolor='cyan', 
    edgecolor='cyan'
  ))
  ax.annotate(text="", xy=b, xytext=(0, 0), arrowprops=dict(
    arrowstyle="-|>",
    facecolor='magenta', 
    edgecolor='magenta'
  ))

  plt.show()