'''

Animation of the heat equation with a Gaussian initial condition on an infinite bar.

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


a = 2 # gaussian standard deviation
T_peak = 200 # peak temperature
k = 2.3e-5 # thermal diffusivity (iron)
dt = 600 # time step in seconds
time_counting = 10 # milliseconds

def HeatFunction(x,t):
    return (a*T_peak)/(np.sqrt(2*k*t+a**2))*np.exp(-1/(4*k*t+2*a**2) * x**2)

x = np.linspace(-20,20,1000)
t = 0

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
plt.title(f'Heat Equation with Gaussian Initial Condition: T max = {T_peak}, dt = {dt}s')
plt.grid(True)

plt.show()