# -*- coding: utf-8 -*-
import PyQt5 as pyqt
from PyQt5.QtWidgets import QApplication, QLabel, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap
import PyQt5.QtGui as QtGui


from PIL import Image
from PIL.ImageQt import ImageQt

from Shapes import Circle
from Shapes import get_image

from PIL.ImageQt import ImageQt

import random
"""
Created on Tue Feb  1 12:13:03 2022

@author: thena
"""

# This should be a tuple. Unchangeable, ordered screen sizes
screenSize = (800, 400)
random.seed(1203897654)


circles = 1000000
# Here we have a variable-sized array of "pixels". 



## thing


# If i can write them to a screen I'll be a happy little boy



shapes = []

app = QApplication([]);

for x in range(circles):
    shapes.append(Circle([random.randint(0, screenSize[0] - 1), random.randint(0, screenSize[1]) - 1], random.randint(10, 20), [0, 0]))



    
    



scene = QGraphicsScene()
scene.setSceneRect(0, 0, screenSize[0], screenSize[1])


imageqt = ImageQt(get_image(shapes, screenSize[0], screenSize[1]))

scene.addPixmap(QtGui.QPixmap.fromImage(imageqt))

graphics_view = QGraphicsView(scene)


graphics_view.show()

app.exec()









