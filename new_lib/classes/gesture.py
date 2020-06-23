import numpy as np


class Gesture:
    def __init__(self, gesture_data, image_path, name=None):
        self.gesture_data = gesture_data
        self.image_path = image_path
        self.name = name


    def to_dict(self):
        return {
            'name': self.name,
            'image': self.image_path,
            'gesture_data': self.gesture_data.to_dict()
        }

