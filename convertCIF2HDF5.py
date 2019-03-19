import numpy as np
import h5py
import sys

from cifStreamer.CIF2HDF5 import convertCIF2HDF5


def __main__():
    import time
    start_time = time.time()
    if (len(sys.argv) < 4 or len(sys.argv) > 5):
        print("Wrong number of input arguments. Usage: python convertCIF2HDF5 input.cif output.hdf5 targetSize")
    else:
        if (len(sys.argv) == 5):
            convertCIF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
        else:
            convertCIF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    __main__()
