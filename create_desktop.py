# -*- coding: utf-8 -*-


import tkinter as tk
import cv2
import Shapes
import numpy
import time

import random
from PIL import Image, ImageTk

"""
Created on Wed Feb  2 09:49:59 2022

@author: thena
"""

# This should be a tuple. Unchangeable, ordered screen sizes
window_size = (1920, 1200)
seed = "surprise"
circles = 30
maxV = 1.5
maxS = 100
minS = 5
wall_v_loss = 1
coeff_restitution = .99
big_g = .0000015
# .5 here for good times
lil_k = 200

# Here we have a variable-sized array of "pixels".
controller = Shapes.Controller(window_size[0], window_size[1], maxV, maxS, seed, circles, wall_v_loss,
                               coeff_restitution, big_g, lil_k, minS)


def runframe(controller):
    controller.move_shapes()

    controller.solve_collisions()
    controller.calculate_force()
    controller.unstack_circles()
    controller.unstack_circles()


# First call so it crashes before creating a window most of the time

controller.unstack_circles()
window = tk.Tk()
original_image = controller.get_image_efficient()

img = ImageTk.PhotoImage(original_image)
# img = ImageTk.PhotoImage(file = 'Rotating_earth_(large).gif')
label = tk.Label(window, image=img)
label.image = img
label.pack()
# tk.update()


running_saved_images = []



for x in range(1, 8000):
    runframe(controller)
    next_img_original = controller.get_image_efficient()
    if x % 4 == 0:
        running_saved_images.append(next_img_original)
    x+=1
    next_img = ImageTk.PhotoImage(next_img_original)
    window.title(str(x))

    label.configure(image=next_img)
    label.image = next_img
    # label = tk.Label(window, image = next_img).pack()
    window.update()

# Reversing into a new list



video = cv2.VideoWriter("DOTS_24.mp4", 0, 20, (1920, 1200))
reversed = running_saved_images.copy()
reversed.reverse()
reversed.remove(reversed[0])
running_saved_images.extend(reversed)
running_saved_images.remove(running_saved_images[0])


#running_saved_images.remove(running_saved_images[len(running_saved_images) - 1])
for frame in running_saved_images:
    opencv_im = numpy.array(frame)
    opencv_im = opencv_im[:, :, ::-1]
    video.write(opencv_im)



video.write(numpy.array(running_saved_images[len(running_saved_images) - 2]))
video.write(numpy.array(running_saved_images[len(running_saved_images) - 1]))
video.write(numpy.array(Image.new("RGB", (1920, 1080), (255, 255, 255))))



cv2.destroyAllWindows()
video.release()




print("Video Saved")
window.mainloop()



