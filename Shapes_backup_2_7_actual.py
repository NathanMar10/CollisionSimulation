# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 18:36:44 2022

@author: thena
"""
from PIL import Image, ImageDraw
import numpy
import random
import circle


class Controller:
    
    
    def __init__(self, screen_size, circle_count, velocity_range, size_range, coeff_restitution, big_g, lil_k, seed):
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.velocity_range = velocity_range
        self.size_range = size_range
        self.shapes = []
        
        self.wall_v_loss = coeff_restitution
        self.coeff_restitution = coeff_restitution
        self.big_g = big_g
        self.lil_k = lil_k

        
        self.create_circles(circle_count)
        if (seed == "surprise"):
            random.seed()
        else:        
            random.seed(seed)
            
        
    def create_circles(self, count):
    
        vel = 24.2
        """
        self.shapes.append(Circle([self.width / 2, self.height / 2], 100, [0, 0], (255, 255, 255)))    
        self.shapes.append(Circle([self.width / 2 - 400, self.height / 2], 5, [0, -vel], (100, 255, 120)))   
        self.shapes.append(Circle([self.width / 2 + 400, self.height / 2], 5, [0, vel], (120, 100, 120))) 
        self.shapes.append(Circle([self.width / 2, self.height / 2 - 400], 5, [vel, 0], (255, 12, 120)))   
        self.shapes.append(Circle([self.width / 2, self.height / 2 + 400], 5, [-vel, 0], (0, 255, 200)))  
        """
    
        for shape in range(count):
            position = [random.random()*self.width, random.random()*self.height]
            velocityx = (random.random() - .5) * 2 * self.velocity_range[1]
            velocityy = (random.random() - .5) * 2 * self.velocity_range[1]

            """
            if random.randint(0, 4) == 0:
                color = (random.randint(0, 255), random.randint(0, 120), random.randint(0, 120))
            elif random.randint(0, 3) == 0:
                color = (random.randint(0, 120),random.randint(0, 255), random.randint(0, 120))
            elif random.randint(0, 2) == 0:
                color = (random.randint(0, 120), random.randint(0, 120), random.randint(0, 255))
            """
            color = color = (random.randint(10, 255), random.randint(10, 255), random.randint(10, 255))


            #print(color)
            #color = (start, start, start)
            #start += 30
            """
            if (random.random() > .66):
                color = (0, 90, 0)
            elif (random.random() > .66):
                color = (56, 56, 56)
            else:
                color = (165, 165, 56)  
            """
            size = int(numpy.floor(max(random.gauss(2, 5) * (self.size_range[1] /10), self.size_range[0])))
            """
            if count == 0:
                size = 10
                print(size)
            elif count == 1:
                size = 200
                print(size)
            count+= 1
            """
            self.shapes.append(circle.Circle(position, size, [velocityx, velocityy], color))
        self.unstack_circles()


    def place_images(self):
        for shape in self.shapes:
            shape.label.place(x=int(shape.position[0]), y=int(shape.position[1]), anchor="sw")

    def place_on_canvas(self, canvas):
        canvas.delete('all')
        for shape in self.shapes:
            canvas.create_image(shape.position[0], shape.position[1], image=shape.image)



    def get_image_library(self):
        img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        # img = self.img

        draw = ImageDraw.Draw(img)
        for circle in self.shapes:

            # Called for each circle and then we can determine the valid x & y values
            x_max = min(circle.position[0] + circle.size * .8, self.width - 1)
            x_min = max(circle.position[0] - circle.size * .8, 0)
            y_max = min(circle.position[1] + circle.size * .8, self.height - 1)
            y_min = max(circle.position[1] - circle.size * .8, 0)
            draw.ellipse((x_min, y_min, x_max, y_max), fill = circle.color)

        return img




    def get_image_efficient(self):
        
        img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        #img = self.img
        
        for circle in self.shapes:

            #Called for each circle and then we can determine the valid x & y values
            x_max = min(circle.position[0] + circle.size * .8, self.width - 1)
            x_min = max(circle.position[0] - circle.size * .8, 0)



            """
            iterating over xmin to xmax -> which are the extreme values of everything
            I can literlaly just use that exact value of x, since they are the further side of the pixel
            check what y value i need
            shrink range
            
            color
            """


            for x in range(int(numpy.ceil(x_min)), int(numpy.floor(x_max))):
                # Called for each x value in the range
                x_at_point = circle.position[0] - x

                y_half_width = numpy.sqrt(circle.size**2 - x_at_point**2)
                y_range = [int(numpy.ceil(-y_half_width + circle.position[1])), int(numpy.floor(y_half_width + circle.position[1]))]
                y_range[0] = max(y_range[0],0)
                y_range[1] = min(y_range[1], self.height - 1)
                #print(y_range)
                """
                if circle.size < 10:
                    for y in range (y_range[0], y_range[1]):
                        img.putpixel((x, y), circle.color)
                """

                for y in (y_range[0], y_range[1]):
                    """
                    print("top")
                    print(x, y)
                    """
                    img.putpixel((x, y), circle.color)



            y_max = min(circle.position[1] + circle.size * .8, self.height - 1)
            y_min = max(circle.position[1] - circle.size * .8, 0)

            for y in range(int(numpy.ceil(y_min)), int(numpy.floor(y_max))):
                # Called for each x value in the range
                y_at_point = circle.position[1] - y

                x_half_width = numpy.sqrt(circle.size**2 - y_at_point**2)
                x_range = [int(numpy.ceil(circle.position[0] - x_half_width)), int(numpy.floor(x_half_width + circle.position[0]))]
                x_range[0] = max(x_range[0],0)
                x_range[1] = min(x_range[1], self.width - 1)
                #print(y_range)

                for x in (x_range):
                    """
                    print("bottom")
                    print(x, y)
                    """
                    img.putpixel((x, y), circle.color)







        return img
    



    def move_shapes(self):
        
        for shape in self.shapes:
            #print(shape.position)
            shape.position[0] += shape.velocity[0]
            shape.position[1] += shape.velocity[1]
            #print("+" + str(shape.velocity))
            #print(shape.position)
            
            if ((shape.position[0] <= shape.size and shape.velocity[0] < 0) or (shape.position[0] >= self.width - shape.size and shape.velocity[0] > 0)):
                shape.velocity[0] *= -self.wall_v_loss
                if (abs(shape.velocity[0]) > self.width):
                    shape.velocity[0] *= 1/100
            if ((shape.position[1] <= shape.size and shape.velocity[1] < 0) or (shape.position[1] >= self.height - shape.size and shape.velocity[1] > 0)):
                shape.velocity[1] *= -self.wall_v_loss
                if (abs(shape.velocity[1]) > self.height):
                    shape.velocity[1] *= 1/50
            shape.position[0] = min(max(shape.position[0], shape.size), self.width - shape.size)
            shape.position[1] = min(max(shape.position[1], shape.size), self.height - shape.size)
            
           
       
            
    def unstack_circles(self):
        for a in range(len(self.shapes)):
            for b in range(a + 1, len(self.shapes)):
                # This will be called for each shape combination (yay!)
                
                if (get_distance(self.shapes[a].position, self.shapes[b].position) <= self.shapes[a].size + self.shapes[b].size):
                    # This is the collision Condition
                    # I will also keep a set of tuples with the most recent boys who collided and if theyre still on that list it doesnt collide again
                    
                    """ Defining my Values for Future Equations """

                    A = self.shapes[a]
                    B = self.shapes[b]
                    
                    if (B.size > A.size):
                        temp = B
                        B = A
                        A = temp
                    
                    distance = get_distance(A.position, B.position)
                    diff_y = B.position[1] - A.position[1]
                    angle = numpy.arccos((B.position[0] - A.position[0]) / distance)
                    if (diff_y < 0):
                        angle = (2 * numpy.pi) - angle
                    
                    B.position[0] = A.position[0] + numpy.cos(angle)*(A.size + B.size)
                    B.position[1] = A.position[1] + numpy.sin(angle)*(A.size + B.size)
                        
                      

            
    def solve_collisions(self):
        # For each shape, check each shaper later in the list if their distance is collidable
        for a in range(len(self.shapes)):
            for b in range(a + 1, len(self.shapes)):
                # This will be called for each shape combination (yay!)
                
                if (get_distance(self.shapes[a].position, self.shapes[b].position) <= self.shapes[a].size + self.shapes[b].size):
                    # This is the collision Condition
                    # I will also keep a set of tuples with the most recent boys who collided and if theyre still on that list it doesnt collide again
                    """ Defining my Values for Future Equations """

                    A = self.shapes[a]
                    B = self.shapes[b]
                    
                    

                    net_v = (A.velocity[0] - B.velocity[0], A.velocity[1] - B.velocity[1])
                    delta_p = (A.position[0] - B.position[0], A.position[1] - B.position[1])
                    if (numpy.dot(net_v, delta_p) < 0):
                                             
                    
                    
                    
                        mass_ratio = B.mass / A.mass
                        distance = get_distance(A.position, B.position)
                        
                        # Pretty sure angle things are also correct (rejecting nested shapes rn)
                        diff_y = B.position[1] - A.position[1]
                        angle = numpy.arccos((B.position[0] - A.position[0]) / distance)
                        if (diff_y < 0):
                            angle = (2 * numpy.pi) - angle
                        
                        
                        
                        Azi = A.velocity[0] * numpy.cos(angle) + A.velocity[1] * numpy.sin(angle)
                        Awi = A.velocity[1] * numpy.cos(angle) - A.velocity[0] * numpy.sin(angle)
                        Bzi = B.velocity[0] * numpy.cos(angle) + B.velocity[1] * numpy.sin(angle)
                        Bwi = B.velocity[1] * numpy.cos(angle) - B.velocity[0] * numpy.sin(angle)
                        
                        """ Backed Up equations
                        # Pretty sure axis conversions are correct
                        Azi = A.velocity[0] * numpy.cos(angle) + A.velocity[1] * numpy.sin(angle)
                        Awi = A.velocity[0] * numpy.sin(angle) - A.velocity[1] * numpy.cos(angle)
                        Bzi = B.velocity[0] * numpy.cos(angle) + B.velocity[1] * numpy.sin(angle)
                        Bwi = B.velocity[0] * numpy.sin(angle) - B.velocity[1] * numpy.cos(angle)
                        """
                        # Its just gotta be my working it out with a pencil
                        Bzf = ((mass_ratio * Bzi + Azi) + self.coeff_restitution * (Azi - Bzi)) / (1 + mass_ratio)
                        

                        Azf = mass_ratio * (Bzi - Bzf) + Azi
                        """
                        if (numpy.sign(Bzi - Azi) == numpy.sign(Bzf - Azf)):
                            Bzf = ((mass_ratio * Bzi - Azi) + self.coeff_restitution * (Bzi - Azi)) / (1 + mass_ratio)
                            Azf = mass_ratio * (Bzi - Bzf) + Azi
                        
                        
                        if (False):
                            Bzf = ((mass_ratio * Bzi - Azi) - self.coeff_restitution * abs(Bzi - Azi)) / (1 + mass_ratio)
                        """
                        
                        A.velocity[0] = Azf * numpy.cos(-angle) + Awi * numpy.sin(-angle)
                        A.velocity[1] = Awi * numpy.cos(-angle) - Azf * numpy.sin(-angle)
                        B.velocity[0] = Bzf * numpy.cos(-angle) + Bwi * numpy.sin(-angle)
                        B.velocity[1] = Bwi * numpy.cos(-angle) - Bzf * numpy.sin(-angle)
                      
                        
                        """
                        # Pretty Sure axis conversions are correct
                        A.velocity[0] = Azf * numpy.cos(angle) + Awi * numpy.sin(angle)
                        A.velocity[1] = - Azf * numpy.sin(angle) + Awi * numpy.cos(angle)
                        B.velocity[0] = Bzf * numpy.cos(angle) + Bwi * numpy.sin(angle)
                        B.velocity[1] = - Bzf * numpy.sin(angle) + Bwi * numpy.cos(angle)
                        """
                        """
                        # Strictly Testing
                        print("----")
                        print("A:" + str(Awi) + ", B:" + str(Bwi))
                        Awf = A.velocity[0] * numpy.sin(angle) - A.velocity[1] * numpy.cos(angle)
                        Bwf = B.velocity[0] * numpy.sin(angle) - B.velocity[1] * numpy.cos(angle)
                        print("A:" + str(Awf) + ", B:" + str(Bwf))
                    
                        numerator = Bzf - Azf
                        denominator = -Bzi + Azi
                        print(numerator / denominator)
                        """
                        
    def calculate_gravity(self):
        shapes = self.shapes
        for a in range(len(self.shapes)):
            for b in range(a + 1, len(self.shapes)):
                # Called for each combo
                force = self.big_g * shapes[a].mass * shapes[b].mass / (get_distance(shapes[a].position, shapes[b].position))**2
                distance_vector = (shapes[b].position[0] - shapes[a].position[0], shapes[b].position[1] - shapes[a].position[1])
                magnitude = (distance_vector[0]**2 + distance_vector[1]**2)**1/2
                unit_distance = (distance_vector[0] / magnitude, distance_vector[1] / magnitude)
                
                force_vector = (unit_distance[0] * force, unit_distance[1] * force)
                
                shapes[a].velocity[0] += force_vector[0] / shapes[a].mass
                shapes[a].velocity[1] += force_vector[1] / shapes[a].mass
                shapes[b].velocity[0] -= force_vector[0] / shapes[b].mass
                shapes[b].velocity[1] -= force_vector[1] / shapes[b].mass
        
    def calculate_charge(self):
        shapes = self.shapes
        for a in range(len(self.shapes)):
            for b in range(a + 1, len(self.shapes)):
                force = - self.lil_k * shapes[a].charge * shapes[b].charge / (get_distance(shapes[a].position, shapes[b].position))**2
                distance_vector = (shapes[b].position[0] - shapes[a].position[0], shapes[b].position[1] - shapes[a].position[1])
                magnitude = (distance_vector[0]**2 + distance_vector[1]**2)**1/2
                unit_distance = (distance_vector[0] / magnitude, distance_vector[1] / magnitude)
                
                force_vector = (unit_distance[0] * force, unit_distance[1] * force)
                
                shapes[a].velocity[0] += force_vector[0] / shapes[a].mass
                shapes[a].velocity[1] += force_vector[1] / shapes[a].mass
                shapes[b].velocity[0] -= force_vector[0] / shapes[b].mass
                shapes[b].velocity[1] -= force_vector[1] / shapes[b].mass



    def calculate_force(self):
        shapes = self.shapes
        for a in range(len(self.shapes)):
            for b in range(a + 1, len(self.shapes)):
                distance_magnitude = get_distance(shapes[a].position, shapes[b].position)
                electric_force = - self.lil_k * shapes[a].charge * shapes[b].charge / (distance_magnitude) ** 2
                gravity_force = self.big_g * shapes[a].mass * shapes[b].mass / (distance_magnitude) ** 2
                distance_vector = (
                shapes[b].position[0] - shapes[a].position[0], shapes[b].position[1] - shapes[a].position[1])

                unit_distance = (distance_vector[0] / distance_magnitude, distance_vector[1] / distance_magnitude)

                force_vector = (unit_distance[0] * (gravity_force + electric_force), unit_distance[1] * (gravity_force + electric_force))

                shapes[a].velocity[0] += force_vector[0] / shapes[a].mass
                shapes[a].velocity[1] += force_vector[1] / shapes[a].mass
                shapes[b].velocity[0] -= force_vector[0] / shapes[b].mass
                shapes[b].velocity[1] -= force_vector[1] / shapes[b].mass
        
def get_distance(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**(1/2)
            