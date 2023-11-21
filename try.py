import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np

class ConvexHullAnimator:
    def __init__(self, points):
        self.points = points

    @staticmethod
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0 
        return 1 if val > 0 else 2

    def convex_hull_animation(self):
        n = len(self.points)
        if n < 3:
            return [self.points]

        hull_points_list = []

        l = min(range(n), key=lambda i: self.points[i][0])

        p = l
        q = 0
        while True:
            hull_points_list.append(self.points[p])

            q = (p + 1) % n
            for i in range(n):
                if self.orientation(self.points[p], self.points[i], self.points[q]) == 2:
                    q = i

            p = q

            if p == l:
                break

        return hull_points_list

    def create_animation(self):
        hull_points_list = self.convex_hull_animation()

        fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter'}]])

        scatter_trace = go.Scatter(x=self.points[:, 0], y=self.points[:, 1], mode='markers', name='Points', marker=dict(color='blue'))
        fig.add_trace(scatter_trace)

        frames = []

        for i in range(len(hull_points_list)):
            hull_points = np.array(hull_points_list[:i + 1])

            scatter_frame = go.Frame(
                data=[go.Scatter(x=self.points[:, 0], y=self.points[:, 1], mode='markers', name='Points'),
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

        return fig

# Example usage:
np.random.seed(42)
points = np.random.rand(20, 2)

animator = ConvexHullAnimator(points)
animation_fig = animator.create_animation()
animation_fig.show()
