import threading
import random
import time
import numpy as np
import math
import matplotlib.pyplot as plt
import plotly.express as px

class ConvexHull:
    def __init__(self, points=None, max_x=100, max_y=100, n=10):
        self.points = points
        self.n = n
        if n is not None:
            self.generatePoints(n, x_range=(0, max_x), y_range=(0, max_y))   

        
    def generatePoints(self, n, x_range=(50, 100), y_range=(50, 100)):
        if n < 3:
            raise ValueError('n must be greater than 3')
        self.n = n        
        self.points = np.array([[random.randint(*x_range), random.randint(*y_range)] for _ in range(n)])
        return self.points
    
    def squareDistance(self, p, q):
        try: 
            x1, y1 = self.points[p]
            x2, y2 = self.points[q]
        except IndexError:
            raise IndexError('p and q must be less than the number of points')
        return (x2 - x1)**2 + (y2 - y1)**2
    
    def orientation(self, p, q, r, index=True) -> int:
        try: 
            if index:
                x1, y1 = self.points[p]
                x2, y2 = self.points[q]
                x3, y3 = self.points[r]
            else:
                x1, y1 = p
                x2, y2 = q
                x3, y3 = r
        except IndexError:
            raise IndexError('p, q and r must be less than the number of points')
        except Exception as e:
            raise e
        
        val = (y2 - y1) * (x3 - x2) - (x2 - x1) * (y3 - y2)
        return 0 if val == 0 else 1 if val > 0 else -1
    
    def findLeftMostPoint(self):
        idx = None
        x_min = 99999
        for ind, point in enumerate(self.points):
            px, py = point
            if px < x_min:
                x_min = px
                idx = ind
        return idx
    
    def algoState(self):
        self.algo = {
			'ind_leftMostPoint': None,
			'ind_p': None,
			'ind_q': None,
			'ind_r': None,
			'result_hull': [],
		}

    def polar_angle(p0, p1):
        x1, y1 = p0
        x2, y2 = p1
        y_span = y1 - y2
        x_span = x1 - x2
        return math.atan2(y_span, x_span)
            
    
        