#!/usr/bin/env pypy
import os
import time
import numpy as np
from PIL import Image

# 70
# 80

#horizontal= 70
#horizontal= 270
#horizontal= 207

#STAMP = "3162099"
#STAMP = "749113"
STAMP = "1297209"

def processing(pStamp, pI, pJ):
    filen = 'SAMPLE_{0}_{1}_{2}.dmp'.format(pStamp, pI, pJ)
    # numpy is very fast at reading binary files
    data = np.fromfile(filen, dtype=np.float32)
    average = np.mean(data)
    colour = int( (average/100)*255 )
    # return just the output value, so we're not passing lists around
    return colour

if __name__ == '__main__':
    t0 = time.time()
    
    VERTICAL = 80
    HORIZONTAL = 270
    
    pixels = np.zeros((HORIZONTAL, VERTICAL, 3), dtype=np.uint8)

    # in principle these loops could be parallelised, but in practice it's IO-limited
    for i in xrange(HORIZONTAL):
        for j in xrange(VERTICAL):
            col = processing(STAMP, i, j)
            # correcting for even vertical pixel data being generated
            # from and upward sweep of the antenna, and vice versa for the odd case
            if i%2: j = VERTICAL-1-j
            pixels[HORIZONTAL-1-i, j, :] = col
    
    IMG = Image.fromarray(pixels)
    print("done in", time.time()-t0)
        
    IMG.show()
