# -*- coding: utf-8 -*-


import tkinter as tk


import Shapes
import time

from PIL import Image, ImageTk
"""
Created on Wed Feb  2 09:49:59 2022

@author: thena
"""
window_size = (1500, 1000)

root = tk.Tk()

frame = tk.Frame(root)
frame.pack()

canvas = tk.Canvas(frame, bg = "black", width=window_size[0], height=window_size[1])
canvas.pack()





# This should be a tuple. Unchangeable, ordered screen sizes
SCREEN_SIZE = (1800, 1000)
SCREEN_NAME = "Wow, Nate! These really look like planets! -Aiden"
MAX_FPS = 25
SUBFRAMES = 4

CIRCLE_COUNT = 100
VELOCITY_RANGE = (20, 100)
SIZE_RANGE = (10, 80)

#COR, Unstack Shapes
COLLISIONS = (1, True)
#Big G, Calculate Gravity
GRAVITY = (.00005, True)
#K, Calculate Charge
ELECTRICITY = (400000, True)
SEED = "surprise"



# Here we have a variable-sized array of "pixels".
controller = Shapes.Controller(SCREEN_SIZE, CIRCLE_COUNT, VELOCITY_RANGE,
                               SIZE_RANGE, COLLISIONS, GRAVITY, ELECTRICITY, SEED,
                               root)
def runframe(controller):
    controller.move_shapes()
    controller.unstack_circles()
    controller.unstack_circles()
    controller.solve_collisions()
    controller.calculate_force()


#First call so it crashes before creating a window most of the time

controller.unstack_circles()


original_image = Image.new('RGBA', (window_size), (0, 0, 0, 100))





img = ImageTk.PhotoImage(original_image)
img = ImageTk.PhotoImage(file = 'Rotating_earth_(large).gif')

canvas.create_image(150, 150, image=img)

#label.pack()
root.configure(background="black")
#tk.update()


#window.wm_attributes("-transparentcolor", 'grey')


prev_time = time.time_ns()
while(True):
    

    prev_time = time.time_ns()
    runframe(controller)
    #next_img_original = controller.get_image_efficient()
    #next_img = ImageTk.PhotoImage(next_img_original)


    controller.place_on_canvas(canvas)

    #label.configure(image = next_img)
    #label.image = next_img

    #label = tk.Label(window, image = next_img).pack()
    window.update()

