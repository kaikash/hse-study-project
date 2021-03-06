from measurement import Measurement
import numpy as np
import matplotlib.pyplot as plt
import json
import glob
import os
from scipy.optimize import minimize
from new_predict import make_prediction
import plotly.graph_objects as go

class Gesture:
    def __init__(self, data):
        self.data = data
        self.measurements = list(map(lambda x: Measurement(x), data))
        self.accel_data = np.array(
            list(map(lambda x: x.acceleration, self.measurements))
        )

    def select_plane(self):
        def objective(x):
            sum = 0
            for v in self.accel_data:
                sum -= np.dot(v, x)
            return sum

        def func_bound(x):
            return sum(x ** 2) - 1

        condition = {'type': 'eq', 'fun': func_bound}
        x0 = np.array([1.0, 1.0, 1.0])
        b = (0.0, 1.0)
        bnds = (b, b, b)
        res = minimize(objective, x0, method='SLSQP', constraints=condition, bounds=bnds)
        return res.x

    def select_proj_3d(self, normal_vector=None):
        if normal_vector is None:
            normal_vector = self.select_plane()
        normal_vector = np.array(normal_vector)
        return list(map(lambda v:
            v - np.dot(v, normal_vector) * normal_vector,
            self.accel_data))

    def select_proj_2d(self, normal_vector=None):
        if normal_vector is None:
            normal_vector = self.select_plane()
        n = np.array(normal_vector)

        a = np.array([n[1], -n[0], 0])
        b = np.array([n[2], 0, -n[0]])
        c = np.array([0, n[2], -n[1]])
        if sum(a ** 2) == 0:
            a = c
        if sum(b ** 2) == 0:
            b = c
        b -= np.dot(b, a) / np.dot(a, a) * a
        a /= np.dot(a, a) ** 0.5
        b /= np.dot(b, b) ** 0.5

        C = np.array([a, b, n]) # 3x3
        A = np.array(self.select_proj_3d(normal_vector)) # 3xn
        res = np.dot(A, np.linalg.inv(C))[:, 0:2]
        # plt.scatter(x=res[:, 0], y=res[:,1])
        # plt.plot(res[:,0], res[:,1], linewidth=5)
        # plt.show()
        return res

    def to_image(self, directory=os.path.dirname(__file__), filename='img.jpg'):
        data = self.select_proj_2d()
        fig = plt.figure(frameon=False, figsize=[10, 10])
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        plt.plot(data[:,0], data[:,1], linewidth=5)
        plt.axis('equal')
        file_abs_path = directory + '/' + filename
        plt.savefig(file_abs_path)
        return file_abs_path

    def predict(self):
        f = self.to_image()
        return make_prediction(f)

    def draw_accel_3d(self, with_surf=False):
        size_of_cube = 15

        figs = [go.Scatter3d(
            x=self.accel_data[:, 0],
            y=self.accel_data[:, 1],
            z=self.accel_data[:, 2],
            opacity=0.5,
            name='accel data'
        )]

        if with_surf:
            n = self.select_plane()
            proj_data = np.array(self.select_proj_3d(n))
            # figs = []
            figs.append(go.Scatter3d(
                x=proj_data[:, 0],
                y=proj_data[:, 1],
                z=proj_data[:, 2],
                opacity=0.5,
                name='accel proj'
            ))
            figs.append(go.Scatter3d(
                x=[n[0]],
                y=[n[1]],
                z=[n[2]],
                opacity=1,
                name='normal vector'
            ))

        fig = go.Figure(data=figs)
        fig.update_layout(
            scene = dict(xaxis = dict(nticks=4, range=[-size_of_cube,size_of_cube],),
                        yaxis = dict(nticks=4, range=[-size_of_cube,size_of_cube],),
                        zaxis = dict(nticks=4, range=[-size_of_cube,size_of_cube],),),
            width=700,
            margin=dict(r=20, l=10, b=10, t=10))

        fig.show()

    @classmethod
    def from_abs_file(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
        return [*map(lambda x: self(x), data)]

    @classmethod
    def from_file(self, filename):
        script_dir = os.path.dirname(__file__)
        return self.from_abs_file(script_dir + '/../data/' + filename)
