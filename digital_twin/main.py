import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random as rnd

ax = plt.axes(projection='3d')
line, = ax.plot3D([], [], [])


def animate(i):
    collected_data = [2*rnd.random(),2*rnd.random(),2*rnd.random()]
    x = np.linspace(0, collected_data[0], 100)
    y = np.linspace(0, collected_data[1], 100)
    z = np.linspace(0, collected_data[2], 100)
    line.set_data_3d(x, y, z)

ax.set_zlim3d(-1, 1)
ax.set_ylim3d(-1, 1)
ax.set_xlim3d(-1, 1)
ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.tight_layout()
plt.show()