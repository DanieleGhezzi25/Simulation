# Fourier Series y = x*cosx in I = [-pi, pi], T = 2pi

import numpy as np
import matplotlib.pyplot as plt

def series_x2(x, k):
    return np.array(4*((-1)**k/k**2)*np.cos(k*x))

def series_xcosx(x, k):
    return np.array((((-1)**k)*2*k*np.sin(k*x))/(k**2-1))

def main():
    
    x_coord = np.linspace(-4*np.pi, 4*np.pi, 20000)
    y_coord = np.zeros(len(x_coord))
    k = 5
    
    for i in range(2, k):
        y_coord_tmp = series_xcosx(x_coord, i)
        y_coord = y_coord + y_coord_tmp
            
    y_coord = y_coord - 0.5*(np.sin(x_coord)) # a0/2
    
    plt.plot(x_coord, y_coord)
    
    plt.show()
    
if __name__ == "__main__":
    main()
    