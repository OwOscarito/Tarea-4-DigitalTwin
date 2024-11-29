import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from receiver import start_receiving_fake

fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))

def get_arrow(theta):

    acc_data = start_receiving_fake()
    
    if acc_data:
        x, y,z = 0, 0, 0
        u = np.linspace(0, acc_data[0], 100)
        v = np.linspace(0, acc_data[1], 100)
        w = np.linspace(0, acc_data[2], 100)
        return x,y,z,u,v,w

quiver = ax.quiver(*get_arrow(0))
ax.set(xlim=[-1,1], ylim=[-1,1], zlim=[-1,1])

def update(theta):
    global quiver
    quiver.remove()
    quiver = ax.quiver(*get_arrow(theta))

ani = FuncAnimation(fig, update, interval=1000)

plt.show()