from base import ConvexHull
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

class JarvisMarch(ConvexHull):
    def __init__(self, points=None, max_x=100, max_y=100):
        super().__init__(points, max_x, max_y, len(points))
        self.hull = None
        self.hull_points = None
        
    def jarvisMarch(self):
        n = self.n
        points = self.points
        if n < 3:
            raise ValueError('n must be greater than 3')
        if n == 3:
            return points
        
        hull = []
        notHull = []
        l = 0
        for i in range(1, n):
            if points[i][0] < points[l][0]:
                l = i
        
        p = l
        q = None
        while True:
            hull.append(p)
            q = (p + 1) % n
            for i in range(n):
                if self.orientation(p, i, q) == -1:
                    q = i
            p = q
            if p == l:
                break
        hull.append(l)
        self.hull = hull
        self.hull_points = points[hull]
        return self.hull_points
    
    def plot(self, hull_points=None):
        if hull_points is None:
            hull_points = self.hull_points
        plt.scatter(self.points[:, 0], self.points[:, 1])
        plt.plot(hull_points[:, 0], hull_points[:, 1], 'r')
        plt.show()
        
    def plot_step_by_step(self):
        fig = go.Figure()
        frames = []

        for i in range(len(self.hull)):
            current_point = self.points[self.hull[i]]
            next_point = self.points[self.hull[(i + 1) % len(self.hull)]]

            frame_data = [
                go.Scatter(x=self.points[:, 0], y=self.points[:, 1], mode='markers', marker=dict(color='blue', size=10),
                        showlegend=False),
                go.Scatter(x=[current_point[0], next_point[0]], y=[current_point[1], next_point[1]],
                        mode='lines', line=dict(color='red'), showlegend=False)
            ]

            fig.add_trace(frame_data[0])
            fig.add_trace(frame_data[1])

            frames.append(go.Frame(data=frame_data, name=f"Frame {i + 1}"))

        fig.frames = frames

        fig.update_layout(updatemenus=[dict(type='buttons', showactive=False,
                                            buttons=[dict(label='Play',
                                                        method='animate',
                                                        args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)])])],
                        sliders=[dict(steps=[dict(args=['frame', dict(value=0)]),
                                            dict(args=['frame', dict(value=len(self.hull) - 1)])],
                                    active=0, pad=dict(t=0, l=0.1))])

        return fig

        
    def __call__(self):
        self.jarvisMarch()
        self.plot_step_by_step()
        return self.hull_points
    
if __name__=="__name__":
    jm = JarvisMarch()
    print(jm())