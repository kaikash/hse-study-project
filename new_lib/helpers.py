import numpy as np
import string
import random


def find_normal_vec(data):
    tmp_A = []
    for i in range(data.shape[0]):
        tmp_A.append([data[i, 0], data[i, 1], 1])

    b = np.matrix([data[:, 2]]).T
    A = np.matrix(tmp_A)
    fit = ((A.T * A).I * A.T * b).tolist()
    fit = np.array([fit[0][0], fit[1][0], fit[2][0]])
    fit /= np.sum(fit ** 2) ** 0.5
    return fit


def proj_of_v_on_plane(v, normal):
    proj_of_v_on_normal = (np.dot(np.array(v), np.array(normal)))*normal
    return v - proj_of_v_on_normal


def select_proj_2d(data, normal_vector=None):
    if normal_vector is None:
        normal_vector = find_normal_vec(data)
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
    A = np.array(data, copy=True) # 3xn
    res = np.dot(A, np.linalg.inv(C))[:, 0:2]
    return res


def select_proj_3d(data, normal_vector=None):
    if normal_vector is None:
        normal_vector = find_normal_vec(data)
    return np.array(list(
        map(lambda x: proj_of_v_on_plane(x, normal_vector), np.array(data, copy=True))))


def random_str(len=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(len))
