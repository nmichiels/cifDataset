from FlowSightReaderC.eigen cimport *

import numpy as np
cimport numpy as np

from libcpp.string cimport string
from libcpp cimport bool

np.import_array()

cdef extern from "FlowSightReaderC.h":
  cdef void c_openGreyscaleBytes "openGreyscaleBytes" (int, int, int, int, int, Map[Matrixf]&)
  cdef void c_openBitmaskBytes "openBitmaskBytes" (int, int, int, int, int, Map[Matrixf]&)
  cdef bool c_openFile "openFile" (string&)
  

def openFile(string &fileName):
  return c_openFile(fileName)



def openGreyscaleBytes(int imageWidth, int imageHeight, int nchannels, int stripByteCounts, int stripOffsets,  np.ndarray uncompressed):
  if (np.isfortran(uncompressed)):
    print("WARNING openGreyscaleBytes(): Order of uncompressed is Fortran .. expecting C")

  if (uncompressed.dtype != np.float32):
    print("WARNING openGreyscaleBytes(): Type of uncompressed is ", uncompressed.dtype, "... expecting float32.")
 
  c_openGreyscaleBytes(imageWidth, imageHeight, nchannels, stripByteCounts, stripOffsets, Map[Matrixf](uncompressed))


def openBitmaskBytes(int imageWidth, int imageHeight, int nchannels, int stripByteCounts, int stripOffsets,  np.ndarray uncompressed):
  if (np.isfortran(uncompressed)):
    print("WARNING openGreyscaleBytes(): Order of uncompressed is Fortran .. expecting C")

  if (uncompressed.dtype != np.float32):
    print("WARNING openGreyscaleBytes(): Type of uncompressed is ", uncompressed.dtype, "... expecting float32.")
 
  c_openBitmaskBytes(imageWidth, imageHeight, nchannels, stripByteCounts, stripOffsets, Map[Matrixf](uncompressed))

