from FlowSightReaderC.eigen cimport *

import numpy as np
cimport numpy as np

np.import_array()

cdef extern from "FlowSightReaderC.h":
  cdef void c_openGreyscaleBytes "openGreyscaleBytes" (int, int, int, int, int, Map[Matrixf]&)
  


def openGreyscaleBytes(int imageWidth, int imageHeight, int nchannels, int stripByteCounts, int stripOffsets,  np.ndarray uncompressed):
  if (np.isfortran(uncompressed)):
    print("WARNING openGreyscaleBytes(): Order of uncompressed is Fortran .. expecting C")

  if (uncompressed.dtype != np.float32):
    print("WARNING openGreyscaleBytes(): Type of uncompressed is ", uncompressed.dtype, "... expecting float32.")
 

  # #double precision
  #image = image.astype(dtype=np.float64, order='C', copy=False)
  #centers = centers.astype(dtype=np.float64, order='C', copy=False)
  #areas = areas.astype(dtype=np.float64, order='C', copy=False)
  #c_getGaborScoreDoublePrec(Map[ConstMatrixd](image), Map[ConstMatrixs](labels), nobjects, frequency, nAngles, Map[ConstMatrixd](centers), Map[ConstVecd](areas), Map[Vecd](best_score))

  # float precision
  # uncompressed = uncompressed.astype(dtype=np.float32, order='C', copy=False)
  c_openGreyscaleBytes(imageWidth, imageHeight, nchannels, stripByteCounts, stripOffsets, Map[Matrixf](uncompressed))

