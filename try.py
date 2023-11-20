import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def orientation(p, q, r):
    ''' Return positive if p-q-r are clockwise, neg if counterclockwise, and 0 if collinear '''
    return (q[1] - p[1]) * (r[0] - p[0]) - (q[0] - p[0]) * (r[1] - p[1])

def convex_hull(points):
    ''' Graham scan for convex hull '''
    # Sorting the points based on their x-coordinate
    points = sorted(points, key=lambda point: (point[0], point[1]))
    hull = []

    for point in points:
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], point) <= 0:
            yield (hull, 'red')  # Edge is being removed (rejected)
            hull.pop()
        hull.append(tuple(point))  # Convert numpy array to tuple
        yield (hull, 'green')  # Edge is being added (accepted)

    # Lower hull
    for point in reversed(points):
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], point) <= 0:
            yield (hull, 'red')  # Edge is being removed (rejected)
            hull.pop()
        hull.append(tuple(point))  # Convert numpy array to tuple
        # yield (hull, 'green')  # Edge is being added (accepted)

    yield (hull, 'white')  # Final hull

# Generating random points
np.random.seed(4)
points = np.random.rand(20, 2)

# Visualization setup
fig, ax = plt.subplots()
fig.patch.set_facecolor('black')  # Set the background color of the figure
ax.set_facecolor('black')  # Set the background color of the axes
x, y = zip(*points)
sc = ax.scatter(x, y, color='white')  # Set point color to white for contrast
line, = ax.plot([], [], lw=2, color='white')  # Initial line color

# Update function for animation
def update(frame):
    hull, color = frame
    line.set_color(color)
    x, y = zip(*hull)
    line.set_data(x, y)
    return line,

# Creating animation
anim = FuncAnimation(fig, update, frames=convex_hull(points), blit=True, repeat=False)

plt.show()
