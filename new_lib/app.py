from server import Server, ServerError
from classes.classifier import Classifier
from classes.gesture import Gesture
from classes.gesture_data import GestureData
from helpers import find_normal_vec, select_proj_3d, select_proj_2d, random_str
from parser import parse

import plotly.graph_objects as go
import numpy as np



def parse_json_data():
    # parse('data/json/squares.json', 'data/imgs/square')
    # parse('data/json/squares_2.json', 'data/imgs/square')
    # parse('data/json/squares_4.json', 'data/imgs/square')
    # parse('data/json/squares_3.json', 'data/imgs/square')
    # parse('data/json/squares_father.json', 'data/imgs/square')
    # parse('data/json/squares_mother.json', 'data/imgs/square')
    # parse('data/json/squares_sister.json', 'data/imgs/square')

    # parse('data/json/circles.json', 'data/imgs/circle')
    # parse('data/json/circles_2.json', 'data/imgs/circle')
    # parse('data/json/circles_3.json', 'data/imgs/circle')
    # parse('data/json/circles_father.json', 'data/imgs/circle')
    # parse('data/json/circles_mother.json', 'data/imgs/circle')
    # parse('data/json/circles_sister.json', 'data/imgs/circle')

    # parse('data/json/shakes.json', 'data/imgs/shake')
    # parse('data/json/shakes_2.json', 'data/imgs/shake')
    # parse('data/json/shakes_3.json', 'data/imgs/shake')
    # parse('data/json/shakes_father.json', 'data/imgs/shakse')
    # parse('data/json/shakes_mother.json', 'data/imgs/shake')

    # parse('data/json/triangles.json', 'data/imgs/triangle')
    pass


parse_json_data()

classifier = Classifier()
server = Server(__name__, port=3000)

def fetch_gesture(data):
    if 'gesture_data' not in data:
        raise ServerError('No gesture data provided', 400)

    gd = GestureData(data['gesture_data'])
    if 'gnorm' in data:
        gd.normalize_gyro()
    if 'norm' in data:
        gd.normalize()
    if 'fil' in data:
        gd.filter()
    if 'avg' in data:
        gd.find_average()
    return gd


def train(request):
    data = request.get_json()
    gd = fetch_gesture(data)

    if 'name' not in data:
        raise ServerError('No class provided', 400)

    if data['name'] not in Classifier.classes:
        raise ServerError('Invalid class', 400)

    image_path = gd.pos_to_image(dir='data/imgs/'+data['name'], filename='img_'+random_str())
    gesture = Gesture(gd, image_path)

    return {
        'success': True,
        'gesture': gesture.to_dict()
    }


def retrain(request):
    if classifier.retraining:
        raise ServerError('Model is retraining', 400)

    classifier.retrain()
    return {
        'success': True
    }


def predict(request):
    data = request.get_json()

    gd = fetch_gesture(data)

    image_path = gd.pos_to_image(dir='data/tmp', filename='img_'+random_str())
    prediction = classifier.predict(image_path)
    idx = np.unravel_index(
        np.argmax(prediction, axis=None), prediction.shape)
    gesture = Gesture(gd, Classifier.classes[idx[1]], image_path)

    return {
        'success': True,
        'prediction': [*zip(map(float, prediction.tolist()[0]), Classifier.classes)],
        'gesture': gesture.to_dict()
    }


server.add_endpoint('/train', 'train', handler=train, methods=['POST'])
server.add_endpoint('/predict', 'predict', handler=predict, methods=['POST'])
server.add_endpoint('/retrain', 'retrain', handler=retrain, methods=['POST'])


if __name__ == '__main__':
    server.run()
