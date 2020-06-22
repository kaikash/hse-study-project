import numpy as np


class Gesture:
    name = None
    data = None

    def __init__(self, gesture_data, name=None):
        self.name = name
        self.gesture_data = gesture_data

    def predict(self):
        pass

    def train(self):
        pass
