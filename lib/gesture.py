from measurement import Measurement
import numpy as np
import matplotlib.pyplot as plt
import json
import glob
import os
from scipy.optimize import minimize

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
                sum += np.dot(v, x)
            return sum

        def func_bound(x):
            return sum(x ** 2) - 1

        condition = {'type': 'eq', 'fun': func_bound}
        x0 = np.array([1, 1, 1])
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

        a = np.array([1, 1, (-n[0] - n[1])/n[2]])
        a /= np.dot(a, a)
        b = np.array([1, -1, (n[1]-n[0])/n[2]])
        b -= np.dot(b, a) * a
        b /= np.dot(b, b)

        C = np.array([a, b, n]).T # 3x3
        A = np.array(self.select_proj_3d(normal_vector)).T # 3xn
        res = np.dot(np.linalg.inv(C), A).T[:, 0:2]
        return res

    @classmethod
    def from_file(self, filename):
        script_dir = os.path.dirname(__file__)
        with open(script_dir + '/../data/' + filename) as json_file:
            data = json.load(json_file)
        return self(data[0])
