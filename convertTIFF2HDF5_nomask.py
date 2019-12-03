import numpy as np
import h5py
import sys

from cifStreamer.TIFF2HDF5 import convertTIFF2HDF5_nomask


def __main__():

    #convertTIFF2HDF5_nomask("C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/TIF files batch 1/TIF files/d8001 B57-15 IFN_%d_Ch%d.ome.tif", 
                            #"C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/d8001_B57-15_IFN_batch1_35x35.hdf5", 35)
    convertTIFF2HDF5_nomask("C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/TIF files batch 1/TIF files/batch 2 d8001 CEF32_%d_Ch%d.ome.tif", 
                            "C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/d8001_CEF32+Nivo_batch1_35x35.hdf5", 35)

    if (len(sys.argv) < 4 or len(sys.argv) > 5):
        print("Wrong number of input arguments. Usage: python convertTIFF2HDF5 tiffPatern output.hdf5 targetSize")
    else:
        if (len(sys.argv) == 5):
            convertTIFF2HDF5_nomask(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
        else:
            convertTIFF2HDF5_nomask(sys.argv[1], sys.argv[2], int(sys.argv[3]))
  

if __name__ == "__main__":
    __main__()

