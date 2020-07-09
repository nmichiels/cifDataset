"""
This script will allow the user to convert a cif dataset to a hdf5 dataset. Masks are also exported to hdf5.

Args:
    inputPattern (str): Directory and pattern of tiff images (e.g. `images_%d.tiff`).
    maskPattern (str): Directory and pattern of tiff masks
    outputFile (str): Output hdf5 file.
    img_size (int): Target resolution of the images.  All images are cropped, centered and padded to an output resolution of `img_size`.
    maxImages (int, optional): Number of images to convert.
    masked (bool, optional): Apply mask to output file. Remove all pixels outside of mask.
    channelsString (str, optional): Channels to keep in the output dataset. (E.g `0,2,3,5`).
    batchSize (int, optional): Specify batch size of HDF5 file format.
    chunkSize (int, optional): Specify chunk size of HDF5 file format.
"""

import numpy as np
import h5py
import sys

from cifStreamer.TIFF2HDF5 import convertTIFF2HDF5


def __main__():


    
    import time
    start_time = time.time()
    if (len(sys.argv) < 4 or len(sys.argv) > 6):
        print("Wrong number of input arguments. Usage: python convertTIFF2HDF5 inputPattern maskPattern output.hdf5 targetSize [maxNumbers] [channels=all]")
    else:
        if (len(sys.argv) == 6):
            convertTIFF2HDF5(inputPattern = sys.argv[1], maskPattern = sys.argv[2], outputFile = sys.argv[3], img_size = int(sys.argv[4]), maxImages = int(sys.argv[5]))
        elif (len(sys.argv) == 7):
            convertTIFF2HDF5(inputPattern = sys.argv[1], maskPattern = sys.argv[2], outputFile = sys.argv[3], img_size = int(sys.argv[4]), maxImages = int(sys.argv[5]), channelsString = sys.argv[6])
        else:
            convertTIFF2HDF5(inputPattern = sys.argv[1], maskPattern = sys.argv[2], outputFile = sys.argv[3], img_size = int(sys.argv[4]))
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    __main__()

