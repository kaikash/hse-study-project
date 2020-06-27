import json
from classes.gesture_data import GestureData
from helpers import random_str


def parse(filename, outputdir='data/imgs'):
    with open(filename) as json_file:
        data = json.load(json_file)
        cur = 1
        prefix = random_str()
        for gdata in data:
            if len(gdata) < 20:
                continue

            gd = GestureData(gdata)
            gd.normalize()
            gd.filter()
            gd.find_average()
            gd.pos_to_image(dir=outputdir, filename='img_' + prefix + '_' + str(cur))
            cur += 1
