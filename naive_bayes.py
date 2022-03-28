import os, cv2
from roipoly import RoiPoly
from matplotlib import pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
import math
from time import time
from collections import Counter

X, y = np.array([]), np.array([])

def data_loader(X, y):

    fname_csv = 'wordle_sample.csv'
    curr_arr = np.genfromtxt(fname_csv, delimiter = ',')
    curr_arr = curr_arr.astype(int)

    curr_x, curr_y = curr_arr[:, : 3], curr_arr[:, -1].reshape((1, -1))

    return curr_x, curr_y

    # if X.size == 0: X = curr_x
    # else: X = np.concatenate((X, curr_x), axis = 0)
    
    # if y.size == 0: y = curr_y
    # else: y = np.concatenate((y, curr_y), axis = 1)

t1 = time()
X, y = data_loader(X, y)
t2 = time()
y = y.T

print ('data loading takes {} seconds'.format(t2 - t1))

print ('Shape of X is {}. Shape of y is {}.'.format(X.shape, y.shape))

from collections import defaultdict

def def_value():
    return []

dict_ = defaultdict(def_value)

for i in range(X.shape[0]):
    curr_x, curr_y = X[i], y[i]
    dict_[curr_y[0]].append(curr_x)

print (len(dict_))

info = {}

for label, val in dict_.items():
    temp = [(np.mean(ele), np.std(ele)) for ele in zip(*val)]
    print (temp)
    info[label] = temp

p_label = {}

for ele in dict_.keys():
    p_label[ele] = np.count_nonzero(y == ele) / len(y)

print (p_label)

def gaussian(x, m, std):
    expo = math.exp(-(math.pow(x - m, 2) / (2 * math.pow(std, 2))))
    return (1 / (math.sqrt(2 * math.pi) * std)) * expo

img = cv2.imread('wordle_sample.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 

m, n = img.shape[: 2]
y_pred = np.zeros((m, n))

for i in range(m):
    for j in range(n):
        ele, curr = img[i, j], [1 for _ in range(len(dict_))]
        for k_index, k in enumerate(dict_.keys()):
            curr_p = p_label[k]
            curr[k_index] *= curr_p
            for idx in range(len(ele)):
                m, std = info[k][idx]
                curr[k_index] *= gaussian(ele[idx], m, std)
        curr = np.array(curr)
        y_pred[i, j] = np.argmax(curr)
#         if np.argmax(curr) == 0: y_pred[i, j] = 1
# #         if curr[0] > curr[1]: y_pred[i, j] = 0
#         else: y_pred[i, j] = 0

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.imshow(img)
ax2.imshow(y_pred)

