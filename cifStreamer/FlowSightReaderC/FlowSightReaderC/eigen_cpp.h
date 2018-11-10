#include <stdexcept>
#include "conversion_api.h"


#include "matrixVector.h"

#ifndef EIGEN_CPP
#define EIGEN_CPP


template <typename T>
PyArrayObject *_ndarray_view(T *data, long rows, long cols, bool is_row_major, long outer_stride=0, long inner_stride=0);

template <typename T>
PyArrayObject *_ndarray_copy(const T *data, long rows, long cols, bool is_row_major, long outer_stride=0, long inner_stride=0);

template <>
inline PyArrayObject *_ndarray_view<double>(double *data, long rows, long cols, bool is_row_major, long outer_stride, long inner_stride) {
    if (is_row_major) {
        // Eigen row-major mode: row_stride=outer_stride, and col_stride=inner_stride
        // If no stride is given, the row_stride is set to the number of columns.
        return ndarray_double_C(data, rows, cols, outer_stride>0?outer_stride:cols, inner_stride>0?inner_stride:1);
    } else {
        // Eigen column-major mode: row_stride=outer_stride, and col_stride=inner_stride
        // If no stride is given, the cow_stride is set to the number of rows.
        return ndarray_double_F(data, rows, cols, inner_stride>0?inner_stride:1, outer_stride>0?outer_stride:rows);
    }
}

template <>
inline PyArrayObject *_ndarray_copy<double>(const double *data, long rows, long cols, bool is_row_major, long outer_stride, long inner_stride) {
    if (is_row_major)
        return ndarray_copy_double_C(data, rows, cols, outer_stride>0?outer_stride:cols, inner_stride>0?inner_stride:1);
    else
        return ndarray_copy_double_F(data, rows, cols, inner_stride>0?inner_stride:1, outer_stride>0?outer_stride:rows);
}


template <>
inline PyArrayObject *_ndarray_view<float>(float *data, long rows, long cols, bool is_row_major, long outer_stride, long inner_stride) {
    if (is_row_major) {
        // Eigen row-major mode: row_stride=outer_stride, and col_stride=inner_stride
        // If no stride is given, the row_stride is set to the number of columns.
        return ndarray_float_C(data, rows, cols, outer_stride>0?outer_stride:cols, inner_stride>0?inner_stride:1);
    } else {
        // Eigen column-major mode: row_stride=outer_stride, and col_stride=inner_stride
        // If no stride is given, the cow_stride is set to the number of rows.
        return ndarray_float_F(data, rows, cols, inner_stride>0?inner_stride:1, outer_stride>0?outer_stride:rows);
    }
}

template <>
inline PyArrayObject *_ndarray_copy<float>(const float *data, long rows, long cols, bool is_row_major, long outer_stride, long inner_stride) {
    if (is_row_major)
        return ndarray_copy_float_C(data, rows, cols, outer_stride>0?outer_stride:cols, inner_stride>0?inner_stride:1);
    else
        return ndarray_copy_float_F(data, rows, cols, inner_stride>0?inner_stride:1, outer_stride>0?outer_stride:rows);
}


template <>
inline PyArrayObject *_ndarray_view<int>(int *data, long rows, long cols, bool is_row_major, long outer_stride, long inner_stride) {
    if (is_row_major) {
        // Eigen row-major mode: row_stride=outer_stride, and col_stride=inner_stride
        // If no stride is given, the row_stride is set to the number of columns.
        return ndarray_int_C(data, rows, cols, outer_stride>0?outer_stride:cols, inner_stride>0?inner_stride:1);
    } else {
        // Eigen column-major mode: row_stride=outer_stride, and col_stride=inner_stride
        // If no stride is given, the cow_stride is set to the number of rows.
        return ndarray_int_F(data, rows, cols, inner_stride>0?inner_stride:1, outer_stride>0?outer_stride:rows);
    }
}

template <>
inline PyArrayObject *_ndarray_copy<int>(const int *data, long rows, long cols, bool is_row_major, long outer_stride, long inner_stride) {
    if (is_row_major)
        return ndarray_copy_int_C(data, rows, cols, outer_stride>0?outer_stride:cols, inner_stride>0?inner_stride:1);
    else
        return ndarray_copy_int_F(data, rows, cols, inner_stride>0?inner_stride:1, outer_stride>0?outer_stride:rows);
}

template <>
inline PyArrayObject *_ndarray_view<bool>(bool *data, long rows, long cols, bool is_row_major, long outer_stride, long inner_stride) {
    if (is_row_major) {
        // Eigen row-major mode: row_stride=outer_stride, and col_stride=inner_stride
        // If no stride is given, the row_stride is set to the number of columns.
        return ndarray_bool_C(data, rows, cols, outer_stride>0?outer_stride:cols, inner_stride>0?inner_stride:1);
    } else {
        // Eigen column-major mode: row_stride=outer_stride, and col_stride=inner_stride
        // If no stride is given, the cow_stride is set to the number of rows.
        return ndarray_bool_F(data, rows, cols, inner_stride>0?inner_stride:1, outer_stride>0?outer_stride:rows);
    }
}

template <>
inline PyArrayObject *_ndarray_copy<bool>(const bool *data, long rows, long cols, bool is_row_major, long outer_stride, long inner_stride) {
    if (is_row_major)
        return ndarray_copy_bool_C(data, rows, cols, outer_stride>0?outer_stride:cols, inner_stride>0?inner_stride:1);
    else
        return ndarray_copy_bool_F(data, rows, cols, inner_stride>0?inner_stride:1, outer_stride>0?outer_stride:rows);
}

template <>
inline PyArrayObject *_ndarray_view<short>(short *data, long rows, long cols, bool is_row_major, long outer_stride, long inner_stride) {
    if (is_row_major) {
        // Eigen row-major mode: row_stride=outer_stride, and col_stride=inner_stride
        // If no stride is given, the row_stride is set to the number of columns.
        return ndarray_short_C(data, rows, cols, outer_stride>0?outer_stride:cols, inner_stride>0?inner_stride:1);
    } else {
        // Eigen column-major mode: row_stride=outer_stride, and col_stride=inner_stride
        // If no stride is given, the cow_stride is set to the number of rows.
        return ndarray_short_F(data, rows, cols, inner_stride>0?inner_stride:1, outer_stride>0?outer_stride:rows);
    }
}

template <>
inline PyArrayObject *_ndarray_copy<short>(const short *data, long rows, long cols, bool is_row_major, long outer_stride, long inner_stride) {
    if (is_row_major)
        return ndarray_copy_short_C(data, rows, cols, outer_stride>0?outer_stride:cols, inner_stride>0?inner_stride:1);
    else
        return ndarray_copy_short_F(data, rows, cols, inner_stride>0?inner_stride:1, outer_stride>0?outer_stride:rows);
}

template <typename Derived>
inline PyArrayObject *ndarray(Eigen::PlainObjectBase<Derived> &m) {
    import_FlowSightReaderC__conversion();
    return _ndarray_view(m.data(), m.rows(), m.cols(), m.IsRowMajor);
}
// If C++11 is available, check if m is an r-value reference, in
// which case a copy should always be made
#if __cplusplus >= 201103L
template <typename Derived>
inline PyArrayObject *ndarray(Eigen::PlainObjectBase<Derived> &&m) {
    import_FlowSightReaderC__conversion();
    return _ndarray_copy(m.data(), m.rows(), m.cols(), m.IsRowMajor);
}
#endif
template <typename Derived>
inline PyArrayObject *ndarray(const Eigen::PlainObjectBase<Derived> &m) {
    import_FlowSightReaderC__conversion();
    return _ndarray_copy(m.data(), m.rows(), m.cols(), m.IsRowMajor);
}
template <typename Derived>
inline PyArrayObject *ndarray_view(Eigen::PlainObjectBase<Derived> &m) {
    import_FlowSightReaderC__conversion();
    return _ndarray_view(m.data(), m.rows(), m.cols(), m.IsRowMajor);
}
template <typename Derived>
inline PyArrayObject *ndarray_view(const Eigen::PlainObjectBase<Derived> &m) {
    import_FlowSightReaderC__conversion();
    return _ndarray_view(const_cast<typename Derived::Scalar*>(m.data()), m.rows(), m.cols(), m.IsRowMajor);
}
template <typename Derived>
inline PyArrayObject *ndarray_copy(const Eigen::PlainObjectBase<Derived> &m) {
    import_FlowSightReaderC__conversion();
    return _ndarray_copy(m.data(), m.rows(), m.cols(), m.IsRowMajor);
}
template <typename Derived>
inline PyArrayObject *ndarray_view(const Eigen::Ref<Derived> &m) {
    import_FlowSightReaderC__conversion();
    return _ndarray_view(const_cast<typename Derived::Scalar*>(m.data()), m.rows(), m.cols(), m.IsRowMajor);
}
template <typename Derived>
inline PyArrayObject *ndarray_copy(const Eigen::Ref<Derived> &m) {
    import_FlowSightReaderC__conversion();
    return _ndarray_copy(m.data(), m.rows(), m.cols(), m.IsRowMajor);
}


template <typename Derived, int MapOptions, typename Stride>
inline PyArrayObject *ndarray(Eigen::Map<Derived, MapOptions, Stride> &m) {
    import_FlowSightReaderC__conversion();
    return _ndarray_view(m.data(), m.rows(), m.cols(), m.IsRowMajor, m.outerStride(), m.innerStride());
}
template <typename Derived, int MapOptions, typename Stride>
inline PyArrayObject *ndarray(const Eigen::Map<Derived, MapOptions, Stride> &m) {
    import_FlowSightReaderC__conversion();
    // Since this is a map, we assume that ownership is correctly taken care
    // of, and we avoid taking a copy
    return _ndarray_view(const_cast<typename Derived::Scalar*>(m.data()), m.rows(), m.cols(), m.IsRowMajor, m.outerStride(), m.innerStride());
}
template <typename Derived, int MapOptions, typename Stride>
inline PyArrayObject *ndarray_view(Eigen::Map<Derived, MapOptions, Stride> &m) {
    import_FlowSightReaderC__conversion();
    return _ndarray_view(m.data(), m.rows(), m.cols(), m.IsRowMajor, m.outerStride(), m.innerStride());
}
template <typename Derived, int MapOptions, typename Stride>
inline PyArrayObject *ndarray_view(const Eigen::Map<Derived, MapOptions, Stride> &m) {
    import_FlowSightReaderC__conversion();
    return _ndarray_view(const_cast<typename Derived::Scalar*>(m.data()), m.rows(), m.cols(), m.IsRowMajor, m.outerStride(), m.innerStride());
}
template <typename Derived, int MapOptions, typename Stride>
inline PyArrayObject *ndarray_copy(const Eigen::Map<Derived, MapOptions, Stride> &m) {
    import_FlowSightReaderC__conversion();
    return _ndarray_copy(m.data(), m.rows(), m.cols(), m.IsRowMajor, m.outerStride(), m.innerStride());
}

template <typename MatrixType,
          int _MapOptions = Eigen::Unaligned,
          typename _StrideType=Eigen::Stride<0,0> >
class MapBase: public Eigen::Map<MatrixType, _MapOptions, _StrideType> {
public:
    typedef Eigen::Map<MatrixType, _MapOptions, _StrideType> Base;
    typedef typename Base::Scalar Scalar;

    MapBase(Scalar* data,
            long rows,
            long cols,
            _StrideType stride=_StrideType())
        : Base(data,
               // If both dimensions are dynamic or dimensions match, accept dimensions as they are
               ((Base::RowsAtCompileTime==Eigen::Dynamic && Base::ColsAtCompileTime==Eigen::Dynamic) ||
                (Base::RowsAtCompileTime==rows && Base::ColsAtCompileTime==cols))
               ? rows
               // otherwise, test if swapping them makes them fit
               : ((Base::RowsAtCompileTime==cols || Base::ColsAtCompileTime==rows)
                  ? cols
                  : rows),
               ((Base::RowsAtCompileTime==Eigen::Dynamic && Base::ColsAtCompileTime==Eigen::Dynamic) ||
                (Base::RowsAtCompileTime==rows && Base::ColsAtCompileTime==cols))
               ? cols
               : ((Base::RowsAtCompileTime==cols || Base::ColsAtCompileTime==rows)
                  ? rows
                  : cols),
               stride
            )  {}
};

#include <iostream>

template <typename MatrixType>
class Map: public MapBase<MatrixType> {
public:
    typedef MapBase<MatrixType> Base;
    typedef typename MatrixType::Scalar Scalar;

    Map()
        : Base(NULL, 0, 0) {
    }

    Map(Scalar *data, long rows, long cols)
        : Base(data, rows, cols) {}

    Map(PyArrayObject *object)
        : Base((PyObject*)object == Py_None? NULL: (Scalar *)object->data,
               // ROW: If array is in row-major order, transpose
               (PyObject*)object == Py_None? 0 :
               (PyArray_IS_C_CONTIGUOUS(object)
                ? object->dimensions[0] : ((object->nd == 1)
                   ? 1  // ROW: If 1D row-major numpy array, set to 1 (row vector)
                   : object->dimensions[1])),
               // COLUMN: If array is in row-major order: transpose
               (PyObject*)object == Py_None? 0 :
               (PyArray_IS_C_CONTIGUOUS(object)
                ? ((object->nd == 1)
                   ? 1  // COLUMN: If 1D col-major numpy array, set to length (column vector)
                   : object->dimensions[1])
								: object->dimensions[0])) {

        if (((PyObject*)object != Py_None) && !PyArray_ISONESEGMENT(object))
            throw std::invalid_argument("Numpy array must be a in one contiguous segment to be able to be transferred to a Eigen Map.");
    }

    Map &operator=(const Map &other) {
        // Replace the memory that we point to (not a memory allocation)
        new (this) Map(const_cast<Scalar*>(other.data()),
                       other.rows(),
                       other.cols());
        return *this;
    }

    operator Base() const {
        return static_cast<Base>(*this);
    }

    operator Base&() const {
        return static_cast<Base&>(*this);
    }

    operator MatrixType() const {
        return MatrixType(static_cast<Base>(*this));
    }
};
#endif
