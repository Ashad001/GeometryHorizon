import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .base import ConvexHull
import matplotlib.pyplot as plt

class QuickHull(ConvexHull):
    def __init__(self, points=None, max_x=100, max_y=100):
        super().__init__(points, max_x, max_y, len(points) if points is not None else None)
        self.hull = None
        self.hull_points = None

    def quickhull(self):
        def find_hull(p, q, points):
            if len(points) == 0:
                return []
            else:
                farthest_point = max(points, key=lambda point: distance(p, q, point))
                hull = find_hull(p, farthest_point, [point for point in points if orientation(p, farthest_point, point) == 1])
                hull.extend([farthest_point])
                hull.extend(find_hull(farthest_point, q, [point for point in points if orientation(farthest_point, q, point) == 1]))
                return hull

        def distance(p, q, r):
            return abs((q[1] - p[1]) * r[0] - (q[0] - p[0]) * r[1] + q[0] * p[1] - q[1] * p[0]) / np.sqrt((q[1] - p[1]) ** 2 + (q[0] - p[0]) ** 2)

        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else -1

        points = sorted(map(tuple, self.points), key=lambda x: x[0])  # Convert numpy arrays to tuples
        hull = find_hull(points[0], points[-1], points)
        hull.extend(find_hull(points[-1], points[0], points))
        self.hull = list(set(map(tuple, hull)))  # Convert back to list after removing duplicates
        return self.hull

    def plot(self, hull_points=None):
        if hull_points is None:
            hull_points = self.hull
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
            hull_points = np.array(hull_points_list[:i + 1])

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
                            mode="lines+markers",
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

    def visualize_quickhull(self):
        fig = self.plot_step_by_step()
        st.line_chart(fig)
    def __call__(self):
        self.quickhull()
        self.visualize_quickhull()
        return self.hull

if __name__ == "__main__":
    qh = QuickHull()
    print(qh())