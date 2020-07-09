"""
This script will allow the user to convert a cif dataset to a hdf5 dataset. Masks are `NOT` exported to hdf5.

Args:
    inputPattern (str): Directory and pattern of tiff images (e.g. `images_%d.tiff`).
    outputFile (str): Output hdf5 file.
    img_size (int): Target resolution of the images.  All images are cropped, centered and padded to an output resolution of `img_size`.
    channelsString (str, optional): Channels to keep in the output dataset. (E.g `0,2,3,5`).
 """


import numpy as np
import h5py
import sys

from cifStreamer.TIFF2HDF5 import convertTIFF2HDF5_nomask


def __main__():


    if (len(sys.argv) < 4 or len(sys.argv) > 5):
        print("Wrong number of input arguments. Usage: python convertTIFF2HDF5 tiffPatern output.hdf5 img_size [channels]")
    else:
        if (len(sys.argv) == 5):
            convertTIFF2HDF5_nomask(inputPattern = sys.argv[1], outputFile = sys.argv[2], img_size = int(sys.argv[3]), channelsString = sys.argv[4])
        else:
            convertTIFF2HDF5_nomask(inputPattern = sys.argv[1], outputFile = sys.argv[2], img_size = int(sys.argv[3]))
  

if __name__ == "__main__":
    __main__()

