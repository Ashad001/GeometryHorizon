import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from base import ConvexHull


class BruteForce(ConvexHull):
    def __init__(self, points=None, max_x=100, max_y=100):
        super().__init__(points, max_x, max_y, len(points))
        self.hull = []
        self.hull_points = []
        self.frames = []

    def bruteForce(self):
        n = self.n
        points = self.points

        # Function to check if three points are collinear
        def are_collinear(p, q, r):
            return (q[1] - p[1]) * (r[0] - q[0]) == (q[0] - p[0]) * (r[1] - q[1])

        hull = []

        # Check all possible combinations of three points
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if not are_collinear(points[i], points[j], points[k]):
                        hull.append(points[i])
                        hull.append(points[j])
                        hull.append(points[k])
            self.frames.append(list(set(map(tuple, hull))))  # Convert to tuples and remove duplicates

        self.hull = hull
        self.hull_points = list(
            set(map(tuple, hull))
        )  # Convert to tuples and remove duplicates
        return self.hull_points

    def plot(self, hull_points=None):
        if hull_points is None:
            hull_points = self.hull_points

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=self.points[:, 0], y=self.points[:, 1], mode="markers", name="Points"
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[p[0] for p in hull_points],
                y=[p[1] for p in hull_points],
                mode="lines",
                name="Convex Hull",
                line=dict(color="green"),
            )
        )
        fig.show()

    def plot_step_by_step(self):
        fig = go.Figure()

        for frame in self.hull:
            fig.add_trace(
                go.Scatter(
                    x=self.points[:, 0],
                    y=self.points[:, 1],
                    mode="markers",
                    name="Points",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=[frame[0]],
                    y=[frame[1]],
                    mode="lines",
                     line=dict(color="red"),
                )
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
                                args=[
                                    None,
                                    dict(
                                        frame=dict(duration=1000, redraw=True),
                                        fromcurrent=True,
                                    ),
                                ],
                            )
                        ],
                    )
                ]
            )

        frames = [
            go.Frame(data=frame, name=f"Frame {i+1}")
            for i, frame in enumerate(fig.data[1::2])
        ]
        fig.frames = frames
        return fig

    def __call__(self):
        self.bruteForce()
        self.plot_step_by_step()
        return self.hull


if __name__ == "__main__":
    bf = BruteForce()
    print(bf())
