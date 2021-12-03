import math
from bezier import Bezier # split, bounding
from array2d import norm

class Xcurves(Bezier):
    
    # def __init__(self):
    bool_data = None

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
        # 何をしているのか
        points = []
        if nodeslist:
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

    def intersections_of_two_curves(self, nodes0, nodes1):

        nodes_list = [[nodes0], [nodes1]]
        nodeslist, bool_data = self.recursive_separate(nodes_list)
        points = self.get_points(nodeslist)
        tvalues = self.get_tvalues(bool_data)

        return points, tvalues

if __name__ == '__main__':
    
    import matplotlib.pyplot as plt
    from bezier import Bezier

    fig = plt.figure(dpi=100, figsize=(4, 3))
    ax = plt.gca()
    ax.set_title("intersection")
    ax.set_xlim(0, 128)
    ax.set_ylim(0, 128)
    
    c = Xcurves()
    b = Bezier()

    nodes0 = (16, 64), (32, 18), (64, 112), (112, 64)
    x, y = b.cubic_bezier(nodes0)
    ax.plot(x, y)

    nodes1 = (16, 32), (32, 112), (64, 18), (112, 112)
    x, y = b.cubic_bezier(nodes1)
    ax.plot(x, y)

    points, t = c.intersections_of_two_curves(nodes0, nodes1)
    for p in points:
        ax.plot(*p, "o")

    plt.show()