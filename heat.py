import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Set the colormap
plt.rcParams['image.cmap'] = 'jet' 

def evolve(u, u_previous, a, dt, dx2, dy2):
    """Explicit time evolution.
       u:            new temperature field
       u_previous:   previous field
       a:            diffusion constant
       dt:           time step. """

    n, m = u.shape

    for i in range(1, n-1):
        for j in range(1, m-1):
            nu = ((u_previous[i-1, j] - 2*u_previous[i, j] + u_previous[i+1, j]) / dx2 + \
            (u_previous[i, j-1] - 2*u_previous[i, j] + u_previous[i, j+1]) / dy2 )
            u[i, j] = u_previous[i, j] + a * dt * nu

    u_previous[:] = u[:]

def iterate(field, field0, a, dx, dy, timesteps):
    """Run fixed number of time steps of heat equation"""

    dx2 = dx**2
    dy2 = dy**2

    # For stability, this is the largest interval possible
    # for the size of the time-step:
    dt = dx2*dy2 / ( 2*a*(dx2+dy2) )    

    for _ in range(1, timesteps+1):
        evolve(field, field0, a, dt, dx2, dy2)


def init_fields(filename):
    # Read the initial temperature field from file
    field = np.loadtxt(filename)
    field0 = field.copy() # Array for field of previous time step
    return field, field0

def write_field(file, field, step):
    plt.gca().clear()
    plt.imshow(field)
    plt.axis('off')
    f, l = file.rfind('/')+1, file.rfind('.')
    plt.savefig(f"./outputs/{file[f:l]}_heat_{step}.png")


