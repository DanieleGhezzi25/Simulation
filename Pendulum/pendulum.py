import numpy, pygame, pygame.mixer
from pygame.locals import *

# some colours
red = 255,0,0
white = 255,255,255
blue = 0,0,255
gray = 128,128,128

g_costant = 60

screen_lenght = 700
screen_high = 600
screen = pygame.display.set_mode((screen_lenght, screen_high),0,32)
pygame.display.set_caption('Pendulum')

clock = pygame.time.Clock()


class MyCircle:
    
    def __init__(self, x, y, radius, color = blue):
        self.x = x
        self.y = y
        self.radius = radius
        self.width = radius # cerchio pieno
        self.color = color
    
    def new_position(self, x, y):
        self.x = x
        self.y = y
       
    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.width)


class MyLine:
    
    def __init__(self, point1, x, y, line_width, color = gray):
        self.point1 = point1
        self.point2_x = x
        self.point2_y = y
        self.line_width = line_width
        self.color = color
        
    def new_position(self, x, y):
        self.point2_x = x
        self.point2_y = y
    
    def display(self):
        pygame.draw.line(screen, self.color, self.point1, (self.point2_x, self.point2_y), self.line_width)


class PendulumMovement:
    
    def __init__(self, x, y, theta, lenght, velocity):
        self.x = x
        self.y = y
        self.theta = theta
        self.lenght = lenght
        self.velocity = velocity
        self.acceleration = -g_costant*numpy.sin(self.theta)/self.lenght
        
    def position(self, dt):
        self.acceleration = -g_costant*numpy.sin(self.theta)/self.lenght
        self.velocity += self.acceleration * dt
        self.theta += self.velocity * dt
        self.x = pivot_x + self.lenght * numpy.sin(self.theta)
        self.y = pivot_y + self.lenght * numpy.cos(self.theta)        
        return self.x, self.y


theta0 = 150 # degrees
theta0 = numpy.radians(theta0)
rope_lenght = 200 # pixels

pivot_x = screen_lenght/2
pivot_y = 250

x0 = pivot_x + rope_lenght * numpy.sin(theta0)
y0 = pivot_y + rope_lenght * numpy.cos(theta0)
v0 = 0

mass = MyCircle(x0, y0, 10)
pivot = MyCircle(pivot_x, pivot_y, 5, color=gray)
rope = MyLine((pivot_x, pivot_y), x0, y0, 3)

pendulum_movement = PendulumMovement(x0, y0, theta0, rope_lenght, v0)

fps_limit = 60
dt = fps_limit/1000
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(color=white)
    
    clock.tick(fps_limit)
    
    x,y = pendulum_movement.position(dt)
    
    mass.new_position(x,y)
    rope.new_position(x,y)
    
    rope.display()
    pivot.display()
    mass.display()
    
    pygame.display.flip()
    
pygame.quit()