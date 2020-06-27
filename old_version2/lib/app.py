from gesture import Gesture


# g = Gesture.from_file("круг.json")
# # print('g', g)
# print('gm', g.measurements)
# print('proj', g.select_proj_on_plane())
# print('res', g.select_proj_2d())

import matplotlib.pyplot as plt

g = Gesture.from_file("cirl_test.json")[0]
# g.draw_accel_3d()
# g.draw_accel_3d(with_surf=True)
# g.to_image()
g.predict()
# data = g.select_proj_2d()
# plt.scatter(data[:,0], data[:,1])
# plt.show()