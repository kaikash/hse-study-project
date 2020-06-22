import sys
sys.path.append('..')

import numpy as np
import plotly.graph_objects as go
import math
import scipy.signal
import matplotlib.pyplot as plt
from helpers import find_normal_vec, select_proj_3d, select_proj_2d
from math import cos, sin

plt.switch_backend('agg')

class GestureData:
    name = None
    data = None

    def __init__(self, data, name=None):
        self.name = name
        self.time = np.array(
            list(map(lambda x: x[0] / 1000, data)))
        self.accel = np.array(
            list(map(lambda x: x[1:4], data)))
        self.gyro = np.array(
            list(map(lambda x: x[4:7], data)))
        self.pos = None
        self.pos_proj_3d = None
        self.pos_proj_2d = None

    def find_average(self):
        vectors_accelerometer_x = self.accel[:, 0].tolist()
        vectors_accelerometer_y = self.accel[:, 1].tolist()
        vectors_accelerometer_z = self.accel[:, 2].tolist()
 
        def find_avr(sig, lag, is_lag):
            avr = 0;
            for i in range(lag, len(sig)):
                if (is_lag): avr += sig[i]
                else: avr += sig[i - lag]
            return avr/(len(sig) - lag)

        def auto_cor_up_part(sig, lag, sig_avr_with_no_lag, sig_avr_with_lag):
            up_part = 0
            for i in range(lag, len(sig)):
                up_part += (sig[i] - sig_avr_with_lag) * (sig[i - lag] - sig_avr_with_no_lag)
            return up_part

        def auto_cor_low_part(sig, lag, sig_avr_with_no_lag, sig_avr_with_lag):
            left_part = 0
            for i in range(lag, len(sig)):
                left_part += (sig[i] - sig_avr_with_lag) ** 2
            right_part = 0
            for i in range(lag, len(sig)):
                right_part += (sig[i - lag] - sig_avr_with_no_lag) ** 2
            return math.sqrt(left_part * right_part)

        def auto_cor(sig, lag):
            sig_avr_with_no_lag = find_avr(sig, lag, 0)
            sig_avr_with_lag = find_avr(sig, lag, 1)
            up_part = auto_cor_up_part(sig, lag, sig_avr_with_no_lag, sig_avr_with_lag)
            low_part = auto_cor_low_part(sig, lag, sig_avr_with_no_lag, sig_avr_with_lag)
            return up_part/low_part

        def find_best_autocorrelation_in_gesture(sig_x, sig_y, sig_z):
            best_cor = -3; best_cor_ind = -1
            delta_for_start = int(len(sig_x) * 0.2);
            delta_for_end = int(len(sig_x) * 0.14);
            step = 1
    
            in_wave = False
            delta_max = 0.22
    
            for i in range(delta_for_start, len(sig_x) - delta_for_end, step):
                loc = auto_cor(sig_x, i) + auto_cor(sig_y, i) + auto_cor(sig_z, i)
                loc /= 3
        
                if (in_wave):
                    if loc > best_cor:
                        best_cor = loc
                        best_cor_ind = i
                    else:
                        in_wave = False
                else:
                    if loc > best_cor + best_cor * delta_max:
                        in_wave = True
                        best_cor = loc
                        best_cor_ind = i
    
            if best_cor < 0.33: best_cor_ind = len(sig_x) - 1
            return best_cor_ind

        cor_ind = find_best_autocorrelation_in_gesture(vectors_accelerometer_x,
                                                vectors_accelerometer_y,
                                                vectors_accelerometer_z)

        def special_round(count_of_tacts):
            special_num = 8
            tmp = int(count_of_tacts * 10) % 10
            if (tmp > special_num): return int(count_of_tacts) + 1
            elif (tmp < special_num): return int(count_of_tacts)
            else:
                tmp = int(count_of_tacts * 100) % 10
                if (tmp > special_num): return int(count_of_tacts) + 1
                elif (tmp < special_num): return int(count_of_tacts)
                else:
                    tmp = int(count_of_tacts * 1000) % 10
                    if (tmp > special_num): return int(count_of_tacts) + 1
                    elif (tmp < special_num): return int(count_of_tacts)
                    else: int(count_of_tacts) + 1
    
        def avr_of_gesture(sig, final_cor):
            count_of_tacts = special_round(len(sig) / final_cor)
            final_cor = int(len(sig) / count_of_tacts)
            if count_of_tacts == 1: return sig
            new_sig = []
            for i in range(final_cor):
                tmp = 0;
                for j in range(count_of_tacts):
                    tmp += sig[i + final_cor * j]
                tmp /= count_of_tacts
                new_sig.append(tmp)
            print('count of tacts', count_of_tacts)
            return new_sig
        
        def find_best_idx(sig, final_cor):
            count_of_tacts = special_round(len(sig) / final_cor)
            return int(len(sig) / count_of_tacts)

        idx = find_best_idx(vectors_accelerometer_x, cor_ind)
        self.accel = self.accel[:idx,]
        self.gyro = self.gyro[:idx,]
        self.time = self.time[:idx,]

    def normalize(self, amount_of_avg=5):
        for _ in range(amount_of_avg):
            for i in range(self.accel.shape[0] - 1):
                for j in range(0, 3):
                    if abs((self.accel[i-1, j] + self.accel[i+1, j]) / 2 - self.accel[i, j]) > 0.1:
                        self.accel[i, j] = (self.accel[i-1, j] + self.accel[i+1, j]) / 2
            avg = np.array([0.0, 0.0, 0.0])
            for i in range(self.accel.shape[0]):
                avg += self.accel[i]
            avg /= self.accel.shape[0]
            for i in range(self.accel.shape[0]):
                self.accel[i] -= avg

    def normalize_gyro(self):
        start_gyro = self.gyro[0]

        for i in range(1, self.gyro.shape[0]):
            cur_gyro = start_gyro - self.gyro[i]
            x, y, z = cur_gyro
            rotation_mtx = np.array([
                [cos(z)*cos(y), -sin(z)*cos(x)+cos(z)*sin(y)*sin(x), sin(z)*sin(x)+cos(z)*sin(y)*cos(x)],
                [sin(z)*cos(y), cos(z)*cos(x)+sin(y)*sin(x), -cos(z)*sin(x)+sin(z)*sin(y)*cos(x)],
                [-sin(y), cos(y)*sin(x), cos(y)*cos(x)]
            ])
            self.accel[i] = rotation_mtx.dot(self.accel[i])

    def filter(self):
        def proc(data):
            return scipy.signal.lfilter(numerator_coeffs, denominator_coeffs, data)
        order = 2
        cutoff_freq = 0.6
        sampling_freq = 10
        sampling_duration = int(self.time[-1] * 1000)
        number_of_samples = self.accel.shape[0]
        normalized_cutoff_freq = 2 * cutoff_freq / sampling_freq
        numerator_coeffs, denominator_coeffs = scipy.signal.butter(order, normalized_cutoff_freq)
        self.accel = np.array([proc(self.accel[:, 0]), proc(self.accel[:, 1]), proc(self.accel[:, 2])]).T

    def find_pos(self, vel_comp=0.0125):
        res = []
        vel = np.array([0., 0., 0.])
        pos = np.array([0., 0., 0.])
        for i in range(1, self.accel.shape[0]):
            dt = self.time[i] - self.time[i - 1]
            vel += ((self.accel[i] + self.accel[i-1]) / 2) * dt
            if i == 1:
                vel = 0
            pos += vel * dt - vel * 0.0125
            res.append(np.array(pos))
        self.pos = np.array(res)

        self.pos_proj_3d = select_proj_3d(self.pos)
        self.pos_proj_2d = select_proj_2d(self.pos)
        return self.pos

    def draw_pos(self):
        if self.pos is None:
            self.find_pos()

        z_zeros = np.zeros(self.pos.shape[0])
        fig = go.Figure(data=[
            go.Scatter3d(x=self.pos[:, 0], y=self.pos[:, 1], z=self.pos[:, 2], opacity=0.5, name='Gesture'),
            go.Scatter3d(x=self.pos_proj_3d[:, 0], y=self.pos_proj_3d[:, 1], z=self.pos_proj_3d[:, 2], opacity=0.5, name='Gesture proj 3d'),
            go.Scatter3d(x=self.pos_proj_2d[:, 0], y=self.pos_proj_2d[:, 1], z=z_zeros, opacity=0.5, name='Gesture proj 2d')
        ])
        size_of_cube = 0.5
        fig.update_layout(
            scene = dict(xaxis = dict(nticks=4, range=[-size_of_cube,size_of_cube],),
                yaxis = dict(nticks=4, range=[-size_of_cube,size_of_cube],),
                zaxis = dict(nticks=4, range=[-size_of_cube,size_of_cube],),),
                width=700,
                margin=dict(r=20, l=10, b=10, t=10))
        fig.show()

    def pos_to_image(self, dir='data/imgs', filename='img'):
        if self.pos is None:
            self.find_pos()

        fig = plt.figure(frameon=False, figsize=[10, 10])
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        plt.plot(self.pos_proj_2d[:, 0], self.pos_proj_2d[:, 1], linewidth=5)
        plt.axis('equal')
        file_abs_path = dir + '/' + filename + '.jpg'
        plt.savefig(file_abs_path)
        plt.close(fig)
        return file_abs_path
