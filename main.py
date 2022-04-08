import numpy as np
from read_img import read_img
from time import time
import sys

def get_outputs(img_name = 'wordle.png'):

    '''
    Get outputs for the input image
    
    :param: img_name
    :type: str
    '''

    t1 = time()

    COLORS = [np.array([[120, 124, 126]]), \
            np.array([[201, 182, 95]]), \
            np.array([[106, 172, 105]])]

    gray, yellow, green = set(), set(), set()
    poss = [gray, yellow, green]

    poss = read_img(poss, COLORS, img_name)
    print (poss)

    res, res_full = [], []

    # check commonly used words
    with open('words_five.txt', 'rt') as f:
        for line in f: 
            judge = True

            # check gray 
            for c, idx in gray:
                if line[idx] == c: 
                    judge = False
                    break

            if judge:
                # check green
                for c, idx in green:
                    if line[idx] != c: 
                        judge = False
                        break

            if judge:
                # check yellow
                for c, idx in yellow:
                    if c not in line:
                        judge = False
                        break
                    elif line[idx] == c:
                        judge = False
                        break
            if judge: 
                res.append(line[: -1])
    
    t2 = time()

    # check all words if there are not enough words produced by reading the most frequent word list
    if len(res) <= 10: 
        with open('words_five_full.txt', 'rt') as f:
            for line in f: 
                judge = True

                # check gray 
                for c, idx in gray:
                    if line[idx] == c: 
                        judge = False
                        break
                    
                if judge:
                    # check green
                    for c, idx in green:
                        if line[idx] != c: 
                            judge = False
                            break
                if judge:
                    # check yellow
                    for c, idx in yellow:
                        if c not in line:
                            judge = False
                            break
                        elif line[idx] == c:
                            judge = False
                            break
                if judge: 
                    res_full.append(line[: -1])
            
    t3 = time()

    # print out results
    if len(res) > 10:
        print ('Some possible commonly used words are ' + ', '.join(res))
        print ('Got these words for you in just %.2f seconds' % (t2 - t1))
    elif len(res_full) < 1:
        print ('No words found based on your input!')
    elif len(res_full) == 1:
        print ('It got to be {}!'.format(res_full[0]))
        print ('Got this unique word for you in just %.2f seconds' % (t3 - t1))
    else: 
        print ('Some possible words are ' + ', '.join(res_full))
        print ('Got these words for you in just %.2f seconds' % (t3 - t1))

if __name__ == '__main__':

    if len(sys.argv) > 1: get_outputs(sys.argv[1])
    else: get_outputs()