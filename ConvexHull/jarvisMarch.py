from .base import ConvexHull
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np


class JarvisMarch(ConvexHull):
    def __init__(self, points=None, max_x=100, max_y=100):
        super().__init__(points, max_x, max_y, len(points))
        self.hull = None
        self.hull_points = None

    @staticmethod
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def jarvisMarch(self):
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
                if (
                    self.orientation(self.points[p], self.points[i], self.points[q])
                    == 2
                ):
                    q = i
            p = q

            if p == l:
                break

        return hull_points_list

    def create_animation(self):
        hull_points_list = self.jarvisMarch()

        fig = make_subplots(rows=1, cols=1, specs=[[{"type": "scatter"}]])

        scatter_trace = go.Scatter(
            x=self.points[:, 0],
            y=self.points[:, 1],
            mode="markers",
            name="Points",
            marker=dict(color="blue"),
        )
        fig.add_trace(scatter_trace)

        frames = []

        for i in range(len(hull_points_list)):
            hull_points = np.array(hull_points_list[: i + 1])

            scatter_frame = go.Frame(
                data=[
                    go.Scatter(
                        x=self.points[:, 0],
                        y=self.points[:, 1],
                        mode="markers",
                        name="Points",
                    ),
                    go.Scatter(
                        x=hull_points[:, 0],
                        y=hull_points[:, 1],
                        mode="markers",
                        name="Hull Points",
                    ),
                ],
                name=f"Frame {i}",
            )
            frames.append(scatter_frame)

            if len(hull_points) > 1:
                hull_x = np.append(hull_points[:, 0], hull_points[0, 0])
                hull_y = np.append(hull_points[:, 1], hull_points[0, 1])
                hull_frame = go.Frame(
                    data=[
                        go.Scatter(
                            x=hull_x,
                            y=hull_y,
                            mode="lines",
                            line=dict(color="green"),
                            name="Convex Hull",
                        ),
                    ],
                    name=f"Frame {i}_hull",
                )
                frames.append(hull_frame)

        fig.frames = frames

        fig.update_layout(
            title="Convex Hull Animation",
            xaxis=dict(title="X-axis"),
            yaxis=dict(title="Y-axis"),
        )

        animation_settings = dict(
            frame=dict(duration=1000, redraw=True), fromcurrent=True
        )
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[None, animation_settings],
                        )
                    ],
                )
            ]
        )

        return fig

    def __call__(self):
        self.jarvisMarch()
        animation_fig = self.create_animation()
        return self.hull_points


# if __name__ == "__name__":
#     jm = JarvisMarch()
#     print(jm())


# from base import ConvexHull
# import matplotlib.pyplot as plt
# import numpy as np
# import operator
# from random import randint
# import plotly.graph_objects as go
# import math

# class GrhamScan(ConvexHull):
#     def __init__(self, points=None, max_x=100, max_y=100, n=10) -> None:
#         super().__init__(points, max_x, max_y, n)
#         self.hull = None
#         self.hull_points = None

#     def sortAngles(self, a, anchor):
#         if len(a) <= 1:
#             return a
#         smaller, equal, larger = [], [], []
#         piv_ang = self.polar_angle(a[randint(0, len(a) - 1)])
#         for pt in a:
#             pt_ang = self.polar_angle(pt, anchor)
#             if pt_ang < piv_ang:
#                 smaller.append(pt)
#             elif pt_ang == piv_ang:
#                 equal.append(pt)
#             else:
#                 larger.append(pt)
#         return self.sortAngles(smaller, anchor) + sorted(equal, key=self.distance) + self.sortAngles(larger, anchor)

#     def GrhamScan(self):
#         points = self.points
#         n = self.n
#         if n < 3:
#             raise ValueError('n must be greater than 3')
#         if n == 3:
#             return points

#         anchor = points[self.findLeftMostPoint()]
#         sorted_points = self.sortAngles(points, anchor)
#         del sorted_points[sorted_points.index(anchor)]
#         hull = [anchor, sorted_points[0]]
#         for s in sorted_points[1:]:
#             while self.det(hull[-2], hull[-1], s) <= 0:
#                 del hull[-1]
#             hull.append(s)
#         self.hull = hull
#         return hull

#     def plot(self, hull_points=None):
#         if hull_points is None:
#             hull_points = self.hull_points
#         plt.scatter(self.points[:, 0], self.points[:, 1])
#         plt.plot(hull_points[:, 0], hull_points[:, 1], 'r')
#         plt.show()

#     def plot_step_by_step(self):
#             fig = go.Figure()
#             frames = []

#             for i in range(len(self.hull)):
#                 current_point = self.points[self.hull[i]]
#                 next_point = self.points[self.hull[(i + 1) % len(self.hull)]]

#                 frame_data = [
#                     go.Scatter(
#                         x=self.points[:, 0],
#                         y=self.points[:, 1],
#                         mode="markers",
#                         marker=dict(color="blue", size=10),
#                         showlegend=False,
#                     ),
#                     go.Scatter(
#                         x=[current_point[0], next_point[0]],
#                         y=[current_point[1], next_point[1]],
#                         mode="lines",
#                         line=dict(color="green"),
#                         showlegend=False,
#                     ),
#                 ]

#                 fig.add_trace(frame_data[0])
#                 fig.add_trace(frame_data[1])

#                 frames.append(go.Frame(data=frame_data, name=f"Frame {i + 1}"))

#             fig.frames = frames

#             fig.update_layout(
#                 updatemenus=[
#                     dict(
#                         type="buttons",
#                         showactive=False,
#                         buttons=[
#                             dict(
#                                 label="Play",
#                                 method="animate",
#                                 args=[
#                                     None,
#                                     dict(
#                                         frame=dict(duration=500, redraw=True),
#                                         fromcurrent=False,
#                                     ),
#                                 ],
#                             )
#                         ],
#                     )
#                 ],
#                 sliders=[
#                     dict(
#                         steps=[
#                             dict(args=["frame", dict(value=0)]),
#                             dict(args=["frame", dict(value=len(self.hull) - 1)]),
#                         ],
#                         active=0,
#                         pad=dict(t=0, l=0.1),
#                     )
#                 ],
#             )

#             return fig

#     def __call__(self):
#         self.hull_points = self.GrhamScan()
#         print(self.hull)
#         self.plot_step_by_step()
#         return self.hull_points
