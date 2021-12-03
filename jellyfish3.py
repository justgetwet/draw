from figure import Figure, show_tk, write_svg
from intersect import Intersect

circle = Figure()
circle.ell(126, 126, (128, 128))

m = 128, 96+12+4
head = Figure()
head.ell(60, 50)
head.move(m)
head.cut(leave="tail")

body = Figure()
body.ell(60, 25)
body.move(m)
body.cut(leave="head")

head.join(body)
head.scale((1.1, 1.1)).move((-3, -1))

g = 24
w = 14
reg1 = Figure()
t1 = (0, 0), (0-g, 16), (0+g, 32), (0, 48)
t2 = (0, 48), (0-g, 64), (0+g, 80), (0, 96)
# r = Figure((t2,))
# r.cut()
# print(r.figure)
t2c = (0, 48), (-12.24, 56.16), (-5.7528, 64.32), (0.359, 72.479)
t2t = (0.359, 72.479), (0.359, 72.479+6), (0.359+w, 72.479+6), (0.359+w, 72.479)
t3c = (0.359+w, 72.479), (-5.7528+w, 64.32), (-12.24+w, 56.16), (0+w, 48)
t3 = (0+w, 48), (0+g+w, 32), (0-g+w, 16), (0+w, 0)
t4 = (0+w, 0), (0, 0)
reg1.figure = (t1, t2c, t2t, t3c, t3, t4)
reg1.move((98-1, 117+12))

reg2 = Figure()
t1 = (0, 0), (0-g, 16), (0+g, 32), (0, 48)
t2 = (0, 48), (0-g, 64), (0+g, 80), (0, 96)
# r = Figure((t2,))
# r.cut(0.7)
# print(r.figure)
t2c = (0, 48), (-17.04, 59.36), (2.215, 70.72), (6.226, 82.08)
t2t = (6.226, 82.08), (6.226, 82.08+6), (6.226+w, 82.08+6), (6.226+w, 82.08)
t3c = (6.226+w, 82.08), (2.215+w, 70.72), (-17.04+w, 59.36), (0+w, 48) 
t3 = (0+w, 48), (0+g+w, 32), (0-g+w, 16), (0+w, 0) 
t4 = (0+w, 0), (0, 0)
reg2.figure = (t1, t2c, t2t, t3c, t3, t4)
reg2.move((98+26-1, 117+16))

reg3 = reg1.copy()
reg3.move((26+26-1, 0))

f = Figure()
f.figure = head.combine_figures(head.figure, reg1.figure)

head.combi(reg1)
head.combi(reg2)
head.combi(reg3)
head.rotate(24)
head.move((-10, -3))
# its = Intersect()
# chead = its.combine_figures(head, reg1)
# print(chead.figure)

# show_tk(circle, head)

f = "./test4.html"
dic = {
    "circle": circle.figure, 
    "head": head.figure, 
    }
write_svg(f, dic)