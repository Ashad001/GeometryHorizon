import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots


class Point:
    def __init__(self, x=0, y=0):
        self.X = x
        self.Y = y

    def __lt__(self, q):
        return self.X < q.X or (self.X == q.X and self.Y < q.Y)

    def __ne__(self, q):
        return self.X != q.X or self.Y != q.Y

    def is_turning_right(self, q, r):
        check = (self.X * q.Y + q.X * r.Y + r.X * self.Y) - (self.Y * q.X + q.Y * r.X + r.Y * self.X)
        return check < 0

    def is_collinear(self, q, r):
        check = (self.X * q.Y + q.X * r.Y + r.X * self.Y) - (self.Y * q.X + q.Y * r.X + r.Y * self.X)
        return check == 0

    def is_on_segment(self, q, r):
        x1, x2 = r.X - self.X, q.X - self.X
        y1, y2 = r.Y - self.Y, q.Y - self.Y
        det = x1 * y2 - x2 * y1
        return det == 0 and x1 * x2 <= 0 and y1 * y2 <= 0

np.random.seed(42)
points = np.random.rand(20, 2)

points = [Point(x, y) for x, y in points]

convex_hull = []
next_point = {}
side = {}

for i in range(len(points)):
    for j in range(len(points)):
        if i != j:
            point_on_segment = False
            right_turn_count = 0
            collinear_count = 0
            for k in range(len(points)):
                if k != i and k != j:
                    if points[i].is_turning_right(points[j], points[k]):
                        right_turn_count += 1
                    if points[i].is_collinear(points[j], points[k]):
                        collinear_count += 1
                        if points[k].is_on_segment(points[i], points[j]):
                            point_on_segment = True

            if right_turn_count + collinear_count == len(points) - 2:
                if not (point_on_segment and side.get((j, i), False)):
                    convex_hull.append((points[i], points[j]))
                    next_point[points[i]] = points[j]
                    side[(i, j)] = True

def output_points():
    print(f"There are {len(convex_hull)} points forming the convex hull.")
    print("The points forming the convex hull in clockwise order are:")
    P0 = P = convex_hull[0][0]
    current = 0
    while current < len(convex_hull):
        print(P.X, P.Y)
        P = next_point[P]
        current += 1
    if P != P0:
        print(P.X, P.Y)

def create_animation(convex_hull, next_point):
    fig = make_subplots(rows=1, cols=1)

    frames = []
    for k in range(len(convex_hull) + 1):
        frame_points = []
        P = P0 = convex_hull[0][0]
        current = 0

        while current < k:
            frame_points.append((P.X, P.Y))
            P = next_point[P]
            current += 1

        if P != P0:
            frame_points.append((P.X, P.Y))

        frame_hull = [(P0.X, P0.Y)] + frame_points + [(P0.X, P0.Y)]

        trace = go.Scatter(
            x=[point[0] for point in frame_hull],
            y=[point[1] for point in frame_hull],
            mode='lines+markers',
            name=f'Frame {k}',
        )

        frames.append(go.Frame(data=[trace], name=f'Frame {k}'))

    fig.add_trace(frames[0]['data'][0])
    fig.frames = frames

    fig.update_layout(updatemenus=[{
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 1500, 'redraw': True}, 'fromcurrent': True}],
                'label': 'Play',
                'method': 'animate',
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate',
            },
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top',
    }])

    fig.update_layout(title='Brute Force Animation', showlegend=False)

    return fig


animation_fig = create_animation(convex_hull, next_point)

animation_fig.show()