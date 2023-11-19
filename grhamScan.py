import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from base import ConvexHull  # Make sure to import ConvexHull from the correct module

class GrahamScan(ConvexHull):
    def __init__(self, points=None, max_x=100, max_y=100):
        super().__init__(points, max_x, max_y, len(points) if points is not None else None)
        self.hull = None
        self.hull_points = None

    def grahamScan(self):
        n = self.n
        points = self.points
        if n < 3:
            raise ValueError("n must be greater than 3")

        # Function to find the polar angle with respect to the reference point
        def polar_angle(p):
            return (p[1] - points[0][1]) / ((p[0] - points[0][0]) + 1e-9)

        # Sort the points based on polar angle
        sorted_points = sorted(points, key=polar_angle)
        
        # Function to calculate the orientation of three points
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
        self.hull_points = sorted_points
        return hull

    def plot(self, hull_points=None):
        if hull_points is None:
            hull_points = self.hull_points
        plt.scatter(self.points[:, 0], self.points[:, 1])
        plt.plot([p[0] for p in hull_points], [p[1] for p in hull_points], "r")
        plt.show()

    def plot_step_by_step(self):
        fig = go.Figure()
        frames = []

        for i in range(len(self.hull)):
            current_point = self.hull[i]
            next_point = self.hull[(i + 1) % len(self.hull)]

            frame_data = [
                go.Scatter(
                    x=[p[0] for p in self.points],
                    y=[p[1] for p in self.points],
                    mode="markers",
                    marker=dict(color="blue", size=10),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[current_point[0], next_point[0]],
                    y=[current_point[1], next_point[1]],
                    mode="lines",
                    line=dict(color="green"),
                    showlegend=False,
                ),
            ]

            fig.add_trace(frame_data[0])
            fig.add_trace(frame_data[1])

            frames.append(go.Frame(data=frame_data, name=f"Frame {i + 1}"))

        fig.frames = frames

        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(
                            label="Play",
                            method="animate",
                            args=[
                                None,
                                dict(
                                    frame=dict(duration=500, redraw=True),
                                    fromcurrent=False,
                                ),
                            ],
                        )
                    ],
                )
            ],
            sliders=[
                dict(
                    steps=[
                        dict(args=["frame", dict(value=0)]),
                        dict(args=["frame", dict(value=len(self.hull) - 1)]),
                    ],
                    active=0,
                    pad=dict(t=0, l=0.1),
                )
            ],
        )

        return fig

    def __call__(self):
        self.grahamScan()
        self.plot_step_by_step()
        return self.hull


if __name__ == "__main__":
    gs = GrahamScan()
    print(gs())
