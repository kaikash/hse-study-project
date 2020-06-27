from gesture import Gesture

import matplotlib.pyplot as plt
import os
import sys


if len(sys.argv) < 2:
    sys.exit("no gesture")
filename = sys.argv[1]
out_dir = '../data/' + filename + '_out'
os.mkdir(out_dir)
for ind, g in enumerate(Gesture.from_file(filename)):
    data = g.select_proj_2d()
    fig = plt.figure(frameon=False, figsize=[10, 10])
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    plt.plot(data[:, 0], data[:, 1], linewidth=5)
    plt.axis('equal')
    plt.savefig(out_dir + '/' + str(ind) + '.jpg')
