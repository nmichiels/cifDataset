"""
This script will allow the user to convert a cif dataset to a hdf5 dataset. Masks are also exported to hdf5.

Args:
    inputFile (str): Input cif file
    outputFile (str): Output hdf5 file.
    img_size (int): Target resolution of the images.  All images are cropped, centered and padded to an output resolution of `img_size`.
    maxImages (int, optional): Number of images to convert.
    channelsString (str, optional): Channels to keep in the output dataset. (E.g `0,2,3,5`).
"""

import numpy as np
import h5py
import sys

from cifStreamer.CIF2HDF5 import convertCIF2HDF5


def __main__():
    import time
    start_time = time.time()
    if (len(sys.argv) < 4 or len(sys.argv) > 6):
        print("Wrong number of input arguments. Usage: python convertCIF2HDF5 input.cif output.hdf5 img_size [maxNumbers] [channels=All]")
    else:
        if (len(sys.argv) == 5):
            convertCIF2HDF5(inputFile = sys.argv[1], outputFile = sys.argv[2], img_size = int(sys.argv[3]), maxNumbers=int(sys.argv[4]), masked = False)
        elif (len(sys.argv) == 6):
            convertCIF2HDF5(inputFile = sys.argv[1], outputFile = sys.argv[2], img_size = int(sys.argv[3]), maxNumbers=int(sys.argv[4]),channels=sys.argv[5], masked = False)
        else:
            convertCIF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    __main__()
