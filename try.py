import plotly.graph_objects as go
import time
import numpy as np

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # collinear
    return 1 if val > 0 else 2  # clock or counterclock wise

def convex_hull(points):
    n = len(points)
    if n < 3:
        return points

    hull = []

    # Find the leftmost point
    l = min(range(n), key=lambda x: points[x][0])

    # Start from the leftmost point, keep moving counterclockwise until
    # we reach the start point again
    p = l
    q = 0
    while True:
        hull.append(p)

        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i

        p = q

        # Break the loop when we reach the starting point
        if p == l:
            break

    return hull

# Generate some random points for demonstration
np.random.seed(42)
points = np.random.rand(10, 2)

# Get the convex hull vertices
hull_vertices = convex_hull(points)

# Create the plot
fig = go.Figure()

# Scatter plot for all points
fig.add_trace(go.Scatter(
    x=points[:, 0],
    y=points[:, 1],
    mode='markers',
    marker=dict(color='blue', size=10),
    name='Points'
))

# Scatter plot for convex hull points
fig.add_trace(go.Scatter(
    x=[points[i][0] for i in hull_vertices],
    y=[points[i][1] for i in hull_vertices],
    mode='markers',
    marker=dict(color='green', size=10),
    name='Convex Hull'
))

# Initialize animation frames
frames = []

for i in range(len(hull_vertices)):
    frame = go.Frame(
        data=[
            go.Scatter(
                x=points[:, 0],
                y=points[:, 1],
                mode='markers',
                marker=dict(color='blue', size=10),
                name='Points'
            ),
            go.Scatter(
                x=[points[hull_vertices[i]][0]],
                y=[points[hull_vertices[i]][1]],
                mode='lines+markers',
                marker=dict(color='red', size=10),
                name='Current Point'
            ),
            go.Scatter(
                x=[points[j][0] for j in hull_vertices[:i + 1]],
                y=[points[j][1] for j in hull_vertices[:i + 1]],
                mode='lines',
                marker=dict(color='green', size=10),
                name='Convex Hull'
            )
        ],
        traces=[0, 1, 2]
    )
    frames.append(frame)

# Update layout
fig.update_layout(
    updatemenus=[{
        'type': 'buttons',
        'showactive': False,
        'buttons': [{
            'label': 'Play',
            'method': 'animate',
            'args': [None, {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True}]
        }]
    }]
)

# Add frames to the layout
fig.frames = frames

# Show the plot
fig.show()
