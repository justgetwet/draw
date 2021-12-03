from bezier import Bezier
from affine import Affine
from array2d import array
import matplotlib.pyplot as plt
import math

fig = plt.figure(dpi=100, figsize=(4, 3))
ax = plt.gca()
ax.set_title("a jellyfish")
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
