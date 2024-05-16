from numpy import sin, cos, radians
import pygame

# PART 0: initial condition

m1 = 1
m2 = 1
l1 = 1
l2 = 1

g = 1.5

a1 = radians(200)
a2 = radians(120)
p1 = 0
p2 = 0

fps_limit = 60
dt = fps_limit/1000

# PART 1: solving the ODE

'''

Solving the Hamilton equations (d=2, so 4 equations) using Runge-Kutta at 4th order.


'''

def A1(a1, a2, p1, p2):
    num = p1*p2*sin(a1-a2)
    denom = l1*l2*(m1 + m2*sin(a1-a2)*sin(a1-a2))
    return num/denom

def A2(a1, a2, p1, p2):
    num = (p1*p1*m2*l2*l2 - 2*p1*p2*m2*l1*l2*cos(a1-a2) + p2*p2*(m1+m2)*l1**2)*(sin(2*(a1-a2)))
    denom = 2*l1*l1*l2*l2*(m1+m2*sin(a1-a2)*sin(a1-a2))
    return num/denom

def p1_f(a1, a2, p1, p2):
    return -(m1+m2)*g*l1*sin(a1)  - A1(a1, a2, p1, p2) + A2(a1, a2, p1, p2)

def p2_f(a1, a2, p1, p2):
    return -m2*g*l2*sin(a2) + A1(a1, a2, p1, p2) - A2(a1, a2, p1, p2)

def a1_f(a1, a2, p1, p2):
    num = p1*l2-p2*l1*cos(a1-a2)
    denom = l1*l1*l2*(m1+m2*sin(a1-a2)*sin(a1-a2))
    return num/denom

def a2_f(a1, a2, p1, p2):
    num = p2*(m1+m2)*l1 - p1*m2*l2*cos(a1-a2)
    denom = m2*l1*l2*l2*(m1+m2*sin(a1-a2)*sin(a1-a2))
    return num/denom

def equations_of_motion_system(a1, a2, p1, p2):
    return a1_f(a1, a2, p1, p2), a2_f(a1, a2, p1, p2), p1_f(a1, a2, p1, p2), p2_f(a1, a2, p1, p2)



def RungeKutta_solver(function, q1, q2, p1, p2, dt):
    
    k1_q1, k1_q2, k1_p1, k1_p2 = function(q1, q2, p1, p2)
    
    k1_q1 *= dt
    k1_q2 *= dt
    k1_p1 *= dt
    k1_p2 *= dt
    
    k2_q1, k2_q2, k2_p1, k2_p2 = function(q1 + dt/2*k1_q1, q2 + dt/2*k1_q2, p1 + dt/2*k1_p1, p2 + dt/2*k1_p2)
    k3_q1, k3_q2, k3_p1, k3_p2 = function(q1 + dt/2*k2_q1, q2 + dt/2*k2_q2, p1 + dt/2*k2_p1, p2 + dt/2*k2_p2)
    k4_q1, k4_q2, k4_p1, k4_p2 = function(q1 + dt*k3_q1, q2 + dt*k3_q2, p1 + dt*k3_p1, p2 + dt*k3_p2)
    
    q1 += dt/6 * (k1_q1 + 2*k2_q1 + 2*k3_q1 + k4_q1)
    q2 += dt/6 * (k1_q2 + 2*k2_q2 + 2*k3_q2 + k4_q2)
    p1 += dt/6 * (k1_p1 + 2*k2_p1 + 2*k3_p1 + k4_p1)
    p2 += dt/6 * (k1_p2 + 2*k2_p2 + 2*k3_p2 + k4_p2)
    
    return q1, q2, p1, p2

class PendulumMovement:
    
    '''
    there we put the angles variations, then the real position (x,y) is put in classes that defines the masses
    '''
    
    def __init__(self, a1, a2, p1, p2):
        self.a1 = a1
        self.a2 = a2
        self.p1 = p1
        self.p2 = p2
        
    def movement(self, dt):
        a1_0 = self.a1
        a2_0 = self.a2
        p1_0 = self.p1
        p2_0 = self.p2
        self.a1, self.a2, self.p1, self.p2 = RungeKutta_solver(equations_of_motion_system, a1_0, a2_0, p1_0, p2_0, dt)
        return self.a1, self.a2
        

# --------------------------------------------------------------------------------------------------- #

# PART 2: showing the motion

red = 255,0,0
gray = 100,100,100
white = 255,255,255

screen_lenght = 800
screen_high = 600
screen = pygame.display.set_mode((screen_lenght, screen_high),0,32)

pygame.display.set_caption('Double Pendulum')

clock = pygame.time.Clock()


class MyCircle:
    
    def __init__(self, x, y, radius, color = red):
        self.x = x
        self.y = y
        self.radius = radius
        self.width = radius
        self.color = color
    
    def new_position(self, x, y):
        self.x = x
        self.y = y
       
    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.width)


class MyLine:
    
    def __init__(self, x1, y1, x2, y2, line_width = 2, color = gray):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2_y = y2
        self.line_width = line_width
        self.color = color
        
    def new_position(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def display(self):
        pygame.draw.line(screen, self.color, (self.x1, self.y1), (self.x2, self.y2), self.line_width)
        

pivot_x = screen_lenght/2
pivot_y = 250

rope1_lenght = l1*100
rope2_lenght = l2*100

x1 = pivot_x + rope1_lenght * sin(a1)
y1 = pivot_y + rope1_lenght * cos(a1)

x2 = x1 + rope2_lenght * sin(a2)
y2 = y1 + rope2_lenght * cos(a2)

mass1 = MyCircle(x1, y1, 8)
mass2 = MyCircle(x2, y2, 8)
pivot = MyCircle(pivot_x, pivot_y, 4, color=gray)
rope1 = MyLine(pivot_x, pivot_y, x1, y1, 3)
rope2 = MyLine(x1, y1, x2, y2, 3)

pendulum_movement = PendulumMovement(a1,a2,p1,p2)

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(color=white)
    
    clock.tick(fps_limit)
    
    a1,a2 = pendulum_movement.movement(dt)
    
    x1 = pivot_x + rope1_lenght * sin(a1)
    y1 = pivot_y + rope1_lenght * cos(a1)
    x2 = x1 + rope2_lenght * sin(a2)
    y2 = y1 + rope2_lenght * cos(a2)
    
    mass1.new_position(x1,y1)
    mass2.new_position(x2,y2)
    rope1.new_position(pivot_x,pivot_y,x1,y1)
    rope2.new_position(x1,y1,x2,y2)
    
    rope1.display()
    rope2.display()
    pivot.display()
    mass1.display()
    mass2.display()
    
    pygame.display.flip()
    
pygame.quit()