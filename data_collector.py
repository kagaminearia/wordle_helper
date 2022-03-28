import os, cv2
from roipoly import RoiPoly
from matplotlib import pyplot as plt
import numpy as np

if __name__ == '__main__':

    fname_img = 'wordle.png'
    img = cv2.imread(fname_img)
    # can be changed to other color space, eg. COLOR_BGR2HSV, but please keep it consecutive and consistent
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    m, n, _ = img.shape

    judge = True

    while judge:

        # display the image and use roipoly for labeling
        fig, ax = plt.subplots()
        ax.imshow(img)
        my_roi = RoiPoly(fig=fig, ax=ax, color='r')

        # get the image mask
        mask = my_roi.get_mask(img)

        # get the y value for this part of training set
        val_1 = input('Please enter 0 for white, 1 for gray, 2 for yellow, 3 for green: ')
        response_1 = ['1', '2', '3', '0'] 
        while val_1 not in response_1: val_1 = input('Invalid input. Please enter 0 for white, 1 for gray, 2 for yellow, 3 for green: ')
        y = np.array([int(val_1)])

        # write data into csv file in format [r, g, b, y]
        fname_csv = 'wordle_sample.csv'
        # print (fname_csv)
        with open(fname_csv, 'ab') as f:
            for i in range(m):
                for j in range(n):
                    if mask[i, j]: 
                        np.savetxt(f, np.concatenate((img[i, j, :], y)).reshape(1, -1), delimiter = ',', newline = '\n')
        f.close()

        # continue to get data from this dataset if needed
        val_2 = input('Are you done with working on this dataset? (Yes or No) ')
        response_2 = ['Yes', 'yes', 'YES', 'y', 'Y', 'No', 'no', 'NO', 'n', 'N']
        while val_1 not in response_1: val_1 = input('Invalid input. Please enter yes or no: ')
        if val_2 in response_2[: 5]: judge = False
        else: judge = True

        # test loading data as numpy array
    curr_arr = np.genfromtxt(fname_csv, delimiter = ',')
    print (curr_arr.shape)