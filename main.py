import tkinter as tk
from tkinter import *
import math
import random

vertex_index = 1
V1 = [0, 0]
V2 = [0, 0]
V3 = [0, 0]


def place_vertex(event):
    global vertex_index
    global V1, V2, V3
    fill_color = "blue"
    point_size = 1
    x, y = event.x, event.y
    x1, y1 = x - point_size, y - point_size
    x2, y2 = x + point_size, y + point_size
    if vertex_index == 1:
        V2 = [0, 0]
        V3 = [0, 0]
        drawspace.delete('all')
        V1 = [x, y]
        vertex_index += 1
        drawspace.create_oval(x1, y1, x2, y2, fill=fill_color)
    elif vertex_index == 2:
        V2 = [x, y]
        vertex_index = 1
        drawspace.create_oval(x1, y1, x2, y2, fill=fill_color)
        # for equilateral triangles
        x, y = get_final_vertex(V1, V2)
        V3 = [x, y]
        x1, y1 = x - point_size, y - point_size
        x2, y2 = x + point_size, y + point_size
        drawspace.create_oval(x1, y1, x2, y2, fill=fill_color)
    # else:
    #     V3 = [x, y]
    #     vertex_index = 1
    #     drawspace.create_oval(x1, y1, x2, y2, fill=fill_color)


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
    return(int(V3[0]), int(V3[1]))


def in_triangle(point_coord):
    # uses barycentric coordinates to determine if point lies in triangle
    # does not currently account for edge cases
    global V1, V2, V3
    alpha = ((V2[1] - V3[1]) * (point_coord[0] - V3[0]) + (V3[0] - V2[0]) * (point_coord[1] -
                                                                             V3[1])) / ((V2[1] - V3[1]) * (V1[0] - V3[0]) + (V3[0] - V2[0]) * (V1[1] - V3[1]))
    beta = ((V3[1] - V1[1]) * (point_coord[0] - V3[0]) + (V1[0] - V3[0]) * (point_coord[1] -
                                                                            V3[1])) / ((V2[1] - V3[1]) * (V1[0] - V3[0]) + (V3[0] - V2[0]) * (V1[1] - V3[1]))
    gamma = 1 - alpha - beta

    # returns true if point is in triangle
    return (0 < alpha < 1) and (0 < beta < 1) and (0 < gamma < 1)


def draw_point(coordinate, fill_color):
    x, y = coordinate[0], coordinate[1]
    point_size = 1
    x1, y1 = x - point_size, y - point_size
    x2, y2 = x + point_size, y + point_size
    drawspace.create_oval(x1, y1, x2, y2, fill=fill_color)


def next_point(last_point, V1, V2, V3):
    vertex = random.choice([V1, V2, V3])
    if abs(vertex[0]) < abs(last_point[0]):
        x = (vertex[0] - last_point[0]) / 2 + last_point[0]
    else:
        x = (last_point[0] - vertex[0]) / 2 + vertex[0]
    if abs(vertex[1]) < abs(last_point[1]):
        y = (vertex[1] - last_point[1]) / 2 + last_point[1]
    else:
        y = (last_point[1] - vertex[1]) / 2 + vertex[1]
    return [x, y]


def sierpensify():
    global V1, V2, V3
    max_x = max([V1[0], V2[0], V3[0]])
    min_x = min([V1[0], V2[0], V3[0]])
    max_y = max([V1[1], V2[1], V3[1]])
    min_y = min([V1[1], V2[1], V3[1]])

    intial_point = [random.randrange(
        min_x, max_x), random.randrange(min_y, max_y)]
    while not in_triangle(intial_point):
        intial_point = [random.randrange(
            min_x, max_x), random.randrange(min_y, max_y)]

    draw_point(intial_point, 'black')
    last_point = intial_point

    if(num_points.get() < 1):
        num_points.set(1)

    if(num_points.get() > 1):
        for x in range(num_points.get() - 1):
            new_point = next_point(last_point, V1, V2, V3)
            draw_point(new_point, 'black')
            last_point = new_point


def clear():
    global V1, V2, V3
    V1 = [0, 0]
    V2 = [0, 0]
    V3 = [0, 0]
    drawspace.delete('all')


app = Tk()
app.title("Sierpinski's Triangle Generator")
app.geometry('600x600')

intructions = Label(
    app, text="Intructions: Place 2 points on window and the third point\nfor an equilateral triangle will be placed automatically.\nThen choose the number of points you'd like to plot and press\nthe start button. Press the clear button to empty the window.")
intructions.pack(side=TOP)

drawspace = Canvas(app)
drawspace.pack(expand=YES, fill=BOTH)
drawspace.bind("<Button-1>", place_vertex)

points_label = Label(app, text="# points:")
points_label.pack(side=LEFT)
num_points = IntVar()
num_points.set(1000)
num_point_entry = Entry(app, textvariable=num_points)
num_point_entry.pack(side=LEFT)
start = Button(text='Start', command=sierpensify)
start.pack(side=LEFT)
clear = Button(text='Clear', command=clear)
clear.pack(side=LEFT)
mainloop()
