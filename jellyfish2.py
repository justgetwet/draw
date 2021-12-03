import math
from figure import Figure, show_tk, write_svg

circle = Figure()
circle.ell(126, 126, (128, 128))

m = 128, 96+12
head = Figure()
head.ell(60, 50)
head.move(m)
head.cut(leave="tail")

body = Figure()
body.ell(60, 25)
body.move(m)
body.cut(leave="head")

head.join(body)
head.scale((1.1, 1.1))

g = 24
w = 12
reg1 = Figure()
t1 = (0, 0), (0-g, 16), (0+g, 32), (0, 48)
# t2 = (0, 48), (0-g, 64), (0+g, 80), (0, 96)
# r = Figure((t2,))
# r.cut()
# print(r.figure)
t2c = (0, 48), (-12.24, 56.16), (-5.7528, 64.32), (0.359, 72.479)
t2t = (0.359, 72.479), (0.359+w, 72.479)
t3c = (0.359+w, 72.479), (-5.7528+w, 64.32), (-12.24+w, 56.16), (0+w, 48)
t3 = (0+w, 48), (0+g+w, 32), (0-g+w, 16), (0+w, 0)
reg1.figure = (t1, t2c, t2t, t3c, t3)
reg1.scale((1.1, 1.1))
reg1.move((96+2, 117+16))


reg2 = reg1.copy()
reg2.move((28, 0))

reg3 = reg2.copy()
reg3.move((28, 0))

# show_tk(circle, head, reg1, reg2, reg3)

f = "./test3.html"
dic = {
    "circle": circle.figure, 
    "reg1": reg1.figure,
    "reg2": reg2.figure,
    "reg3": reg3.figure,
    "head": head.figure, 
    }
write_svg(f, dic)