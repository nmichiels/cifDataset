cimport cython
cimport numpy as np

ctypedef fused DenseTypeShort:
    ConstMatrixd
    ConstVecd
    Matrixd
    Vecd
    ConstMatrixi
    ConstVeci
    Matrixi
    Veci
    ConstMatrixb
    ConstVecb
    Matrixb
    Vecb
    ConstMatrixs
    ConstVecs
    Matrixs
    Vecs
    ConstMatrixl
    ConstVecl
    Matrixl
    Vecl
    ConstMatrixf
    ConstVecf
    Matrixf
    Vecf

cdef extern from "eigen_cpp.h":
    cdef cppclass PlainObjectBase:
        pass

    cdef cppclass Map[DenseTypeShort](PlainObjectBase):
        Map() except +
        Map(np.ndarray array) except +

    cdef np.ndarray ndarray_view(PlainObjectBase &)
    cdef np.ndarray ndarray_copy(PlainObjectBase &)
    cdef np.ndarray ndarray(PlainObjectBase &)

cdef extern from "eigen_cpp.h":
    cdef cppclass ConstMatrixd(PlainObjectBase):
        pass

    cdef cppclass ConstVecd(PlainObjectBase):
        pass

    cdef cppclass Matrixd(PlainObjectBase):
        pass

    cdef cppclass Vecd(PlainObjectBase):
        Vecd() except +

    cdef cppclass ConstMatrixb(PlainObjectBase):
        pass

    cdef cppclass ConstVecb(PlainObjectBase):
        pass

    cdef cppclass Matrixb(PlainObjectBase):
        pass

    cdef cppclass Vecb(PlainObjectBase):
        pass

    cdef cppclass ConstMatrixi(PlainObjectBase):
        pass

    cdef cppclass ConstVeci(PlainObjectBase):
        pass

    cdef cppclass Matrixi(PlainObjectBase):
        pass

    cdef cppclass Veci(PlainObjectBase):
        pass

    cdef cppclass ConstMatrixl(PlainObjectBase):
        pass

    cdef cppclass ConstVecl(PlainObjectBase):
        pass

    cdef cppclass Matrixl(PlainObjectBase):
        pass

    cdef cppclass Vecl(PlainObjectBase):
        pass

    cdef cppclass ConstMatrixs(PlainObjectBase):
        pass

    cdef cppclass ConstVecs(PlainObjectBase):
        pass

    cdef cppclass Matrixs(PlainObjectBase):
        pass

    cdef cppclass Vecs(PlainObjectBase):
        pass

    cdef cppclass ConstMatrixf(PlainObjectBase):
        pass

    cdef cppclass ConstVecf(PlainObjectBase):
        pass

    cdef cppclass Matrixf(PlainObjectBase):
        pass

    cdef cppclass Vecf(PlainObjectBase):
        pass

