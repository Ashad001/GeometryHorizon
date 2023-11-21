import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

import math
import numpy as np

from plotly.subplots import make_subplots
from .base import ConvexHull  

class GrahamScan(ConvexHull):
    def __init__(self, points=None, max_x=100, max_y=100):
        super().__init__(points, max_x, max_y, len(points) if points is not None else None)
        self.hull = None
        self.hull_points = None

    def grahamScan(self):
        n = self.n
        points = self.points
        if n < 3:
            raise ValueError("n must be greater than 2")

        start_point = min(points, key=lambda p: (p[1], p[0]))

        def polar_angle(p):
            x, y = p[0] - start_point[0], p[1] - start_point[1]
            return math.atan2(y, x)

        sorted_points = sorted(points, key=polar_angle)

        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else -1

        hull = [sorted_points[0], sorted_points[1]]
        for i in range(2, n):
            while len(hull) > 1 and orientation(hull[-2], hull[-1], sorted_points[i]) != -1:
                hull.pop()
            hull.append(sorted_points[i])

        self.hull = hull
        return hull


    def plot(self, hull_points=None):
        if hull_points is None:
            hull_points = self.hull_points
        plt.scatter(self.points[:, 0], self.points[:, 1])
        plt.plot([p[0] for p in hull_points], [p[1] for p in hull_points], "r")
        plt.show()

    def plot_step_by_step(self):
        hull_points_list = self.hull
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
                            mode="lines+markers+text",
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
        self.grahamScan()
        self.plot_step_by_step()
        return self.hull


if __name__ == "__main__":
    gs = GrahamScan()
    print(gs())