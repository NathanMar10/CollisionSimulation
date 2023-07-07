import pygame
import Shapes
import circle

pygame.init()
clock = pygame.time.Clock()

# Window Config Area
SCREEN_SIZE = (1800, 1000)
SCREEN_NAME = "Wow, Nate! These really look like planets! -Aiden"
MAX_FPS = 60
SUBFRAMES = 1

root = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(SCREEN_NAME)

# Game Config Area - Motion Values are Time-Dependent
# I want to save some config files because that would be cool
CIRCLE_COUNT = 500
VELOCITY_RANGE = (20, 100)
SIZE_RANGE = (20, 50)

#COR, Unstack Shapes
COLLISIONS = (1, False)
#Big G, Calculate Gravity
GRAVITY = (.00005, False)
#K, Calculate Charge
ELECTRICITY = (400000, False)
SEED = "surprie"



# Here we have a variable-sized array of "pixels".
controller = Shapes.Controller(SCREEN_SIZE, CIRCLE_COUNT, VELOCITY_RANGE,
                               SIZE_RANGE, COLLISIONS, GRAVITY, ELECTRICITY, SEED,
                               root)


def runframe(controller, delta_t):
    controller.move_shapes(delta_t)
    #controller.unstack_circles()
    #controller.unstack_circles()
    #controller.solve_collisions()
    controller.solve_collisions_optimized()
    #controller.calculate_force(delta_t)

def display_shapes(controller, root):
    root.fill((0, 0, 0))
    for shape in controller.shapes:
        root.blit(shape.pygame_image, dest = (shape.position[0] - shape.size - 1, shape.position[1] - shape.size - 1))

exit = False

while not exit:
    delta_t = clock.tick(MAX_FPS) / 1000.0
    for x in range(SUBFRAMES):
        runframe(controller,delta_t / SUBFRAMES)
    display_shapes(controller, root)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           exit = True















