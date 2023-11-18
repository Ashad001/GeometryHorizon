from base import ConvexHull
import matplotlib.pyplot as plt

class JarvisMarch(ConvexHull):
    def __init__(self, points=None, max_x=100, max_y=100, n=100):
        super().__init__(points, max_x, max_y, n)
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
        plt.ion()  
        fig, ax = plt.subplots()

        plt.scatter(self.points[:, 0], self.points[:, 1], label='Points')
        plt.title('Jarvis March - Convex Hull Construction')

        for i in range(len(self.hull)):
            current_point = self.points[self.hull[i]]
            next_point = self.points[self.hull[(i + 1) % len(self.hull)]]

            plt.plot([current_point[0], next_point[0]], [current_point[1], next_point[1]], 'r')
            plt.scatter(current_point[0], current_point[1], color='blue', marker='o', s=100, label='Hull Points')

            plt.pause(0.5) 

        plt.ioff()
        plt.show()
        
    def __call__(self):
        self.jarvisMarch()
        self.plot_step_by_step()
        return self.hull_points
    
if __name__=="__name__":
    jm = JarvisMarch()
    print(jm())