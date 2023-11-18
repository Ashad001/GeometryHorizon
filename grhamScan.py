from base import ConvexHull
import matplotlib.pyplot as plt
import numpy as np
import operator
from random import randint
import math
class GrhamScan(ConvexHull):
    def __init__(self, points=None, max_x=100, max_y=100, n=10) -> None:
        super().__init__(points, max_x, max_y, n)
        self.hull = None
        self.hull_points = None
        
    def sortAngles(self, a, anchor):
        if len(a) <= 1:
            return a
        smaller, equal, larger = [], [], []
        piv_ang = self.polar_angle(a[randint(0, len(a) - 1)])
        for pt in a:
            pt_ang = self.polar_angle(pt, anchor)
            if pt_ang < piv_ang:
                smaller.append(pt)
            elif pt_ang == piv_ang:
                equal.append(pt)
            else:
                larger.append(pt)
        return self.sortAngles(smaller, anchor) + sorted(equal, key=self.distance) + self.sortAngles(larger, anchor)
        
    def GrhamScan(self):
        points = self.points
        n = self.n
        if n < 3:
            raise ValueError('n must be greater than 3')
        if n == 3:
            return points
        
        anchor = points[self.findLeftMostPoint()]    
        sorted_points = self.sortAngles(points, anchor)
        del sorted_points[sorted_points.index(anchor)]
        hull = [anchor, sorted_points[0]]
        for s in sorted_points[1:]:
            while self.det(hull[-2], hull[-1], s) <= 0:
                del hull[-1]
            hull.append(s)
        self.hull = hull
        return hull
           
    def plot(self, hull_points=None):
        if hull_points is None:
            hull_points = self.hull_points
        plt.scatter(self.points[:, 0], self.points[:, 1])
        plt.plot(hull_points[:, 0], hull_points[:, 1], 'r')
        plt.show()
        
    def plot_step_by_step(self):
        plt.ion()  
        fig, ax = plt.subplots()

        plt.scatter(self.points[:, 0], self.points[:, 1], label='Points')
        plt.title('Graham Scan - Convex Hull Construction')

        for i in range(len(self.hull)):
            current_point = self.points[self.hull[i]]
            next_point = self.points[self.hull[(i + 1) % len(self.hull)]]

            plt.plot([current_point[0], next_point[0]], [current_point[1], next_point[1]], 'r')
            plt.scatter(current_point[0], current_point[1], color='blue', marker='o', s=100, label='Hull Points')

        plt.show()
        plt.pause(0.5)
        plt.close()
        
    def __call__(self):
        self.hull_points = self.GrhamScan()
        print(self.hull)
        self.plot_step_by_step()
        return self.hull_points
    