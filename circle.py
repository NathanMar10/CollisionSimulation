import numpy
import PIL.Image
import pygame
from PIL import ImageTk, ImageDraw
import tkinter


class Circle:
    """ A Circle to be Drawn on the Screen. Has a Position, Size, and Velocity """

    def __init__(self, position: list, size: float, velocity: list, color: tuple):
        # Given Properties
        self.velocity = velocity
        self.size = size
        self.position = position
        self.color = color
        # Derived Properties
        self.density = 255 * 3 - color[0] - color[1] - color[2]
        self.charge = color[0] - color[2]
        self.mass = self.density * self.size**2


        self.take_library_selfie()


        # Set the root window background color to a transparent color


    def __str__(self):
        return "Position: " + str(self.position) + "\nVelocity: " + str(self.velocity) + "\nSize: " + str(self.size)


    def take_a_selfie(self):
        img = PIL.Image.new('RGBA', (int(numpy.ceil(self.size * 2.1)), int(numpy.ceil(self.size * 2.1))), (0, 0, 0, 0))

        # Called for each circle and then we can determine the valid x & y values
        x_max = int(numpy.floor(1.8 * self.size))
        x_min = int(numpy.ceil(.2 * self.size))

        """
        iterating over xmin to xmax -> which are the extreme values of everything
        I can literlaly just use that exact value of x, since they are the further side of the pixel
        check what y value i need
        shrink range

        color
        """

        for x in range(x_min, x_max):
            # Called for each x value in the range

            y_half_width = numpy.sqrt(self.size ** 2 - (self.size - x) ** 2)
            y_range = [int(numpy.ceil(self.size - y_half_width)), int(numpy.floor(self.size + y_half_width))]

            for y in (y_range):
                img.putpixel((x, y), self.color)
                img.putpixel((y, x), self.color)

        self.image = ImageTk.PhotoImage(img)


    def take_library_selfie(self):
        img = PIL.Image.new('RGBA', (int(numpy.ceil(self.size * 2) + 2), int(numpy.ceil(self.size * 2)) + 2), (0, 0, 0, 0))
        x_max = 2 * self.size + 1
        x_min = 1

        draw = ImageDraw.Draw(img)
        draw.ellipse((x_min, x_min, x_max, x_max), fill='black', outline=self.color)
        #self.imageTk = ImageTk.PhotoImage(img)

        mode = img.mode
        size = img.size
        data = img.tobytes()
        self.pillow_image = img
        self.pygame_image = pygame.image.fromstring(data, size, mode)