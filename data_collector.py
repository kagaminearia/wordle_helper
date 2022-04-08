import numpy as np
import cv2
import pytesseract as pyt
from matplotlib import pyplot as plt
from skimage.measure import regionprops, label
import pickle

'''
Collect character shape data from the official wordle website:
https://www.nytimes.com/games/wordle/index.html

Collected data can be found in img_data folder
'''

img_ls = []
blk = np.array([0, 0, 0])
f_name = 'characters.pickle'
f = open(f_name, 'wb')

for i in range(0, 26, 5):
    temp = []
    for j in range(i, i + 5):
        if j < 26: temp.append(chr(97 + j))
    img_ls.append(''.join(temp) + '.png')

for img_name in img_ls:

    img = cv2.imread(f'img_data/{img_name}')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.imshow(img)
    plt.show()

    blk = np.array([0, 0, 0])
    m, n, _ = img.shape
    mask = np.zeros((m, n))

    for i in range(m):
        for j in range(n):
            if np.sum(np.absolute(blk - img[i, j])) < 10:
                mask[i, j] = 1
    
    mask = mask.astype('int')
    res = label(mask)

    regions = regionprops(res)

    for region in regions:

        if region.area > 2000: continue
        minr, minc, maxr, maxc = region.bbox

        # print (minr, maxr, minc, maxc, maxr - minr, maxc - minc)

        len_x, len_y = maxr - minr, maxc - minc
        len_max = max(len_x, len_y)

        pad_x, pad_y = len_max - len_x, len_max - len_y

        curr = mask[minr : maxr, minc : maxc]
        curr = np.pad(curr, pad_width = [(0, pad_x), (0, pad_y)], mode = 'constant')
        curr = curr.astype('float32')

        # resize everything to shape 22 * 22 for comparision
        curr = cv2.resize(curr, (22, 22), interpolation = cv2.INTER_AREA)
        
        # convert the ndarray to binary
        curr[curr < 0.5] = 0
        curr[curr > 0.5] = 1

        pickle.dump(curr, f)