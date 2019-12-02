import numpy as np
import h5py
import sys

from cifStreamer.CIF2HDF5 import convertCIF2HDF5


def __main__():
    import time
    start_time = time.time()
    if (len(sys.argv) < 4 or len(sys.argv) > 6):
        print("Wrong number of input arguments. Usage: python convertCIF2HDF5 input.cif output.hdf5 targetSize maxNumbers channels")
    else:
        if (len(sys.argv) == 5):
            convertCIF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]), maxNumbers=int(sys.argv[4]), masked = True)
        elif (len(sys.argv) == 6):
            convertCIF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]), maxNumbers=int(sys.argv[4]),channels=sys.argv[5], masked = True)
        else:
            convertCIF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]), masked = True)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    __main__()
