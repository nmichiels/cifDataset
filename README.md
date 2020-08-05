## CIF Streamer
**CIF Streamer** is a a Python parser for *.cif or *.cif files captured with Amnis Image Flow Cytometry Imagestreamer.
The project supports the streaming of CIF files for deep learning purposes or converting the cif files to hdf5 datasets.
Decoding the cif files is done in Python and uses C++ functions for decoding images and masks and is no longer dependend on Bioformats and Javabridge.

## Installation
The package is tested with Pyton version >= 3.6.

#### First create an activate a Python virtual environment:
```
python -m venv venv
source <venv>/bin/activate (Unix)
.\venv\Scripts\Activate.ps1 (Windows Powershell)
```
#### Install python requirements
```
pip install numpy cython
```

Optionally, if you want to use the tiff datasets convertors, you need to install to following additional requirements:
```
pip install tifffile PIL
```


### Installing the FlowSightReaderC package for cifstreamer:

#### Unix
Install Eigen3 (3.3.6) in the user directory:
```
sudo apt install libeigen3-dev
```

Build FlowSightReaderC python package on Unix
```
cd cifStreamer/FlowSightReaderC
python setup.py build_ext --inplace
```

#### Windows
Install Eigen 3.3.6: <http://bitbucket.org/eigen/eigen/get/3.3.6.tar.bz2>

Open `cifStreamer/FlowSightReaderC/setup_win.py` and change `eigen_include_dir = "D:/libraries/eigen-3.3.6"` to your own installed version.

Build FlowSightReaderC python package on Windows
```
cd cifStreamer/FlowSightReaderC
python setup_win.py build_ext --inplace
```


