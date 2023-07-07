# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 12:30:57 2022

@author: thena
"""



from Shapes import get_image_efficient

from PIL import Image
from PIL.ImageQt import ImageQt


class MainWindow(QMainWindow):
    
    def __init__ (self, window_size, shapes):
        super().__init__()
        
        # Initializing Values
        self.setWindowTitle("These Look Like Planets - Aiden Yeo")
        self.window_size = window_size
        self.shapes = shapes
    
        self.create_pixmap(window_size, shapes)

        

    def create_pixmap(self, window_size, shapes):
        baseimg = get_image_efficient(shapes, window_size[0], window_size[1])
        
        imageqt = ImageQt(baseimg)
        img2 = QtGui.QImage(imageqt)
        pixmap = QtGui.QPixmap.fromImage(img2)
        #pixmap = QPixmap.fromImage(qim)
        #pixmap = QPixmap()
        
        """ 
        button = QPushButton("Advance Them Planets")
        button.setCheckable(True)
        button.clicked.connect(self.update_view)
        """
        label = QLabel()
       
        label.setPixmap(pixmap)
        label.resize(pixmap.width(), pixmap.height())
        self.setCentralWidget(label)



    def update_view(self):
        img = get_image_efficient(self.shapes, self.window_size[0], self.window_size[1])
        print("uronon")
        
        

        
        