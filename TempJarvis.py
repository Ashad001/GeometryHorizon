import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np

# Function to determine orientation of triplet (p, q, r)
def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

# Gift Wrapping (Jarvis March) algorithm to find convex hull
def convex_hull_animation(points):
    n = len(points)
    if n < 3:
        return points

    hull_points = []

    # Find the leftmost point
    l = min(range(n), key=lambda i: points[i][0])

    p = l
    q = 0
    while True:
        hull_points.append(points[p])

        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i

        p = q

        if p == l:
            break

    return [np.array(hull_points)]

# Create some sample data (random points in a 2D plane)
np.random.seed(42)
points = np.random.rand(20, 2)

# Create a subplot with two traces (scatter plot for points and convex hull)
fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter'}]])

# Create the initial scatter plot
scatter_trace = go.Scatter(x=points[:, 0], y=points[:, 1], mode='markers', name='Points')
fig.add_trace(scatter_trace)

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0 
    return 1 if val > 0 else 2

# Gift Wrapping (Jarvis March) algorithm to find convex hull
def convex_hull_animation(points):
    n = len(points)
    if n < 3:
        return [points]

    hull_points_list = []

    l = min(range(n), key=lambda i: points[i][0])

    p = l
    q = 0
    while True:
        hull_points_list.append(points[p])

        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i

        p = q

        if p == l:
            break

    return hull_points_list

np.random.seed(42)
points = np.random.rand(20, 2)

fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter'}]])

scatter_trace = go.Scatter(x=points[:, 0], y=points[:, 1], mode='markers', name='Points', marker=dict(color='blue'))
fig.add_trace(scatter_trace)

hull_points_list = convex_hull_animation(points)
frames = []

for i in range(len(hull_points_list)):
    hull_points = np.array(hull_points_list[:i + 1])

    scatter_frame = go.Frame(
        data=[go.Scatter(x=points[:, 0], y=points[:, 1], mode='markers', name='Points'),
              go.Scatter(x=hull_points[:, 0], y=hull_points[:, 1], mode='markers', name='Hull Points')],
        name=f'Frame {i}'
    )
    frames.append(scatter_frame)

    if len(hull_points) > 1:
        hull_x = np.append(hull_points[:, 0], hull_points[0, 0])
        hull_y = np.append(hull_points[:, 1], hull_points[0, 1])
        hull_frame = go.Frame(
            data=[go.Scatter(x=hull_x, y=hull_y, mode='lines', line=dict(color='red'), name='Convex Hull')],
            name=f'Frame {i}_hull'
        )
        frames.append(hull_frame)

fig.frames = frames

fig.update_layout(title='Convex Hull Animation', xaxis=dict(title='X-axis'), yaxis=dict(title='Y-axis'))

animation_settings = dict(frame=dict(duration=1500, redraw=True), fromcurrent=True)
fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play', method='animate', args=[None, animation_settings])])])

fig.show()

