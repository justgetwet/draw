import math
import tkinter

def line(p, q, steps=100):
    
    dist = ((q[0]-p[0])**2 + (q[1]-p[1])**2)**0.5
    rad = math.atan2(q[1]-p[1], q[0]-p[0])

    t_list = [s / steps for s in range(steps + 1)]
    x, y = [], []
    for t in t_list:
        x.append(math.cos(rad) * dist * t + p[0])
        y.append(math.sin(rad) * dist * t + p[1])

    return x, y

def show(x, y, title):
    root = tkinter.Tk()
    root.title(title)
    width, height = 256, 256
    root.geometry(f"{width}x{height}+{150}+{150}")
    canvas = tkinter.Canvas(root,width=width,height=height)
    canvas.pack()
    plot = tuple(zip(x, y))
    canvas.create_line(plot)

    root.mainloop()

if __name__ == '__main__':

    p = 64, 64
    q = 192, 192
    x, y = line(p, q)
    show(x, y, "draw a line")

