cimport cython
import numpy as np
cimport numpy as np
from numpy.lib.stride_tricks import as_strided

@cython.boundscheck(False)
cdef np.ndarray[double, ndim=2] ndarray_double_C(double *data, long rows, long cols, long row_stride, long col_stride):
    cdef double[:,:] mem_view = <double[:rows,:cols]>data
    dtype = 'double'
    cdef int itemsize = np.dtype(dtype).itemsize
    return as_strided(np.asarray(mem_view, dtype=dtype, order="C"), strides=[row_stride*itemsize, col_stride*itemsize])

@cython.boundscheck(False)
cdef np.ndarray[double, ndim=2] ndarray_double_F(double *data, long rows, long cols, long row_stride, long col_stride):
    cdef double[::1,:] mem_view = <double[:rows:1,:cols]>data
    dtype = 'double'
    cdef int itemsize = np.dtype(dtype).itemsize
    return as_strided(np.asarray(mem_view, dtype=dtype, order="F"), strides=[row_stride*itemsize, col_stride*itemsize])

@cython.boundscheck(False)
cdef np.ndarray[double, ndim=2] ndarray_copy_double_C(const double *data, long rows, long cols, long row_stride, long col_stride):
    cdef double[:,:] mem_view = <double[:rows,:cols]>data
    dtype = 'double'
    cdef int itemsize = np.dtype(dtype).itemsize
    return np.copy(as_strided(np.asarray(mem_view, dtype=dtype, order="C"), strides=[row_stride*itemsize, col_stride*itemsize]))

@cython.boundscheck(False)
cdef np.ndarray[double, ndim=2] ndarray_copy_double_F(const double *data, long rows, long cols, long row_stride, long col_stride):
    cdef double[::1,:] mem_view = <double[:rows:1,:cols]>data
    dtype = 'double'
    cdef int itemsize = np.dtype(dtype).itemsize
    return np.copy(as_strided(np.asarray(mem_view, dtype=dtype, order="F"), strides=[row_stride*itemsize, col_stride*itemsize]))


@cython.boundscheck(False)
cdef np.ndarray[float, ndim=2] ndarray_float_C(float *data, long rows, long cols, long row_stride, long col_stride):
    cdef float[:,:] mem_view = <float[:rows,:cols]>data
    dtype = 'float'
    cdef int itemsize = np.dtype(dtype).itemsize
    return as_strided(np.asarray(mem_view, dtype=dtype, order="C"), strides=[row_stride*itemsize, col_stride*itemsize])

@cython.boundscheck(False)
cdef np.ndarray[float, ndim=2] ndarray_float_F(float *data, long rows, long cols, long row_stride, long col_stride):
    cdef float[::1,:] mem_view = <float[:rows:1,:cols]>data
    dtype = 'float'
    cdef int itemsize = np.dtype(dtype).itemsize
    return as_strided(np.asarray(mem_view, dtype=dtype, order="F"), strides=[row_stride*itemsize, col_stride*itemsize])

@cython.boundscheck(False)
cdef np.ndarray[float, ndim=2] ndarray_copy_float_C(const float *data, long rows, long cols, long row_stride, long col_stride):
    cdef float[:,:] mem_view = <float[:rows,:cols]>data
    dtype = 'float'
    cdef int itemsize = np.dtype(dtype).itemsize
    return np.copy(as_strided(np.asarray(mem_view, dtype=dtype, order="C"), strides=[row_stride*itemsize, col_stride*itemsize]))

@cython.boundscheck(False)
cdef np.ndarray[float, ndim=2] ndarray_copy_float_F(const float *data, long rows, long cols, long row_stride, long col_stride):
    cdef float[::1,:] mem_view = <float[:rows:1,:cols]>data
    dtype = 'float'
    cdef int itemsize = np.dtype(dtype).itemsize
    return np.copy(as_strided(np.asarray(mem_view, dtype=dtype, order="F"), strides=[row_stride*itemsize, col_stride*itemsize]))

@cython.boundscheck(False)
cdef np.ndarray[int, ndim=2] ndarray_int_C(int *data, long rows, long cols, long row_stride, long col_stride):
    cdef int[:,:] mem_view = <int[:rows,:cols]>data
    dtype = 'int'
    cdef int itemsize = np.dtype(dtype).itemsize
    return as_strided(np.asarray(mem_view, dtype=dtype, order="C"), strides=[row_stride*itemsize, col_stride*itemsize])

@cython.boundscheck(False)
cdef np.ndarray[int, ndim=2] ndarray_int_F(int *data, long rows, long cols, long row_stride, long col_stride):
    cdef int[::1,:] mem_view = <int[:rows:1,:cols]>data
    dtype = 'int'
    cdef int itemsize = np.dtype(dtype).itemsize
    return as_strided(np.asarray(mem_view, dtype=dtype, order="F"), strides=[row_stride*itemsize, col_stride*itemsize])

@cython.boundscheck(False)
cdef np.ndarray[int, ndim=2] ndarray_copy_int_C(const int *data, long rows, long cols, long row_stride, long col_stride):
    cdef int[:,:] mem_view = <int[:rows,:cols]>data
    dtype = 'int'
    cdef int itemsize = np.dtype(dtype).itemsize
    return np.copy(as_strided(np.asarray(mem_view, dtype=dtype, order="C"), strides=[row_stride*itemsize, col_stride*itemsize]))

@cython.boundscheck(False)
cdef np.ndarray[int, ndim=2] ndarray_copy_int_F(const int *data, long rows, long cols, long row_stride, long col_stride):
    cdef int[::1,:] mem_view = <int[:rows:1,:cols]>data
    dtype = 'int'
    cdef int itemsize = np.dtype(dtype).itemsize
    return np.copy(as_strided(np.asarray(mem_view, dtype=dtype, order="F"), strides=[row_stride*itemsize, col_stride*itemsize]))

@cython.boundscheck(False)
cdef np.ndarray[char, ndim=2] ndarray_bool_C(bool *data, long rows, long cols, long row_stride, long col_stride):
    cdef bool[:,:] mem_view = <bool[:rows,:cols]>data
    dtype = 'uint8'
    cdef int itemsize = np.dtype(dtype).itemsize
    return as_strided(np.asarray(mem_view, dtype=dtype, order="C"), strides=[row_stride*itemsize, col_stride*itemsize])

@cython.boundscheck(False)
cdef np.ndarray[char, ndim=2] ndarray_bool_F(bool *data, long rows, long cols, long row_stride, long col_stride):
    cdef bool[::1,:] mem_view = <bool[:rows:1,:cols]>data
    dtype = 'uint8'
    cdef int itemsize = np.dtype(dtype).itemsize
    return as_strided(np.asarray(mem_view, dtype=dtype, order="F"), strides=[row_stride*itemsize, col_stride*itemsize])

@cython.boundscheck(False)
cdef np.ndarray[char, ndim=2] ndarray_copy_bool_C(const bool *data, long rows, long cols, long row_stride, long col_stride):
    cdef bool[:,:] mem_view = <bool[:rows,:cols]>data
    dtype = 'uint8'
    cdef int itemsize = np.dtype(dtype).itemsize
    return np.copy(as_strided(np.asarray(mem_view, dtype=dtype, order="C"), strides=[row_stride*itemsize, col_stride*itemsize]))

@cython.boundscheck(False)
cdef np.ndarray[char, ndim=2] ndarray_copy_bool_F(const bool *data, long rows, long cols, long row_stride, long col_stride):
    cdef bool[::1,:] mem_view = <bool[:rows:1,:cols]>data
    dtype = 'uint8'
    cdef int itemsize = np.dtype(dtype).itemsize
    return np.copy(as_strided(np.asarray(mem_view, dtype=dtype, order="F"), strides=[row_stride*itemsize, col_stride*itemsize]))


@cython.boundscheck(False)
cdef np.ndarray[short, ndim=2] ndarray_short_C(short *data, long rows, long cols, long row_stride, long col_stride):
    cdef short[:,:] mem_view = <short[:rows,:cols]>data
    dtype = 'short'
    cdef int itemsize = np.dtype(dtype).itemsize
    return as_strided(np.asarray(mem_view, dtype=dtype, order="C"), strides=[row_stride*itemsize, col_stride*itemsize])

@cython.boundscheck(False)
cdef np.ndarray[short, ndim=2] ndarray_short_F(short *data, long rows, long cols, long row_stride, long col_stride):
    cdef short[::1,:] mem_view = <short[:rows:1,:cols]>data
    dtype = 'short'
    cdef int itemsize = np.dtype(dtype).itemsize
    return as_strided(np.asarray(mem_view, dtype=dtype, order="F"), strides=[row_stride*itemsize, col_stride*itemsize])

@cython.boundscheck(False)
cdef np.ndarray[short, ndim=2] ndarray_copy_short_C(const short *data, long rows, long cols, long row_stride, long col_stride):
    cdef short[:,:] mem_view = <short[:rows,:cols]>data
    dtype = 'short'
    cdef int itemsize = np.dtype(dtype).itemsize
    return np.copy(as_strided(np.asarray(mem_view, dtype=dtype, order="C"), strides=[row_stride*itemsize, col_stride*itemsize]))

@cython.boundscheck(False)
cdef np.ndarray[short, ndim=2] ndarray_copy_short_F(const short *data, long rows, long cols, long row_stride, long col_stride):
    cdef short[::1,:] mem_view = <short[:rows:1,:cols]>data
    dtype = 'short'
    cdef int itemsize = np.dtype(dtype).itemsize
    return np.copy(as_strided(np.asarray(mem_view, dtype=dtype, order="F"), strides=[row_stride*itemsize, col_stride*itemsize]))




@cython.boundscheck(False)
cdef np.ndarray[long, ndim=2] ndarray_long_C(long *data, long rows, long cols, long row_stride, long col_stride):
    cdef long[:,:] mem_view = <long[:rows,:cols]>data
    dtype = 'long'
    cdef int itemsize = np.dtype(dtype).itemsize
    return as_strided(np.asarray(mem_view, dtype=dtype, order="C"), strides=[row_stride*itemsize, col_stride*itemsize])

@cython.boundscheck(False)
cdef np.ndarray[long, ndim=2] ndarray_long_F(long *data, long rows, long cols, long row_stride, long col_stride):
    cdef long[::1,:] mem_view = <long[:rows:1,:cols]>data
    dtype = 'long'
    cdef int itemsize = np.dtype(dtype).itemsize
    return as_strided(np.asarray(mem_view, dtype=dtype, order="F"), strides=[row_stride*itemsize, col_stride*itemsize])

@cython.boundscheck(False)
cdef np.ndarray[long, ndim=2] ndarray_copy_long_C(const long *data, long rows, long cols, long row_stride, long col_stride):
    cdef long[:,:] mem_view = <long[:rows,:cols]>data
    dtype = 'long'
    cdef int itemsize = np.dtype(dtype).itemsize
    return np.copy(as_strided(np.asarray(mem_view, dtype=dtype, order="C"), strides=[row_stride*itemsize, col_stride*itemsize]))

@cython.boundscheck(False)
cdef np.ndarray[long, ndim=2] ndarray_copy_long_F(const long *data, long rows, long cols, long row_stride, long col_stride):
    cdef long[::1,:] mem_view = <long[:rows:1,:cols]>data
    dtype = 'long'
    cdef int itemsize = np.dtype(dtype).itemsize
    return np.copy(as_strided(np.asarray(mem_view, dtype=dtype, order="F"), strides=[row_stride*itemsize, col_stride*itemsize]))