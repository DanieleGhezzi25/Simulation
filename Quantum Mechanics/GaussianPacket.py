'''

    Evolution of a gaussian wave function in an infinite square well potential [0, a] according to the time-independent Schrödinger equation.

'''

import numpy as np
from numpy import sqrt, sin, pi, exp
from scipy.integrate import quad
import matplotlib.pyplot as plt
import keyboard

# Initial Condition
a = 5
m = 2 #9.11e-31
h = 1.2 #1.05459e-34
p0 = 0

N = 200
dt = 0.01

def HilbertBase(x,n):
    return sqrt(2/a)*sin(n*pi*x/a)

def wavefunc0(x):
    return pow(2*a/pi, 1/4)*exp(-a*(x-a/2)**2)*exp(1j/h*p0*x)

def wavefunc1(x):
    return sqrt(30/a**5)*x*(a-x)*exp(1j/h*p0*x)

def energy(n):
    return h**2*pi**2*n**2/(2*m*a**2)

def main():

    t = 0.

    xpoints = np.linspace(0, a, 1000)
    cn = []

    fig, ax = plt.subplots()
    line, = ax.plot(xpoints, np.zeros(len(xpoints)), lw=2, color='red', label='Re(ψ(x, t))', )
    line2, = ax.plot(xpoints, np.zeros(len(xpoints)), lw=2, color='blue', label='Im(ψ(x, t))')
    line3, = ax.plot(xpoints, np.zeros(len(xpoints)), lw=2, color='green', label='|ψ(x, t)|^2')
    ax.set_xlim(-0.2, a+0.2)
    ax.set_ylim(-1.5, 3)
    ax.set_title("Time evolution of a Gaussian wave function in an infinite well potential")
    ax.set_xlabel("Position x")
    ax.set_ylabel("ψ(x, t)")
    ax.grid()
    ax.legend()

    for n in range(1,N):
        cn.append(quad(lambda x: wavefunc0(x) * HilbertBase(x,n), 0, a)[0])

    while True:

        psi_values = np.zeros(len(xpoints), dtype=complex)

        for n in range(1,N):
            psi_values += cn[n-1]*HilbertBase(xpoints,n)*exp(-1j/h * energy(n) * t)

        wavefunc_real = np.real(psi_values)
        wavefunc_imag = np.imag(psi_values)
        wavefunc_mod = wavefunc_real**2 + wavefunc_imag**2

        line.set_ydata(wavefunc_real)
        line2.set_ydata(wavefunc_imag)
        line3.set_ydata(wavefunc_mod)

        plt.pause(0.005)

        t += dt

        if keyboard.is_pressed('q'):
            plt.close()
            break

    return

if __name__ == "__main__":
    main()