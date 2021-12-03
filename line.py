import matplotlib.pyplot as plt
import math
import numpy as np



def pythagoras_line(p, q, steps=100):

    dist = ((q[0]-p[0])**2 + (q[1]-p[1])**2)**0.5
    rad = math.atan2(q[1]-p[1], q[0]-p[0])

    t_list = [s / steps for s in range(steps + 1)]
    x, y = [], []
    for t in t_list:
        x.append(math.cos(rad) * dist * t + p[0])
        y.append(math.sin(rad) * dist * t + p[1])

    return x, y

def linear_bezier(p, q, steps=100):

  x, y = [], []
  for t in [s / steps for s in range(steps + 1)]:
    x.append((1-t)*p[0] + t*q[0])
    y.append((1-t)*p[1] + t*q[1])

  return x, y

def linear_bezier(p, q, steps=1000):

  points = [(1-t)*np.array(p) + t*np.array(q) for t in np.linspace(0, 1, steps+1)]

  return zip(*points)

def linear_bezier(p, q, steps=1000):
  
  t = np.linspace(0, 1, steps+1)
  x = (1-t)*p[0] + t*q[0]
  y = (1-t)*p[1] + t*q[1]

  return x, y

def linear_bezier(p, q, steps=10):
  # できta
  t = np.linspace(0, 1, steps+1)
  x, y = (1-t)*np.array([p]).T + t*np.array([q]).T

  return x, y

def linear_bezier(nodes, steps=10):

  p, q = nodes
  t = np.linspace(0, 1, steps+1)
  x, y = (1-t)*np.array([p]).T + t*np.array([q]).T

  # return zip(*zip(*p))
  return x, y



def cubic_bezier(nodes, steps=1000):

  p0, p1, p2, p3 = nodes
  x, y = [], []
  for t in [s / steps for s in range(steps + 1)]:
    x.append((1-t)**3*p0[0]+3*t*(1-t)**2*p1[0]+3*t**2*(1-t)*p2[0]+t**3*p3[0])         
    y.append((1-t)**3*p0[1]+3*t*(1-t)**2*p1[1]+3*t**2*(1-t)*p2[1]+t**3*p3[1])

  return x, y

def cubic_bezier(nodes, steps=1000):
  
  p0, p1, p2, p3 = np.array(nodes)
  p = []
  for t in np.linspace(0, 1, steps+1):
    p.append((1-t)**3*p0 + 3*t*(1-t)**2*p1 + 3*t**2*(1-t)*p2 + t**3*p3)

  return zip(*p)



def cubic_bezier(nodes, steps=1000):
  
  p0, p1, p2, p3 = nodes
  t = np.linspace(0, 1, steps+1)
  x = (1-t)**3*p0[0] + 3*t*(1-t)**2*p1[0] + 3*t**2*(1-t)*p2[0] + t**3*p3[0]
  y = (1-t)**3*p0[1] + 3*t*(1-t)**2*p1[1] + 3*t**2*(1-t)*p2[1] + t**3*p3[1]

  return x, y

def cubic_bezier_matrix(nodes, steps=1000):
  
  p0, p1, p2, p3 = nodes
  A = np.matrix([[1, 0, 0, 0],
                [-3, 3, 0, 0],
                [3, -6, 3, 0],
                [-1, 3, -3, 1]])
  px = np.array([[p0[0], p1[0], p2[0], p3[0]]])
  py = np.array([[p0[1], p1[1], p2[1], p3[1]]])
  # t = np.linspace(0, 1, steps+1)
  # a = np.array([[np.ones(steps+1), t, t**2, t**3]])

  x, y = [], []
  for t in np.linspace(0, 1, steps+1): # matrix.A1 -> arr
    x.append((np.array([[1, t, t**2, t**3]]) * A * px.T).A1[0])
    y.append((np.array([[1, t, t**2, t**3]]) * A * py.T).A1[0])

  return x, y

def cubic_bezier_bernstein(nodes, steps=1000):

  bernstein = lambda n, i, t: math.comb(n, i) * t**i * (1-t)**(n-i)
  points = []
  for t in [s / steps for s in range(steps + 1)]:
    n = len(nodes) - 1
    x, y = 0.0, 0.0
    for i, p in enumerate(nodes):
      x += bernstein(n, i, t) * p[0]
      y += bernstein(n, i, t) * p[1]
    points.append([x, y])

  return zip(*points)


if __name__ == '__main__':

  h1 = (25, 105), (60, 105)
  h2 = (60, 105), (60, 200), (190, 200), (190, 105)
  h3 = (190, 105), (225, 105)
  h4 = (225, 105), (250, 105), (250, 100), (225, 100)
  h5 = (225, 100), (25, 100)
  h6 = (25, 100), (0, 100), (0, 105), (25, 105)

  fig = plt.figure(dpi=100, figsize=(4, 4))
  ax = plt.gca()
  ax.set_title("a line")
  ax.set_xlim(0, 256)
  ax.set_ylim(0, 256)

  p, q = (5, 5), (250, 250)
  x, y = linear_bezier(h1)
  ax.plot(x, y)
  # x, y = pythagoras_line(p, q)
  x, y = cubic_bezier(h2)
  ax.plot(x, y)

  x, y = cubic_bezier_matrix(h2)
  ax.plot(x, y)

  ax.plot(*p, "o")
  ax.plot(*q, "o")

  plt.show()