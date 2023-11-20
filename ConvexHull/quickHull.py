import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from .base import ConvexHull  

class QuickHull(ConvexHull):
    def __init__(self, points=None, max_x=100, max_y=100):
        super().__init__(points, max_x, max_y, len(points)if points is not None else None)
        self.hull = []
        self.hull_points = []
        
    def quickHull(self):
        n = self.n
        points = self.points

        def distance(p, q, r):
            return ((q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]))

        def find_side(p1, p2, points):
            # Find points on the left side of the line formed by p1 and p2
            return [point for point in points if distance(p1, p2, point) > 0]

        def quick_hull_util(p1, p2, points, hull):
            if not points:
                return

            max_dist = -1
            farthest_point = None

            for point in points:
                dist = distance(p1, p2, point)
                if dist > max_dist:
                    max_dist = dist
                    farthest_point = point

            hull.append(farthest_point)

            points_left = find_side(p1, farthest_point, points)
            points_right = find_side(farthest_point, p2, points)

            quick_hull_util(p1, farthest_point, points_left, hull)
            quick_hull_util(farthest_point, p2, points_right, hull)

        if n < 3:
            raise ValueError("n must be greater than 2")

        min_point = min(points, key=lambda x: x[0])
        max_point = max(points, key=lambda x: x[0])

        hull = [min_point, max_point]

        points_left = find_side(min_point, max_point, points)
        points_right = find_side(max_point, min_point, points)

        quick_hull_util(min_point, max_point, points_left, hull)
        quick_hull_util(max_point, min_point, points_right, hull)

        self.hull = hull
        self.hull_points = hull
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
        self.quickHull()
        self.plot_step_by_step()
        return self.hull


if __name__ == "__main__":
    qh = QuickHull()
    print(qh())
