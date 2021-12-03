import matplotlib.pyplot as plt
import numpy as np

def line(p, q, steps=100):
    t = np.linspace(0, 1, steps+1)
    x = (1-t)*p[0] + t*q[0]
    y = (1-t)*p[1] + t*q[1]

    return x, y

def show(x, y, title):
    fig = plt.figure(dpi=100, figsize=(3, 3))
    ax = fig.gca()
    ax.set_title(title)
    ax.set_xlim(0, 256)
    ax.set_ylim(0, 256)
    ax.plot(x, y)
    
    plt.show()

if __name__ == '__main__':
    
    p = 64, 64
    q = 192, 192
    x, y = line(p, q)
    show(x, y, "draw a line")