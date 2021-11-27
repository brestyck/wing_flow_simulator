import tkinter as tk
from PIL import Image
from PIL import ImageTk
import math
from time import sleep

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
    def __init__(self, starts, Swing, mass):
        self.Swing = Swing
        self.mass = mass
        x0 = starts[0][0]
        x1 = starts[1][0]
        x2 = starts[2][0]
        x3 = starts[3][0]
        y0 = starts[0][1]
        y1 = starts[1][1]
        y2 = starts[2][1]
        y3 = starts[3][1]
        self.redraw(starts)
        self.centre = self.centroid(x0, x1, x2, x3, y0, y1, y2, y3)

    def centroid(self, x0, x1, x2, x3, y0, y1, y2, y3):
        cx = (1 / 4) * (x0 + x1 + x2 + x3)
        cy = (1 / 4) * (y0 + y1 + y2 + y3)
        canvas.create_oval(cx-10, cy-10, cx+10, cy+10, tag="centroid_visual", fill="yellow")
        # canvas.create_oval(0, 0, 20, 20, tag="centroid_visual_debug", fill="yellow")
        print(cx, cy)

    def simple_rotate(self, points, aoa_df):
        if aoa_df > 0:
            points[0][0] += aoa_df
            points[1][0] += aoa_df
            points[2][0] -= aoa_df
            points[3][0] -= aoa_df
            points[0][1] -= aoa_df
            points[1][1] += aoa_df
            points[2][1] += aoa_df
            points[3][1] -= aoa_df
        if aoa_df < 0:
            points[0][0] += aoa_df
            points[1][0] += aoa_df
            points[2][0] -= aoa_df
            points[3][0] -= aoa_df
            points[0][1] -= aoa_df
            points[1][1] += aoa_df
            points[2][1] += aoa_df
            points[3][1] -= aoa_df
        return points

    def rotate(self, points, aoa, aoa_df):
        print(points)

        # Translate coordinates to the sq system
        sq = [
            [
                (points[0][0] - points[1][0])/2,
                (points[0][1] - points[3][1])/2
            ],
            [
                (points[1][0] - points[0][0])/2,
                (points[1][1] - points[2][1])/2
            ],
            [
                (points[2][0] - points[3][0])/2,
                (points[2][1] - points[1][1])/2
            ],
            [
                (points[3][0] - points[2][0])/2,
                (points[3][1] - points[0][1])/2
            ]
        ]

        new_points = list(sq)
        rad = aoa * (math.pi / 180) #180
        cos_val = math.cos(rad)
        sin_val = math.sin(rad)
        for i in range(0, 3):
            x_val = new_points[i][0]
            y_val = new_points[i][1]
            nx = x_val * cos_val - y_val * sin_val
            ny = x_val * sin_val + y_val * cos_val
            dx = abs(nx - x_val)
            dy = abs(ny - y_val)
            if aoa_df > 0:
                pass

        return new_points

    def redraw(self, points):
        canvas.delete("wing_frame")
        canvas.create_polygon(points, fill="red", tag="wing_frame")

    def calculate(self, speed, aoa, altitude):
        if aoa <= 20:
            Cy = -(1/30)*aoa
        else:
            Cy = -(1/aoa)
        Ro = -0.0001 * altitude + 1.27
        Swing = self.Swing
        Ya = Cy*(Swing*((Ro*speed*speed)/2))
        mass = self.mass
        vertical_speed = Ya - mass*0.01
        altitude += vertical_speed
        return altitude


speed = 0
altitude = 0
aoa = 0
speed_indicator = canvas.create_text(950, 10, text=f"Speed {speed}", font="Times 20 italic bold", fill="white")
altitude_indicator = canvas.create_text(500, 10, text=f"Altitude {altitude}", font="Times 20 italic bold", fill="white")
aoa_indicator = canvas.create_text(210, 10, text=f"AOA {aoa}", font="Times 20 italic bold", fill="white")

starts = [
    [500, 500],
    [800, 500],
    [800, 550],
    [500, 550]
]

boeing = PolyWing(starts, Swing=10, mass=10000)
# boeing.redraw(boeing.rotate(starts, aoa=aoa))
# Functions
def aoa_plus(event):
    global aoa
    print(aoa)
    aoa += 1
    boeing.redraw(boeing.simple_rotate(starts, aoa_df=5))
    canvas.itemconfig(aoa_indicator, text=f"AOA {aoa}")
    # aoa_indicator.text = aoa

def aoa_minus(event):
    global aoa
    print(aoa)
    aoa -= 1
    boeing.redraw(boeing.simple_rotate(starts, aoa_df=-5))
    canvas.itemconfig(aoa_indicator, text=f"AOA {aoa}")
    # aoa_indicator.text = aoa

def speed_increase(event):
    global speed
    speed += 5
    canvas.itemconfig(speed_indicator, text=f"SPD {speed}")

def speed_decrease(event):
    global speed
    speed -= 5
    canvas.itemconfig(speed_indicator, text=f"SPD {speed}")

def mainloop(event):
    print("Mainloop activated")
    global altitude
    altitude = boeing.calculate(speed=speed, aoa=aoa, altitude=altitude)
    canvas.itemconfig(altitude_indicator, text=f"ALTITUDE {altitude}")
    sleep(1)
    # window.after(ms=1000, func=mainloop)


window.bind("<w>", aoa_plus)
window.bind("<s>", aoa_minus)
window.bind("<e>", speed_increase)
window.bind("<q>", speed_decrease)
window.bind("<x>", mainloop)

window.mainloop()
window.after(ms=1000, func=mainloop)
