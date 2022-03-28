import numpy as np
import cv2
import pytesseract as pyt
from matplotlib import pyplot as plt
from skimage.measure import regionprops, label
from copy import deepcopy

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
    
    # read the input image, convert the image to RGB type for ease of recognization
    img = cv2.imread(img_name)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_g = deepcopy(img)
    m, n, _ = img.shape
    mask = np.zeros((m, n))
    
    # get the mask 
    for i in range(m):
        for j in range(n):
            if np.sum(np.absolute(img[i, j] - np.array([[255, 255, 255]]))) < 10: 
                mask[i, j] = 1
                img_g[i, j] = np.array([[0, 0, 0]])
            else: mask[i, j] = 0

    # plt.imshow(mask)
    # plt.show()
    
    # process on the mask
    mask = mask.astype('int')
    res = label(mask)

    # plt.imshow(res)
    # plt.show()
    
    # get the possible regions
    regions = regionprops(res)
    token = 0

    for region in regions:

        # analyze on the bbox, get the possible character
        if region.area > 2000: continue
        pos = token % 5
        minr, minc, maxr, maxc = region.bbox
        curr = img_g[minr - 8 : maxr + 5, minc - 8 : maxc + 5]
        
        # read text from image using pytesseract
        configuration = ("-l eng --oem 1 --psm 10")
        temp = pyt.image_to_boxes(curr, config = configuration)
        print(temp)
        if not temp[0].isalpha(): 
            token += 1
            continue

        color = img_g[minr - 5, minc - 5]
        print(color)
        for i in range(len(colors)):
            if np.sum(np.absolute(color - colors[i])) < 10: 
                info[i].add((temp[0].lower(), pos))
                # break
        
        token += 1
    print(info)
    return info



