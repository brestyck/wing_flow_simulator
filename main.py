import tkinter as tk
from PIL import Image
from PIL import ImageTk
import math

window = tk.Tk()
canvas = tk.Canvas(window, width=1000, height=1000, bg="cyan")
canvas.pack()

# Elements

class Airplane(object):
    def __init__(self, filename, **kwargs):
        self.filename = filename

    def redraw(self, aoa):
        image = Image.open(self.filename)
        image = image.rotate(aoa)
        image_rdy = canvas.create_image(0, 0, image=ImageTk.PhotoImage(image), anchor="nw")
        return image_rdy

    def debug(self):
        image = Image.open(self.filename)
        image_tk = ImageTk.PhotoImage(image, master=window)
        image_rdy = canvas.create_image(500, 100, image=image_tk, anchor="nw")
        # label = tk.Label(window, image=ImageTk.PhotoImage(image))
        return image_rdy


class PolyWing(object):
    def __init__(self):
        pass

    def rotate(self, points, aoa):
        new_points = list(points)
        rad = aoa * (math.pi / 180)
        cos_val = math.cos(rad)
        sin_val = math.sin(rad)
        for coords in new_points:
            x_val = coords[0]
            y_val = coords[1]
            coords[0] = x_val * cos_val - y_val * sin_val
            coords[1] = x_val * sin_val + y_val * cos_val
        return new_points

    def redraw(self, points):
        canvas.create_polygon(points, fill="red")

speed = 0
altitude = 0
aoa = 0
speed_indicator = canvas.create_text(950, 10, text=f"Speed {speed}", font="Times 20 italic bold", fill="white")
altitude_indicator = canvas.create_text(820, 10, text=f"Altitude {altitude}", font="Times 20 italic bold", fill="white")
aoa_indicator = canvas.create_text(710, 10, text=f"AOA {aoa}", font="Times 20 italic bold", fill="white")

starts = [
    [30, 30],
    [50, 30],
    [50, 50],
    [30, 50],
]

boeing = PolyWing()
boeing.redraw(boeing.rotate(starts, aoa=-15))
# Functions
# def aoa_plus():


window.mainloop()