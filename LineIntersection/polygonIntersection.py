import plotly.graph_objects as go
from shapely.geometry import LineString, Polygon

class PolygonIntersection:
    def __init__(self, polygon_coords):
        self.polygon = Polygon(polygon_coords)
        self.line = None
        self.intersect = None
        self.color = 'green'

    def set_line(self, line_coords):
        self.line = LineString(line_coords)

    def check_intersection(self):
        if self.line is not None:
            self.intersect = self.polygon.intersects(self.line)
            return self.intersect
        else:
            raise ValueError("Line not set. Use set_line method to set the line.")

    def plot(self):
        fig = go.Figure()

        # Plot polygon
        polygon_x, polygon_y = self.polygon.exterior.xy
        fig.add_trace(go.Scatter(x=list(polygon_x), y=list(polygon_y), mode='lines', fill='toself', fillcolor='rgba(0,100,80,0.2)', line=dict(color='blue'), name='Polygon'))

        # Plot line
        line_x, line_y = self.line.xy
        fig.add_trace(go.Scatter(x=list(line_x), y=list(line_y), mode='lines', line=dict(color=self.color), name='Line'))

        # Highlight intersection point if exists
        if self.intersect:
            intersection_point = self.polygon.intersection(self.line)
            if intersection_point.geom_type == 'Point':
                fig.add_trace(go.Scatter(x=[intersection_point.x], y=[intersection_point.y], mode='markers', marker=dict(color='red'), name='Intersection Point'))

        fig.update_layout(title='Polygon and Line Intersection', showlegend=True)
        fig.show()

# Example Usage:
polygon_coords = [(1, 1), (3, 1), (3, 3), (1, 3), (0, 2)]
line_coords = [(0, 2), (4, 2)]

poly_intersection = PolygonIntersection(polygon_coords)
poly_intersection.set_line(line_coords)
poly_intersection.check_intersection()
poly_intersection.plot()
