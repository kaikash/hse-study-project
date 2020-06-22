from server import Server, ServerError
from classes.gesture import Gesture
from classes.gesture_data import GestureData
from helpers import find_normal_vec, select_proj_3d, select_proj_2d
from parser import parse

import plotly.graph_objects as go
import numpy as np


def parse_json_data():
    # parse('data/json/squares.json', 'data/imgs/squares')
    # parse('data/json/squares_2.json', 'data/imgs/squares')
    # parse('data/json/squares_4.json', 'data/imgs/squares')
    # parse('data/json/squares_3.json', 'data/imgs/squares')
    # parse('data/json/squares_father.json', 'data/imgs/squares')
    # parse('data/json/squares_mother.json', 'data/imgs/squares')
    # parse('data/json/squares_sister.json', 'data/imgs/squares')

    # parse('data/json/circles.json', 'data/imgs/circles')
    # parse('data/json/circles_2.json', 'data/imgs/circles')
    # parse('data/json/circles_3.json', 'data/imgs/circles')
    # parse('data/json/circles_father.json', 'data/imgs/circles')
    # parse('data/json/circles_mother.json', 'data/imgs/circles')
    # parse('data/json/circles_sister.json', 'data/imgs/circles')

    # parse('data/json/shakes.json', 'data/imgs/shakes')
    # parse('data/json/shakes_2.json', 'data/imgs/shakes')
    # parse('data/json/shakes_3.json', 'data/imgs/shakes')
    # parse('data/json/shakes_father.json', 'data/imgs/shakes')
    # parse('data/json/shakes_mother.json', 'data/imgs/shakes')

    # parse('data/json/triangles.json', 'data/imgs/triangles')
    pass


parse_json_data()

server = Server(__name__, port=3000)

def train(request):
    data = request.get_json()

    gd = GestureData(data['gesture_data'])
    if 'gnorm' in data:
        gd.normalize_gyro()

    if 'norm' in data:
        gd.normalize()

    if 'fil' in data:
        gd.filter()

    if 'avg' in data:
        gd.find_average()

    # gd.pos_to_image()
    gd.draw_pos()

    return {
        'method': 'train'
    }


def predict(request):
    return {
        'method': 'predict'
    }

server.add_endpoint('/train', 'train', handler=train, methods=['POST'])
server.add_endpoint('/predict', 'predict', handler=predict, methods=['POST'])

if __name__ == '__main__':
    server.run()
