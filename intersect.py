import math
from bezier import Bezier
from equations import Equations
from array2d import array, norm, dot, cross2

class Xlines:
  
  def is_intersect(self, nodes0, nodes1):

    a, b = [array(p) for p in nodes0]
    c, d = [array(p) for p in nodes1]
    # ab case
    AB = b - a
    AC = c - a
    AD = d - a
    # cd case
    CD = d - c
    CA = a - c
    CB = b - c

    ab_case = cross2(AB, AC) * cross2(AB, AD) < 0
    cd_case = cross2(CD, CA) * cross2(CD, CB) < 0
    parallel = cross2(AB, CD) == 0
    # print(ab_case, cd_case, not_parallel)
    return (ab_case and cd_case) and not parallel

  def distance_from_point_to_line(self, nodes, p):

    a, b = [array(q) for q in nodes]
    AB = b - a
    AP = array(p) - a

    return abs(cross2(AB, AP) / norm(a, b))

  def intersections_lines(self, nodes0, nodes1):

    p = []
    if self.is_intersect(nodes0, nodes1):      
      a, b = [array(q) for q in nodes0]
      c, d = [array(q) for q in nodes1]
      nc = self.distance_from_point_to_line(nodes0, c)
      nd = self.distance_from_point_to_line(nodes0, d)
      t = nd / (nc+nd)
      if cross2(b-a, d-c) < 0:
        t = nc / (nc+nd)

      p = tuple((1-t)*a + t*b)

    return [p], [t]

class XcurveLine(Equations):

  def intersections_curveline(self, nodes0, nodes1):

    curve, line = (), ()
    if (len(nodes0), len(nodes1)) == (4, 2):
      curve, line = nodes0, nodes1
    elif (len(nodes0), len(nodes1)) == (2, 4):
      line, curve = nodes0, nodes1
    else:
      pass # raise

    p0, p1, p2, p3 = curve
    a, b, c = self.linear_equation(line)
    f0 =      a * p0[0] + b * p0[1] + c
    f1 = 3 * (a * p1[0] + b * p1[1] + c)
    f2 = 3 * (a * p2[0] + b * p2[1] + c)
    f3 =      a * p3[0] + b * p3[1] + c

    a = -f0 + f1 - f2 + f3
    b = 3 * f0 - 2 * f1 + f2
    c = -3 * f0 + f1
    d = f0
    
    if a == 0:
      if b == 0:
        if c == 0: tlist = []
        else: tlist = -d/c
      else:
        tlist = self.quadratic_equation(b,c,d)
    else:
      tlist = self.cubic_equation(a,b,c,d)
    points = []
    for t in tlist:
      if 0.0 < t < 1.0:
        x = (1-t)**3*p0[0]+3*(1-t)**2*t*p1[0]+3*(1-t)*t**2*p2[0]+t**3*p3[0]
        y = (1-t)**3*p0[1]+3*(1-t)**2*t*p1[1]+3*(1-t)*t**2*p2[1]+t**3*p3[1]
        points.append((x,y))

    # 線分上の点を選択 ?
    index_of_points = []
    for i, p in enumerate(points):
      if (line[0][0] < p[0] < line[1][0]) or (line[0][0] > p[0] > line[1][0]):
        if (line[0][1] < p[1] < line[1][1]) or (line[0][1] > p[1] > line[1][1]):
          index_of_points.append(i)

    if not index_of_points:
      # とりあえずの当たり判定
      return []

    tvalues = []
    if len(nodes0) == 4:
      tlist = [t for t in tlist if t > 0 and 1 > t] # くるしい
      tvalues = sorted([tlist[i] for i in index_of_points])
    elif len(nodes0) == 2:
      req_points = [points[i] for i in index_of_points]
      line_tlist = [math.dist(line[0], p)/math.dist(*line) for p in req_points]
      tvalues = sorted(line_tlist)

    return points, tvalues

class Xcurves(Equations):

  def __init__(self):
    self.bool_data = None

  def bounding(self, nodes: tuple) -> tuple:
    """ the bounding box (left, bottom, right, top) """
    if len(nodes) == 2:
      p0, p1 = nodes
      px, py = (p0[0], p1[0]), (p0[1], p1[1])
      return min(px), min(py), max(px), max(py)

    p0, p1, p2, p3 = nodes
    bounds = [[], []]
    bounds[0] += p0[0], p3[0]
    bounds[1] += p0[1], p3[1]

    for i in [0, 1]:

      f = lambda t: ((1-t)**3*p0[i]+3*t*(1-t)**2*p1[i]+3*t**2*(1-t)*p2[i]+t**3*p3[i])

      a = float(-3 * p0[i] + 9 * p1[i] - 9 * p2[i] + 3 * p3[i])  # -3*p0 + 9*p1 - 9*p2 + 3*p3
      b = float(6 * p0[i] - 12 * p1[i] + 6 * p2[i])  # 6*p0 - 12*p1 + 6*p2
      c = float(-3 * p0[i] + 3 * p1[i])  # -3*p0 + 3*p1

      t_list = self.quadratic_equation(a, b, c)
      for t in t_list:
        if 0.0 < t < 1.0:
          p = f(t)
          bounds[i].append(p)

    return min(bounds[0]), min(bounds[1]), max(bounds[0]), max(bounds[1])

  def is_overlap(self, nodes0: tuple, nodes1: tuple) -> bool:
    """ ２つのバウンディングボックスの重なり判定、重なりで True を返す """
    if nodes0[-1] == nodes1[0]:
      return False
    left0, bottom0, right0, top0 = self.bounding(nodes0)
    left1, bottom1, right1, top1 = self.bounding(nodes1)

    return not (bottom0 > top1 or top0 < bottom1 or left0 > right1 or right0 < left1)

  def split_nodes(self, nodes, opposed_figure):
    """ 分割したベジェ曲線と相手のベジェ曲線(複数)の重なり判定を返す """
    nodes0, nodes1 = self.split(nodes)
    is_overlaps0 = [self.is_overlap(nodes0, nodes) for nodes in opposed_figure]
    is_overlaps1 = [self.is_overlap(nodes1, nodes) for nodes in opposed_figure]

    return (nodes0, any(is_overlaps0)), (nodes1, any(is_overlaps1))

  def separate(self, nodes_list=[[],[]]):
    """ ベジェ曲線を分割し、重なりありの曲線を残す """
    spr_nodes_list = [[],[]]
    bool_values = [[],[]]
    for i in [0, 1]:
      for nodes in nodes_list[i]:
        nb0, nb1 = self.split_nodes(nodes, nodes_list[1-i])
        for nb in [nb0, nb1]:
          spr_nodes, bool_value = nb
          bool_values[i].append((bool_value, 1))
          if bool_value == True:
            spr_nodes_list[i].append(spr_nodes)

    return spr_nodes_list, bool_values

  def get_tvalues(self, bool_data):
    if bool_data is None:
      return []
    smr_bool_data = []
    pre_b = None
    count = 0
    for idx, data in enumerate(bool_data):
      b, i = data
      if pre_b is None or pre_b == b:
        count += i
      elif pre_b != b:
        smr_bool_data.append((pre_b, count))
        count = i

      if idx == len(bool_data)-1:
        if pre_b == b:
          smr_bool_data.append((b, count))
        elif pre_b != b:
          smr_bool_data.append((b, i))
      else:
        pre_b = b
    # print(smr_bool_data)
    t_values = []
    total_count = sum(map(lambda e: e[1], smr_bool_data))
    false_counts = [e[1] for e in smr_bool_data if e[0] == False]
    del (false_counts[-1:])
    true_counts = [e[1] for e in smr_bool_data if e[0] == True]
    
    count = 0 # _f -> overlap_fals
    for false_count, true_count in zip(false_counts, true_counts):
      count = count + false_count + (true_count / 2)
      t_values.append(count / total_count)
      count += (true_count / 2)

    return t_values

  def update_bool_data(self, bool_data):
    if self.bool_data is None:
      self.bool_data = bool_data
      return
    pre_bool_data = [(b, i*2) for b,i in self.bool_data]
    cur_bool_data = []
    for b, i in pre_bool_data:
      if b == False:
        cur_bool_data.append((b, i))
      if b == True:
        count = 0
        while True:
          _b, _i = bool_data.pop(0)
          count += _i
          cur_bool_data.append((_b, _i))
          if count == i:
            break

    self.bool_data = cur_bool_data

  def get_points(self, nodeslist):
    
    _points = [nodes[0] for nodes in nodeslist[0]]
    dic = {1.: _points[0]}
    for i in range(len(_points)-1):
      p = _points[i]
      q = _points[i+1]
      dist = norm(p, q)
      dic[dist] = tuple(q)
    
    points = tuple(p for dist, p in dic.items() if dist > 0.0001)
    
    return points


  def recursive_separate(self, nodes_list, count=0):
    """ main process """
    count += 1
    all_nodes = sum(nodes_list, [])
    distances = [math.dist(nodes[0], nodes[-1]) for nodes in all_nodes]
    if distances == [] or count > 50:
      self.bool_data = None
      return [], None
    if max(distances) < 0.0000001:
      bool_data = self.bool_data
      self.bool_data = None
      return nodes_list, bool_data
    
    nodes_list, bool_values = self.separate(nodes_list)
    self.update_bool_data(bool_values[0])

    return self.recursive_separate(nodes_list, count)

  def intersections_curves(self, nodes0, nodes1):

    nodes_list = [[nodes0], [nodes1]]
    nodeslist, bool_data = self.recursive_separate(nodes_list)
    points = self.get_points(nodeslist)
    tvalues = self.get_tvalues(bool_data)

    return points, tvalues


class Intersect(Xlines, XcurveLine, Xcurves, Bezier):
  
  def intersections(self, nodes, othernodes):
    length = len(nodes) + len(othernodes)
    points, tvalues = [], []
    if length == 4:
      points, tvalues = self.intersections_lines(nodes, othernodes)
    elif length == 6:
      points, tvalues = self.intersections_curveline(nodes, othernodes)
    elif length == 8:
      points, tvalues = self.intersections_curves(nodes, othernodes)
    else:
      print("intersections: nodes value error.")
    
    return points, tvalues

  def separate_nodes(self, nodes, tlist, nodes_list=None):
    if nodes_list is None and tlist:
      nodes_list = []
      tlist_idx = range(len(tlist))
      tlist = [(tlist[i]-tlist[i-1])/(1-tlist[i-1]) if i!=0 else tlist[i] for i in tlist_idx]
    elif nodes_list is None and not tlist:
      return []
    
    elif not tlist:
      nodes_list.append(nodes)
      return nodes_list

    # print(len(tlist))
    t = tlist.pop(0)
    nodes0, nodes1 = self.split(nodes, t)
    nodes_list.append(nodes0)

    return self.separate_nodes(nodes1, tlist, nodes_list)


  def separate_figure(self, figure, otherfigure):
    figure_t = []
    for nodes in figure:
      tlist = []
      for othernodes in otherfigure:
        _, _tlist = self.intersections(nodes, othernodes)
        if _tlist:
          tlist += _tlist
      # print(sorted(tlist))
      figure_t.append((nodes, sorted(tlist)))

    figure_n = []
    for nodes, tlist in figure_t:
      if tlist == []:
        figure_n.append(nodes)
      else:
        nodes_list = self.separate_nodes(nodes, tlist)
        figure_n += nodes_list

    return figure_n

  def find_outside_nodes(self, figures, length=512):
    direction = ""
    first_outside_nodes = ()
    for nodes in figures:
      p = array(self.t2point(nodes, 0.01))
      q = array(nodes[0])
      a = q - p
      h = length / math.dist(p, q)
      b = array([a[1], -a[0]]) * h
      c = array([-a[1], a[0]]) * h
      left_line = (tuple(p), tuple(p+b))
      right_line = (tuple(p), tuple(p+c))
      print(math.dist(*left_line))
      othernodes_list = figures[::]
      othernodes_list.remove(nodes)
      ret_l, ret_r = [], []
      for othernodes in othernodes_list:
        _, left_t = self.intersections(left_line, othernodes)
        ret_l += left_t
        _, right_t = self.intersections(right_line, othernodes)
        ret_r += right_t
        if not len(ret_l) % 2:
          first_outside_nodes = nodes
          direction = "clockwise"
          break
        if not len(ret_r) % 2:
          first_outside_nodes = nodes
          direction = "anti-clockwise"
          break
      else:
        continue
      break

    return first_outside_nodes, direction

  def combine_figures(self, figure, otherfigure):
    
    figures = figure + otherfigure
    nodes, direction = self.find_outside_nodes(figures)

    startpoint = nodes[0]
    cmb_figure = [nodes]
    nodes_list = []
    while True:
      if nodes_list == []:
        figures.remove(nodes)
      else:
        while nodes_list:
          rm_nodes, _ = nodes_list.pop()
          figures.remove(rm_nodes)
      for othernodes in figures:
        if math.dist(nodes[-1], othernodes[0]) < 0.0001:
          nodes_list.append((othernodes, othernodes))
        elif math.dist(nodes[-1], othernodes[-1]) < 0.0001:
          nodes_list.append((othernodes, othernodes[::-1]))
      if 1 < len(nodes_list):
        p = array(nodes[-1])
        q = array(self.t2point(nodes, 0.99))
        a = q - p
        rad_d = {}
        for _, othernodes in nodes_list:
          p = array(othernodes[0])
          q = array(self.t2point(othernodes, 0.01))
          b = q - p
          cos_theta = round(dot(a, b)/(norm(a)*norm(b)), 10)
          # round 1.000000000000001の誤差をまるめる
          # print(cos_theta)
          r = math.acos(cos_theta)
          if cross2(a, b) < 0:
            r = 2 * math.pi - r
          rad_d[r] = othernodes
        key = 0.
        if direction == "clockwise":
          key = max(rad_d)
        if direction == "anti=clockwise":
          key = min(rad_d)
        nodes = rad_d[key]
        cmb_figure.append(nodes)
      elif len(nodes_list) == 1:
        _, nodes = nodes_list[0]
        cmb_figure.append(nodes)

      if math.dist(nodes[-1], startpoint) < 0.0001:
        break

    return cmb_figure

if __name__ == '__main__':

  import matplotlib.pyplot as plt
  from figure import Figure

  fig = plt.figure(dpi=100, figsize=(4, 3))
  ax = plt.gca()
  ax.set_title("intersection")
  ax.set_xlim(0, 128)
  ax.set_ylim(0, 128)

  nodes0 = (16, 32), (112, 96)
  nodes0 = (16, 64), (32, 18), (64, 112), (112, 64)
  x, y = Figure([nodes0]).plot()
  ax.plot(x, y)

  nodes1 = (16, 96), (112, 16)
  nodes1 = (16, 32), (32, 112), (64, 18), (112, 112)
  x, y = Figure([nodes1]).plot()
  ax.plot(x, y)


  # xl = xline()
  # p = xl.intersections_lines(nodes0, nodes1)
  # ax.plot(*p, "o")

  intercept = Intersect()
  points, tvalues = intercept.intersections(nodes0, nodes1)
  for p in points:
    ax.plot(*p, "o")

  plt.show()