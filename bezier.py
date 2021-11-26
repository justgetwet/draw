
class Bezier:

  STEPS = 100

  def linear_bezier(self, nodes, steps=STEPS):
  
    p0, p1 = nodes
    x, y = [], []
    for t in [s/steps for s in range(steps+1)]:
      x.append((1-t)*p0[0] + t*p1[0])
      y.append((1-t)*p0[1] + t*p1[1])

    return x, y

  def cubic_bezier(self, nodes, steps=STEPS):
  
    p0, p1, p2, p3 = nodes
    x, y = [], []
    for t in [s/steps for s in range(steps+1)]:
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

if __name__ == '__main__':

  import tkinter

  root = tkinter.Tk()
  root.title("bezier")
  canvas = tkinter.Canvas(root,width=256,height=256)
  canvas.pack()

  b = Bezier()
  nodes = (8, 128), (128, 192), (128, 64), (248, 128)
  
  x, y = b.cubic_bezier(nodes) 
  p = tuple(zip(x, y))
  canvas.create_line(p)

  x, y = b.linear_bezier(nodes[:2]) 
  p = tuple(zip(x, y))
  canvas.create_line(p)

  x, y = b.linear_bezier(nodes[2:]) 
  p = tuple(zip(x, y))
  canvas.create_line(p)

  root.mainloop()