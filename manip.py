#!/usr/bin/env pypy
# These make division and print work like in python 3, making the code compatible in
# both versions.
from __future__ import division
from __future__ import print_function

# Make sure that we are using the generator function for range in both python 2 and 3.
import builtins
if hasattr(builtins, 'xrange'):
    range = xrange

import os
import time

from PIL import Image
import multiprocessing as mp
import numpy
import tqdm

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
    colour = int( (average*255)//100 )

    hold = [ pStamp, pI, pJ, VER, HOR, colour ]
    return hold
    #print("{0} : [{1},{2}]".format(average,pI,pJ)) # DEBUG


def main():
    start = time.time()

    VERTICAL = 80
    HORIZONTAL = 206

    IMG = Image.new('RGB', (HORIZONTAL, VERTICAL), 'black')
    PIXELS = IMG.load()

    # create file processing queue
    DUMPS = []
    for i in range(HORIZONTAL):
        for j in range(VERTICAL):
            DUMPS.append([ STAMP, i, j, VERTICAL, HORIZONTAL, 0])

    # create threadpool and process the data
    pewl = mp.Pool(3)
    print("processing...")

    for PXL in tqdm.tqdm(pewl.imap_unordered(processing, DUMPS), total=len(DUMPS)):
        # correcting for even vertical pixel data being generated
        # from and upward sweep of the antenna, and vice versa for the odd case
        if PXL[1]//2 == PXL[1]/2:
            reverse = 0
        else:
            reverse = VERTICAL - 1

        PIXELS[ HORIZONTAL-1-PXL[1], abs(PXL[2] - reverse) ] = (PXL[5], PXL[5], PXL[5])

    print("Done. Processing took: %d s." % int(time.time() - start))

    IMG.show()


if __name__ == '__main__':
    main()
