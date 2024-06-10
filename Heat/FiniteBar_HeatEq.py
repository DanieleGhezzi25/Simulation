'''

Animation of the heat equation with a constant initial condition on a finite bar (length l).
    Equation solved analytically with Fourier Series.

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

l = 5 # length of the bar
T = 20 # temperature of the bar
k = 2.3e-5 # thermal diffusivity (iron)
dt = 3600 # time step in seconds
time_counting = 10 # milliseconds

x = np.linspace(0,l,1000)
t = 0
N_sum = 1000

def HeatFunction(x,t):
    u_x = np.zeros(len(x))
    for i in range(N_sum):
        u_x += 2*np.sqrt(2)*T/(np.pi*(2*i+1))*np.sin((2*i+1)*np.pi*x/l)*np.exp(-k*(2*i+1)**2*np.pi**2*t/l**2)
    return u_x

fig, ax = plt.subplots()
line, = ax.plot(x, HeatFunction(x,0), color='red',  label=f't = {t} s')
legend = ax.legend()

def init():
    # Initialize the animation frame
    global t
    t = 0  # Reset the time to zero
    line.set_ydata(HeatFunction(x, t))
    legend.get_texts()[0].set_text(f't = {t / 3600:.2f} h')
    return line, legend

def animate(i):
    global t
    if i != 0:  # skip incrementing t for the first frame
        t += dt
    line.set_ydata(HeatFunction(x,t))
    legend.get_texts()[0].set_text(f't = {t/3600:.2f} h')
    return line, legend

ani = animation.FuncAnimation(fig, animate, init_func=init, interval=time_counting, blit=True, save_count=100)

plt.xlabel('x')
plt.ylabel('Temperature')
plt.title(f'Heat Equation with constant initial condition: T = {T}, dt = {dt}s')
plt.grid(True)

plt.show()
