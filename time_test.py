#!/usr/bin/env python

import numpy as np
from bitstring import ConstBitStream
import time

data = np.arange(0, 1000000, 0.1).astype('float32')

data.tofile("test.dat")



def old_way(fname):
    f = open(fname, 'rb')
    read = handleDump(f)
    f.close()
    return read

def handleDump(fileObj):
    tech = []
    raw = ConstBitStream(fileObj)
    try:
        while True:
            tech.append(raw.read('floatle:32'))
    except:
        pass
    del(raw)
    return tech 


def numpy_way(fname):
    return np.fromfile(fname, "float32")

def time_millis():
    return int(round(time.time() * 1000))


numpy_start = time_millis()
np_dat = numpy_way("test.dat")
numpy_end = time_millis()

old_start = time_millis()
old_dat = old_way("test.dat")
old_end = time_millis()


print("Numpy: %10i ms"%(numpy_end-numpy_start))
print("  Old: %10i ms"%(old_end-old_start))















