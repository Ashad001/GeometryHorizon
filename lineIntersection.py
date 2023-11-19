import matplotlib.pyplot as plt
import plotly.graph_objects as go

class LineIntersection:
    def __init__(self, line1, line2):
        self.line1 = line1
        self.line2 = line2
        self.intersect = None
        self.color = 'green'
        self.frames = []

    def are_lines_intersecting(self, line1, line2):
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2

        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else -1

        o1 = orientation((x1, y1), (x2, y2), (x3, y3))
        o2 = orientation((x1, y1), (x2, y2), (x4, y4))
        o3 = orientation((x3, y3), (x4, y4), (x1, y1))
        o4 = orientation((x3, y3), (x4, y4), (x2, y2))

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and self.on_segment((x1, y1), (x3, y3), (x2, y2)):
            return True

        if o2 == 0 and self.on_segment((x1, y1), (x4, y4), (x2, y2)):
            return True

        if o3 == 0 and self.on_segment((x3, y3), (x1, y1), (x4, y4)):
            return True

        if o4 == 0 and self.on_segment((x3, y3), (x2, y2), (x4, y4)):
            return True

        self.color = 'red'
        return False

    def on_segment(self, p, q, r):
        return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

    def check_intersection(self):
        self.intersect = self.are_lines_intersecting(self.line1, self.line2)
        return self.intersect

    def plot(self, color="red"):
        fig, ax = plt.subplots()
        ax.plot([self.line1[0], self.line1[2]], [self.line1[1], self.line1[3]], color=color)
        ax.plot([self.line2[0], self.line2[2]], [self.line2[1], self.line2[3]], color=color)
        plt.scatter([self.line1[0], self.line1[2]], [self.line1[1], self.line1[3]], color=color)
        plt.scatter([self.line2[0], self.line2[2]], [self.line2[1], self.line2[3]], color=color)
        plt.show()

    def plot_step_by_step(self):
        fig = go.Figure()
        frames = []

        for i in range(2):
            color = self.color

            frame_data = [
                go.Scatter(
                    x=[self.line1[0], self.line1[2]],
                    y=[self.line1[1], self.line1[3]],
                    mode="lines+markers",
                    line=dict(color=color),
                    showlegend=False,
                ),
                go.Scatter(
                    x=[self.line2[0], self.line2[2]],
                    y=[self.line2[1], self.line2[3]],
                    mode="lines+markers",
                    line=dict(color=color),
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
                                    frame=dict(duration=1000, redraw=True),
                                    fromcurrent=True,
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
                        dict(args=["frame", dict(value=len(frames) - 1)]),
                    ],
                    active=0,
                    pad=dict(t=0, l=0.1),
                )
            ],
        )
        return fig

    def __call__(self):
        self.check_intersection()
        self.plot_step_by_step()
        return self.intersect


# if __name__ == "__main__":
#     line1 = [1, 2, 0, 4]
#     line2 = [4, 2, 1, 4]

#     intersection_checker = LineIntersection(line1, line2)
#     print(intersection_checker())
