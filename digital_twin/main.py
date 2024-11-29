import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random as rnd

fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))

def get_arrow(theta):
    collected_data = [rnd.uniform(-1.0, 1.0), rnd.uniform(-1.0, 1.0), rnd.uniform(-1.0, 1.0)]
    x = 0
    y = 0
    z = 0
    u = collected_data[0]
    v = collected_data[1]
    w = collected_data[2]
    return x,y,z,u,v,w

quiver = ax.quiver(*get_arrow(0))

ax.set(xlim=[-1, 1], ylim=[-1, 1], zlim=[-1, 1])

def update(theta):
    global quiver
    quiver.remove()
    quiver = ax.quiver(*get_arrow(theta))

ani = FuncAnimation(fig, update, frames=np.linspace(0,2*np.pi,200), interval=1000)
plt.show()