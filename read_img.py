import numpy as np
import cv2
import pytesseract as pyt
from matplotlib import pyplot as plt
from skimage.measure import regionprops, label
import pickle as pk

def read_img(info, colors, img_name = 'wordle.png'):

    '''
    Read an input image, filter the information on the image based on colors.

    :param: info
    :type: list
    :param: colors
    :type: np.ndarray
    :param: img_name
    :type: str
    :rtype: list
    '''

    # initialize parameters
    wht = np.array([255, 255, 255])
    chars = [chr(97 + i) for i in range(26)]

    # read the input image, create a zero mask for it
    img = cv2.imread(img_name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    m, n, _ = img.shape
    mask = np.zeros((m, n))

    # load file from the pickle file generated by data_collector.py
    f_name = 'c_store.pickle'
    f = open(f_name, 'rb')
    dic = pk.load(f)
    f.close()

    # get the mask 
    for i in range(m):
        for j in range(n):
            if np.sum(np.absolute(img[i, j] - wht)) < 10: 
                mask[i, j] = 1
    
    # process on the mask
    mask = mask.astype('int')
    res = label(mask)
    
    # get the possible regions
    regions = regionprops(res)
    
    # track the index
    index = 0

    for region in regions:

        # analyze on the bbox, filter the possible regions based on area and shape of bbox
        if region.area > 2000: continue
        minr, minc, maxr, maxc = region.bbox
        len_x, len_y = maxr - minr, maxc - minc
        if len_x >= 6 * len_y or len_x <= 1/6 * len_y: continue

        len_max = max(len_x, len_y)
        pad_x, pad_y = len_max - len_x, len_max - len_y

        curr = mask[minr : maxr, minc : maxc]
        curr = np.pad(curr, pad_width = [(0, pad_x), (0, pad_y)], mode = 'constant').astype(np.float32)
        curr = cv2.resize(curr, (22, 22), interpolation = cv2.INTER_AREA)

        char_score = np.zeros(26)

        for i in range(26):
            char = chars[i]
            value = dic[char]
            char_score[i] = np.sum(curr == value) / np.sum(curr != value) if np.sum(curr != value) != 0 else 1000
        
        # use argmax to find the character with the highest possibility
        char_here = chars[np.argmax(char_score)]
        
        # find the color of the corresponding character
        color = img[minr - 10, minc - 10]

        # track the index of this character
        index %= 5
        
        # add the color and character information
        curr_color = np.zeros(3)
        for i in range(len(colors)):
            curr_color[i] = np.sum(np.absolute(color - colors[i])) 
        
        curr_color_index = np.argmin(curr_color)
        info[curr_color_index].add((char_here, index))
        
        index += 1
    
    return info



