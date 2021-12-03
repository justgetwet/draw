import matplotlib.pyplot as plt
from affine import Affine
from figure import Figure

class Shape(Affine):

  def ellipse(self, a, b, origin=(0., 0.)):
    m = 4 / 3 * (2 ** 0.5 - 1) * a
    n = 4 / 3 * (2 ** 0.5 - 1) * b
    q1 = ((a, 0), (a, n), (m, b), (0, b))
    q2 = tuple([self.affine_scale(p, (-1, 1)) for p in q1[::-1]])
    q3 = tuple([self.affine_scale(p, (1, -1)) for p in q2[::-1]])
    q4 = tuple([self.affine_scale(p, (-1, 1)) for p in q3[::-1]])
    ell = [q1, q2, q3, q4]

    if not origin == (0., 0.):
      points = [self.affine_translate(p, origin) for p in sum(ell, ())]
      figure = [tuple(points[i:i + 4]) for i in range(0, 15, 4)]
    else:
      figure = ell

    return figure

  # def rectangle(self, a, b, origin=(0., 0.)):
  #     """  """
  #   rect = [((a, b), (-a, b)), ((-a, b), (-a, -b)),
  #           ((-a, -b), (a, -b)), ((a, -b), (a, b))]

  #   if not origin == (0., 0.):
  #     lst = [self.affine_translate(p, origin) for p in sum(rect, ())]
  #     figure = [tuple(lst[i:i + 2]) for i in range(0, 7, 2)]
  #   else:
  #     figure = rect

  #   return figure

if __name__ == '__main__':

  fig = plt.figure(dpi=100, figsize=(4, 3))
  ax = plt.gca()
  ax.set_title("a ell")
  ax.set_xlim(-128, 128)
  ax.set_ylim(-128, 128)

  s = Shape()
  ell = s.ellipse(30, 40, (-30, -30))
  x, y = Figure(ell).plot()
  ax.plot(x, y, "pink")

  plt.show()