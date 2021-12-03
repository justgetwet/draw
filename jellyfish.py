import math
from figure import Figure, show_tk, write_svg

circle = Figure()
circle.ell(126, 126, (128, 128))

m = 126, 86
body = Figure()
body.ell(60, 50)
body.move(m)
body.cut(leave="tail")

head = Figure()
head.ell(60, 30)
head.move(m)
head.cut(leave="head")

body.join(head)
body.scale((0.9, 0.9))
body.rotate(25)
body.move((25, -5))
# body.show()

reg = Figure()
t1 = (0, 0), (0, 32), (0, 64), (0, 96)
t2 = (0, 96), (0, 108), (10, 108), (10, 96)
t3 = (10, 96), (10, 64), (10, 32), (10, 0) 
reg.figure = (t1, t2, t3)
reg.move((123, 102))
reg.rotate(25)
reg.move((-18, -5))

arm = Figure()
t1 = (0, 0), (10, 32), (10, 64), (0, 84)


h = math.dist((0, 84), (10, 64))
print(h)
a = 10
rad = math.asin(a/h)
print(rad)
print(math.degrees(rad))
print("---")
x1 = math.cos(rad) + 0
x2 = math.cos(rad) + 10
y1 = math.sin(rad) * 12 + 84
print(x1, y1, x2, y1)
t2 = (0, 84), (x1, y1), (x2, y1), (10, 84)

t3 = (10, 84), (20, 64), (20, 32), (10, 0) 
arm.figure = (t1, t2, t3)
arm.move((128-38, 102))
arm.rotate(20)
arm.rotate(25)
arm.move((-13, -19))

arm_r = arm.copy()
arm_r.reflect("y")
arm_r.rotate(45)
arm_r.move((62, 20))

# show_tk(circle, body, reg, arm, arm_r)

f = "./test2.html"
dic = {
    "circle": circle.figure, 
    "reg": reg.figure,
    "arm": arm.figure,
    "arm_r": arm_r.figure,
    "body": body.figure, 
    }
write_svg(f, dic)