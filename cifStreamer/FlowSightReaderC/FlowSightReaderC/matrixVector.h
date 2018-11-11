#ifndef MATRIXVECTOR_H
#define MATRIXVECTOR_H

#define EIGEN_DEFAULT_DENSE_INDEX_TYPE int
#define EIGEN_DONT_PARALLELIZE
#include <Eigen/Dense>


typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Matrixd;
typedef Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Matrixf;
typedef Eigen::Array<bool, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Matrixb;
typedef Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Matrixi;
typedef Eigen::Matrix<long, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Matrixl;
typedef Eigen::Matrix<short, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Matrixs;
typedef Eigen::Matrix<double, Eigen::Dynamic, 1> Vecd;
typedef Eigen::Matrix<float, Eigen::Dynamic, 1> Vecf;
typedef Eigen::Array<bool, Eigen::Dynamic, 1> Vecb;
typedef Eigen::Matrix<int, Eigen::Dynamic, 1> Veci;
typedef Eigen::Matrix<long, Eigen::Dynamic, 1> Vecl;
typedef Eigen::Matrix<short, Eigen::Dynamic, 1> Vecs;

typedef const Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> ConstMatrixd;
typedef const Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> ConstMatrixf;
typedef const Eigen::Array<bool, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> ConstMatrixb;
typedef const Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> ConstMatrixi;
typedef const Eigen::Matrix<long, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> ConstMatrixl;
typedef const Eigen::Matrix<short, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> ConstMatrixs;
typedef const Eigen::Matrix<double, Eigen::Dynamic, 1> ConstVecd;
typedef const Eigen::Matrix<float, Eigen::Dynamic, 1> ConstVecf;
typedef const Eigen::Array<bool, Eigen::Dynamic, 1> ConstVecb;
typedef const Eigen::Matrix<int, Eigen::Dynamic, 1> ConstVeci;
typedef const Eigen::Matrix<long, Eigen::Dynamic, 1> ConstVecl;
typedef const Eigen::Matrix<short, Eigen::Dynamic, 1> ConstVecs;

typedef Eigen::Map< Eigen::Matrix<double, Eigen::Dynamic, 1> > MapVecd;
typedef Eigen::Map< Eigen::Matrix<float, Eigen::Dynamic, 1> > MapVecf;
typedef Eigen::Map< Eigen::Array<bool, Eigen::Dynamic, 1> > MapVecb;
typedef Eigen::Map< Eigen::Matrix<int, Eigen::Dynamic, 1> > MapVeci;
typedef Eigen::Map< Eigen::Matrix<long, Eigen::Dynamic, 1> > MapVecl;
typedef Eigen::Map< Eigen::Matrix<short, Eigen::Dynamic, 1> > MapVecs;
typedef Eigen::Map< const Eigen::Matrix<double, Eigen::Dynamic, 1> > ConstMapVecd;
typedef Eigen::Map< const Eigen::Matrix<float, Eigen::Dynamic, 1> > ConstMapVecf;
typedef Eigen::Map< const Eigen::Array<bool, Eigen::Dynamic, 1> > ConstMapVecb;
typedef Eigen::Map< const Eigen::Matrix<int, Eigen::Dynamic, 1> > ConstMapVeci;
typedef Eigen::Map< const Eigen::Matrix<long, Eigen::Dynamic, 1> > ConstMapVecl;
typedef Eigen::Map< const Eigen::Matrix<short, Eigen::Dynamic, 1> > ConstMapVecs;

typedef Eigen::Map< Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > MapMatrixd;
typedef Eigen::Map< Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > MapMatrixf;
typedef Eigen::Map< Eigen::Array<bool, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > MapMatrixb;
typedef Eigen::Map< Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > MapMatrixi;
typedef Eigen::Map< Eigen::Matrix<long, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > MapMatrixl;
typedef Eigen::Map< Eigen::Matrix<short, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > MapMatrixs;
typedef Eigen::Map< const Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > ConstMapMatrixd;
typedef Eigen::Map< const Eigen::Matrix<float, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > ConstMapMatrixf;
typedef Eigen::Map< const Eigen::Array<bool, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > ConstMapMatrixb;
typedef Eigen::Map< const Eigen::Matrix<int, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > ConstMapMatrixi;
typedef Eigen::Map< const Eigen::Matrix<long, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > ConstMapMatrixl;
typedef Eigen::Map< const Eigen::Matrix<short, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> > ConstMapMatrixs;


#endif