from gesture import Gesture


g = Gesture.from_file("gestures_1581174980043.json")
# print('g', g)
# print('gm', g.measurements)
print('proj', g.select_proj_on_plane())
