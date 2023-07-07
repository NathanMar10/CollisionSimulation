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
    
    
    def __init__(self, screen_size, circle_count, velocity_range, size_range, collision_properties, gravity_properties, electric_properties, seed, pygame_window):
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.velocity_range = velocity_range
        self.size_range = size_range
        self.shapes = []
        
        self.wall_v_loss = collision_properties[0]
        self.coeff_restitution = collision_properties[0]
        self.big_g = gravity_properties[0]
        self.lil_k = electric_properties[0]

        self.unstack = collision_properties[1]
        self.use_gravity = gravity_properties[1]
        self.use_electric = electric_properties[1]

        self.pygame_window = pygame_window

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
        self.shapes.append(circle.Circle([1000, 500], 30, [0, 0], (0, 255, 255)))
        self.shapes.append(circle.Circle([600, 600], 7, [150, 200], (255, 0, 0)))
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




    def move_shapes(self, delta_t):
        
        for shape in self.shapes:
            #print(shape.position)
            shape.position[0] += shape.velocity[0] * delta_t
            shape.position[1] += shape.velocity[1] * delta_t
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
                        
                      
    def solve_collisions_optimized(self):
        # segments the space into the necessary smaller groups to allow for more efficient calculation
        split_field(self.shapes, False, self)
        # this is literally just recursive... right? I guess this has to call it with the proper arg




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



    def calculate_force(self, delta_t):
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

                shapes[a].velocity[0] += (force_vector[0] / shapes[a].mass) * delta_t
                shapes[a].velocity[1] += (force_vector[1] / shapes[a].mass) * delta_t
                shapes[b].velocity[0] -= (force_vector[0] / shapes[b].mass) * delta_t
                shapes[b].velocity[1] -= (force_vector[1] / shapes[b].mass) * delta_t
        
def get_distance(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**(1/2)



def check_lists(list_first: list, list_second: list, vertical_prev: bool, controller):
    if len(list_first) == len(list_second) or len(list_second) <= 2:
        check_collisions(list_second, controller)
    else:
        split_field(list_second, vertical_prev, controller)


# Splits the game into two sections to simplify collision checks
def split_field(shapes_list: list, last_split_vertical: bool, controller):

    # Determines which direction to split
    if last_split_vertical:
        shapes_list.sort(key=getHorizontalPos)
        direction_index = 0
    else:
        shapes_list.sort(key=getVerticalPos)
        direction_index = 1

    # Finding the Value to split at
    list_len = len(shapes_list)
    if list_len % 2 == 0:
        mid_val = shapes_list[(int)(list_len / 2)].position[direction_index] + shapes_list[(int)(list_len / 2) - 1].position[direction_index]
    else:
        mid_val = shapes_list[(int)(numpy.ceil(list_len / 2))].position[1]

    lower_list = []
    upper_list = []

    for shape in shapes_list:
        if shape.position[direction_index] <= mid_val:
            lower_list.append(shape)
        if shape.position[direction_index] >= mid_val:
            upper_list.append(shape)

    # Checks if the splits did anything and continues if they did
    check_lists(shapes_list, lower_list, not last_split_vertical, controller)
    check_lists(shapes_list, upper_list, not last_split_vertical, controller)



def check_collisions(circles: list, controller):
    for a in range(len(circles)):
        for b in range( a + 1, len(circles)):
            A = circles[a]
            B = circles[b]
            distance = get_distance(A.position, B.position)
            if (distance <= (A.size + B.size)):
                net_v = (A.velocity[0] - B.velocity[0], A.velocity[1] - B.velocity[1])
                delta_p = (A.position[0] - B.position[0], A.position[1] - B.position[1])
                if (numpy.dot(net_v, delta_p) < 0):
                    # If we reach here, then we are colliding
                    execute_collision(A, B, distance, controller)




def execute_collision(A: circle, B: circle, distance: float, controller):
    # input two circles that are colliding to update their values (ill also input some info from prev function)
    mass_ratio = B.mass / A.mass

    # Pretty sure angle things are also correct (rejecting nested shapes rn)
    diff_y = B.position[1] - A.position[1]
    angle = numpy.arccos((B.position[0] - A.position[0]) / distance)
    if (diff_y < 0):
        angle = (2 * numpy.pi) - angle

    Azi = A.velocity[0] * numpy.cos(angle) + A.velocity[1] * numpy.sin(angle)
    Awi = A.velocity[1] * numpy.cos(angle) - A.velocity[0] * numpy.sin(angle)
    Bzi = B.velocity[0] * numpy.cos(angle) + B.velocity[1] * numpy.sin(angle)
    Bwi = B.velocity[1] * numpy.cos(angle) - B.velocity[0] * numpy.sin(angle)

    # Its just gotta be my working it out with a pencil
    Bzf = ((mass_ratio * Bzi + Azi) + controller.coeff_restitution * (Azi - Bzi)) / (1 + mass_ratio)

    Azf = mass_ratio * (Bzi - Bzf) + Azi


    A.velocity[0] = Azf * numpy.cos(-angle) + Awi * numpy.sin(-angle)
    A.velocity[1] = Awi * numpy.cos(-angle) - Azf * numpy.sin(-angle)
    B.velocity[0] = Bzf * numpy.cos(-angle) + Bwi * numpy.sin(-angle)
    B.velocity[1] = Bwi * numpy.cos(-angle) - Bzf * numpy.sin(-angle)


def getHorizontalPos(circle: circle.Circle):
    return circle.position[0]

def getVerticalPos(circle: circle.Circle):
    return circle.position[1]
