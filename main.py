import tkinter as tk
from tkinter import *
import math

vertex_index = 1
V1 = [0, 0]
V2 = [0, 0]
V3 = [0, 0]


def place_vertex(event):
    global vertex_index
    global V1, V2
    fill_color = "black"
    x, y = event.x, event.y
    x1, y1 = x - 1, y - 1
    x2, y2 = x + 1, y + 1
    print(x1)
    if vertex_index == 1:
        drawspace.delete('all')
        V1 = [x, y]
        vertex_index += 1
        drawspace.create_oval(x1, y1, x2, y2, fill=fill_color)
    elif vertex_index == 2:
        V2 = [x, y]
        vertex_index = 1
        drawspace.create_oval(x1, y1, x2, y2, fill=fill_color)
        x, y = get_final_vertex(V1, V2)
        x1, y1 = x - 1, y - 1
        x2, y2 = x + 1, y + 1
        drawspace.create_oval(x1, y1, x2, y2, fill=fill_color)


def get_final_vertex(V1, V2):
    [x1, y1] = V1
    [x2, y2] = V2
    side_len = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    angle = math.atan((y2 - y1) / (x2 - x1)) + (2 * math.pi / 6)
    if x2 >= x1:
        V3 = [x1 + side_len * math.cos(angle),
              y1 + side_len * math.sin(angle)]
    else:
        V3 = [x2 + side_len * math.cos(angle),
              y2 + side_len * math.sin(angle)]
    return(V3)


app = Tk()
app.title("Sierpinski's Triangle")
app.geometry('400x400')

drawspace = Canvas(app)
drawspace.pack(expand=YES, fill=BOTH)
drawspace.bind("<Button-1>", place_vertex)
mainloop()
