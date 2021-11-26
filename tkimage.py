# import os
# import io
import subprocess
from PIL import ImageGrab
from time import sleep
from figure import Figure


if __name__ == '__main__':

  h1 = (25, 105), (60, 105)
  h2 = (60, 105), (60, 200), (190, 200), (190, 105)
  h3 = (190, 105), (225, 105)
  h4 = (225, 105), (250, 105), (250, 100), (225, 100)
  h5 = (225, 100), (25, 100)
  h6 = (25, 100), (0, 100), (0, 105), (25, 105)

  hat_data = (h1, h2, h3, h4, h5, h6)

  # hat = Figure(hat_data)
  hat = Figure()
  hat.figure = hat_data

  import tkinter
  root = tkinter.Tk()
  # root.geometry(f"{256}x{256}+{120}+{100}")
  root.title("a hat")
  canvas = tkinter.Canvas(root,width=256,height=256)
  canvas.pack()

  plot = hat.reflection(256).tkplot()
  canvas.create_line(plot)

  root.mainloop()

  # w = root.winfo_screenwidth()
  # print(w)
  # h = root.winfo_screenheight()
  # print(h)
  
  # ImageGrab.grab(bbox=(x, y, w, h)).save("test.png")

  # x, y, w, h = 120, 100, 256, 256
  # subprocess.run(f"screencapture -c -R {x},{y},{w},{h}")
  # subprocess.run(f"screenshot -c -R {x},{y},{w},{h}")

  # x = root.winfo_rootx() + canvas.winfo_x()
  # print(x)
  # y = root.winfo_rooty() + canvas.winfo_y()
  # print(y)
  # x1= x + canvas.winfo_width()
  # print(x1)
  # y1= y + canvas.winfo_height()
  # print(y1)

  # canvas.postscript(file="test.ps")

  # ps = canvas.postscript() # colormode='color')
  # img = Image.open(io.BytesIO(ps.encode('utf-8')))
  # GhostScript が必要 OSError: Unable to locate Ghostscript on paths
  # bm = img.tobytes()
  # img.save('test.jpg')



