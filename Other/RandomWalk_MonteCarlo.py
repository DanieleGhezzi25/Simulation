'''

    Prove that the mean squared displacement of a random walk
    is proportional to the number of steps taken (2 dimensions).

'''

import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit, LeastSquares

def random_walk(N):
    # N is the number of steps
    x = 0
    y = 0
    for i in range(N):
        x += np.random.choice([-1, 1])
        y += np.random.choice([-1, 1])
    return x**2 + y**2

mean_squared_list = []
mean_squared_errors = []
N_steps = np.arange(10, 200, 10)
for i in N_steps:
    list = []
    for j in range(1000):
        list.append(random_walk(i))
    mean_squared_list.append(np.mean(list))
    mean_squared_errors.append(np.std(list)/np.sqrt(len(list)))

plt.plot(N_steps, mean_squared_list)
plt.errorbar(N_steps, mean_squared_list, yerr=mean_squared_errors, fmt='o')
plt.xlabel('Number of steps')
plt.ylabel('Mean squared displacement')

plt.show()


