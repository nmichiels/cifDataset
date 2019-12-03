import numpy as np
import h5py
import sys

from cifStreamer.TIFF2HDF5 import convertTIFF2HDF5


def __main__():

    #convertTIFF2HDF5("C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/TIF files batch 1/TIF files/d8001 B57-15 IFN_%d_Ch%d.ome.tif",
    #                 "C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/TIF files batch 1/ExportedMasks/d8001 B57-15 IFN_%d_Ch%d.dmask.pgm",
    #                 "C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/d8001_B57-15_IFN_batch1_35x35.hdf5", 35)
    #convertTIFF2HDF5("C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/TIF files batch 1/TIF files/batch 2 d8001 B57-15 + Nivo_%d_Ch%d.ome.tif",
    #                 "C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/ExportedMasks/batch 2 d8001 B57-15 + Nivo_%d_Ch%d.dmask.pgm",
    ##                 "C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/d8001_B57-15+Nivo_IFN_batch2_35x35.hdf5", 35)
    #convertTIFF2HDF5("C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/TIF files batch 1/TIF files/batch 2 d8001 CEF32_%d_Ch%d.ome.tif",
    #                 "C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/ExportedMasks/batch 2 d8001 CEF32_%d_Ch%d.dmask.pgm",
    #                 "C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/d8001_CEF32_batch2_35x35.hdf5", 35)
    #convertTIFF2HDF5("C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/TIF files batch 1/TIF files/batch 2 d8001 CEF32 + Nivo_%d_Ch%d.ome.tif",
    #                 "C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/ExportedMasks/batch 2 d8001 CEF32 + Nivo_%d_Ch%d.dmask.pgm",
    #                 "C:/Users/nmichiels/Desktop/201909 d8001 for Nick TIF files/d8001_CEF32+Nivo_batch2_35x35.hdf5", 35)

    #convertTIFF2HDF5("E:/Projects/ImmCyte/data/20190906_d8001_exp3/d8001_CEF32_batch1/d8001_CEF32_batch1_%d_Ch%d.ome.tif",
    #                 "E:/Projects/ImmCyte/data/20190906_d8001_exp3/d8001_CEF32_batch1/ExportedMasks/d8001_CEF32_batch1_%d_Ch%d.dmask.pgm",
    #                 "E:/Projects/ImmCyte/data/20190906_d8001_exp3_tiff/d8001_CEF32_batch1_35x35.hdf5", 35)
    #convertTIFF2HDF5("E:/Projects/ImmCyte/data/20190906_d8001_exp3/d8001_B57-15_batch1/d8001_B57-15_batch1_%d_Ch%d.ome.tif",
    #                 "E:/Projects/ImmCyte/data/20190906_d8001_exp3/d8001_B57-15_batch1/ExportedMasks/d8001_B57-15_batch1_%d_Ch%d.dmask.pgm",
    #                 "E:/Projects/ImmCyte/data/20190906_d8001_exp3_tiff/d8001_B57-15_batch1_35x35.hdf5", 35)
    convertTIFF2HDF5("E:/Projects/ImmCyte/data/20190906_d8001_exp3/d8001_B57-15_batch2/d8001_B57-15_batch2_%d_Ch%d.ome.tif",
                     "E:/Projects/ImmCyte/data/20190906_d8001_exp3/d8001_B57-15_batch2/ExportedMasks/d8001_B57-15_batch2_%d_Ch%d.dmask.pgm",
                     "E:/Projects/ImmCyte/data/20190906_d8001_exp3_tiff/d8001_B57-15_batch2_35x35.hdf5", 35)
    
    
    
    import time
    start_time = time.time()
    if (len(sys.argv) < 4 or len(sys.argv) > 6):
        print("Wrong number of input arguments. Usage: python convertTIFF2HDF5 input.cif output.hdf5 targetSize maxNumbers channels")
    else:
        if (len(sys.argv) == 5):
            convertTIFF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
        elif (len(sys.argv) == 6):
            convertTIFF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]),sys.argv[5])
        else:
            convertTIFF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    __main__()

