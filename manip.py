#!/usr/bin/env pypy
import os
import time
import tqdm
import multiprocessing as mp
from PIL import Image
import numpy

# 70
# 80

#horizontal= 70
#horizontal= 270
#horizontal= 207

#STAMP = "3162099"
#STAMP = "749113"
STAMP = "1297209"


def processing(params):
    pStamp, pI, pJ, VER, HOR, _ = params

    ## put data in RAM
    filename = 'SAMPLE_{0}_{1}_{2}.dmp'.format(pStamp, str(pI), str(pJ) )
    tech = numpy.fromfile(filename, numpy.float32)

    ## DATA MANIP START
    average = numpy.average(tech)
    colour = int( (average/100)*255 )

    hold = [ pStamp, pI, pJ, VER, HOR, colour ]
    return hold
    #print("{0} : [{1},{2}]".format(average,pI,pJ)) # DEBUG


if __name__ == '__main__':
    
    VERTICAL = 80
    HORIZONTAL = 270
    
    IMG = Image.new('RGB', (HORIZONTAL, VERTICAL), 'black')
    PIXELS = IMG.load()

    # create file processing queue
    DUMPS = []
    for i in xrange(HORIZONTAL):
        for j in xrange(VERTICAL):
            DUMPS.append([ STAMP, i, j, VERTICAL, HORIZONTAL, 0])

    # create threadpool and process the data
    pewl = mp.Pool(3)
    print("processing...")

    for PXL in tqdm.tqdm(pewl.imap_unordered(processing, DUMPS), total=len(DUMPS)):
        # correcting for even vertical pixel data being generated
        # from and upward sweep of the antenna, and vice versa for the odd case
        if PXL[1]/2 == PXL[1]/2.0:
            reverse = 0
        else:
            reverse = VERTICAL - 1

        PIXELS[ HORIZONTAL-1-PXL[1], abs(PXL[2] - reverse) ] = (PXL[5], PXL[5], PXL[5])
        
    print("done.")
        
    IMG.show()
