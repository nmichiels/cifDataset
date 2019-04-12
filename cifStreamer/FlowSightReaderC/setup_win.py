from distutils.core import setup
from distutils.extension import Extension
import numpy as np
from Cython.Build import cythonize

__package_name__ = "FlowSightReaderC"

eigen_include_dir = "E:/Libraries/eigen"

extensions = [
    Extension("FlowSightReaderC.conversion", ["FlowSightReaderC/conversion.pyx"],
              include_dirs=[np.get_include(), eigen_include_dir],
              language="c++",
              extra_compile_args=["-std=c++11"],
              extra_link_args=[]
              ),
    Extension("FlowSightReaderC.eigen", ["FlowSightReaderC/eigen.pyx"],
              include_dirs=[np.get_include(), eigen_include_dir],
              language="c++",
              extra_compile_args=["-std=c++11"],
              extra_link_args=[]
              ),
    Extension("FlowSightReaderC.core", ["FlowSightReaderC/core.pyx", "FlowSightReaderC/FlowSightReaderC.cpp"],
              include_dirs=[np.get_include(), eigen_include_dir],
              language="c++",
              extra_compile_args=["-std=c++11", "-march=native", "-mtune=native", "-O3"],#, "-ftree-vectorize", "-fopt-info-all=vect.all"],#, "-fopt-info-vec-missed" ,"-fopt-info" ],
              extra_link_args=[],
              #libraries=["DiffMEM"],
              #library_dirs=[diffmem_library_path],
                ),

]

dist = setup(
    name=__package_name__,
    version="0.01",
    description="FlowSightParserC",
    author="Nick Michiels",
    author_email="nick.michiels@uhasselt.be",
    ext_modules=cythonize(extensions),#, gdb_debug=True),
    packages=[__package_name__], requires=['numpy', 'Cython']
)
