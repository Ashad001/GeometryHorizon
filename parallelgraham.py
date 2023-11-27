import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from mpi4py import MPI
import math
import numpy as np
from plotly.subplots import make_subplots
from .base import ConvexHull

class ParallelGrahamScan(ConvexHull):
    def __init__(self, points=None, max_x=100, max_y=100):
        super().__init__(points, max_x, max_y, len(points) if points is not None else None)
        self.hull = None
        self.hull_points = None

    def parallel_graham_scan(self):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()

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

        # Distribute data among processors
        local_data = np.array_split(sorted_points, size)[rank]

        # Each processor computes local convex hull using Graham's Scan
        local_hull = [sorted_points[0], sorted_points[1]]
        for i in range(2, len(local_data)):
            while len(local_hull) > 1 and orientation(local_hull[-2], local_hull[-1], local_data[i]) != -1:
                local_hull.pop()
            local_hull.append(local_data[i])

        # Gather local hulls from all processors
        all_hulls = comm.gather(local_hull, root=0)

        # Master processor merges convex hulls
        if rank == 0:
            final_hull = self.merge_convex_hulls(all_hulls)

            # Print or further process the final convex hull computed by master processor
            print(f"Convex Hull: {final_hull}")

            # Visualize the convex hull
            self.hull = final_hull
            self.plot_step_by_step()

    def merge_convex_hulls(self, hulls):
        def find_tangent(hull_a, hull_b, upper=True):
            # Find the tangent point on hull_a from hull_b
            tangent_point = None

            for i in range(len(hull_a)):
                while True:
                    current_index_b = 0 if upper else len(hull_b) - 1
                    next_index_b = (current_index_b + 1) % len(hull_b)

                    if upper:
                        orientation = self.orientation(hull_a[i], hull_b[current_index_b], hull_b[next_index_b])
                    else:
                        orientation = self.orientation(hull_a[i], hull_b[next_index_b], hull_b[current_index_b])

                    if orientation == -1:
                        break
                    else:
                        current_index_b = next_index_b

                if upper and (tangent_point is None or hull_a[i][1] > tangent_point[1]):
                    tangent_point = hull_a[i]
                elif not upper and (tangent_point is None or hull_a[i][1] < tangent_point[1]):
                    tangent_point = hull_a[i]

            return tangent_point

        # Sort hulls based on their leftmost points
        sorted_hulls = sorted(hulls, key=lambda h: min(h, key=lambda p: p[0])[0])

        # Find the upper and lower tangent points
        upper_tangent = find_tangent(sorted_hulls[0], sorted_hulls[1], upper=True)
        lower_tangent = find_tangent(sorted_hulls[0], sorted_hulls[1], upper=False)

        # Merge the hulls using the upper and lower tangent points
        merged_hull = sorted_hulls[0]
        for hull in sorted_hulls[1:]:
            upper_index = hull.index(upper_tangent)
            lower_index = hull.index(lower_tangent)

            # Merge the convex hulls based on the upper and lower tangent points
            merged_hull = merged_hull[:upper_index] + hull[lower_index:] + hull[:lower_index] + merged_hull[upper_index:]

            # Update upper and lower tangent points for the next iteration
            upper_tangent = find_tangent(merged_hull, hull, upper=True)
            lower_tangent = find_tangent(merged_hull, hull, upper=False)

        return merged_hull

    def orientation(self, p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else -1

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

        st.plotly_chart(fig)

    def __call__(self):
        self.parallel_graham_scan()
        return self.hull

if __name__ == "__main__":
    gs = ParallelGrahamScan()
    print(gs())
