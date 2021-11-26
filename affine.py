import math
from array2d import array

class Affine:

  def affine_translate(self, p, move=(0., 0.)):
    x = array(p)
    b = array(move)
    A = [[1., 0.], 
        [0., 1.]]

    return tuple(A*x + b)

  def affine_scale(self, p, scale=(0., 0.), move=(0., 0.)):
    x = array(p)
    b = array(move)
    cx, cy = scale
    A = [[cx, 0.],
        [0., cy]]

    return tuple(A*x + b)

  def affine_rotate(self, p, rad=0., move=(0., 0.)):
    x = array(p)
    b = array(move)
    A = [[math.cos(rad), -math.sin(rad)],
        [math.sin(rad), math.cos(rad)]]
    
    return tuple(A*x + b)

  def affine_shear(self, p, shear=(0., 0.), move=(0., 0.)):
    x = array(p)
    b = array(move)
    sx, sy = shear
    A = [[1., math.tan(sx)], 
        [math.tan(sy), 1.]]
                        
    return tuple(A*x + b)

if __name__ == '__main__':

  import matplotlib.pyplot as plt
  
  fig = plt.figure(dpi=100, figsize=(4, 3))
  ax = plt.gca()
  ax.set_title("a hat")
  ax.set_xlim(0, 128)
  ax.set_ylim(0, 128)

  aff = Affine()

  a = (10, 10)
  b = aff.affine_translate(a, move=(10, 10))
  c = aff.affine_scale(a, scale=(3, 3))
  d = aff.affine_rotate(c, rad=math.pi/6)
  e = aff.affine_shear(c, shear=(math.pi/12, math.pi/12), move=(10, 10))
  
  # tkplot([a, b, c, d, e])

  ax.plot(*a, "o")
  ax.plot(*b, "o")
  ax.plot(*c, "x")
  ax.plot(*d, "*")
  ax.plot(*e, "s")
  
  plt.show()

