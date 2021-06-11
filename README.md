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


## Usage

### Supported datasets
Different types of datasets can be instantiated:
- **cifDataset**: Loading cif or rif files using our fast FloxSighReaderC plugin. Images or batches can be streamed from file.
- **cifDatasetBioformats**: Loading cif or rif using the slower Bioformats java plugin. This Dataset requires additional python dependencies: `pip install javabridge bioformats`
- **hdf5Dataset**: Loading hdf5 datasets. The dataset contains of images and masks extracted from a cif or rif file. Images or batches can be streamed from file.
- **npDataset**: Loading numpy datasets. Here the entire dataset is stored in memory. This only works for small datasets but is the fastest to use for processing.
- **tiffDataset**: Loading a collection of tiff images and tiff masks as dataset. This is usefull when the users exports the Imagestreamer dataset as tiff files instead of cif files.

### Example scripts for converting datasets
Converting a cif dataset to a hdf5 dataset. The images are centered, cropped and padded towards a fixed resolution of 35x35:
```
python .\convertCIFtoHDF5.py .\examples\example.cif .\examples\example.hdf5 35
```

Converting a hdf5 dataset to a numpy dataset. If required the max numer of exported images can be chosen as extra parameter.
```
python .\convertToNumpy.py .\examples\example.hdf5 .\examples\example.npy 35
```

Converting a cif dataset to a hdf5 dataset and applying the underlying mask to remove background. The images are centered, cropped and padded towards a fixed resolution of 35x35:
```
python .\convertCIFtoHDF5_masked.py .\examples\example.cif .\examples\example.hdf5 35
```

Converting a hdf5 dataset to a numpy dataset. The data is augmented with random rotations
```
python .\convertToNumpy_rotInvariant.py .\examples\example.hdf5 .\examples\example.npy 35
```

Converting a collection of tiff images to a hdf5 dataset. The images are centered, cropped and padded towards a fixed resolution of 35x35:
```
python .\convertTIFFtoHDF5.py .\tiffImagesDir\image_%d.tiff .\tiffMasksDir\mask_%d.tiff output.hdf5 35
```

### Visualizing datasets
These visualization require opencv: `pip install opencv-python`

Examples on how to visualize data using opencv are given in this script:
```
python showDataset.py
```

## Acknowledgements
This work is executed in the context of the ImmCyte project (VLAIO R&D project nr: HBC.2016.0889). 

## License
Copyright © 2021, [Nick Michiels](https://www.nickmichiels.com).
Released under the [BSD 3-Clause License](LICENSE).
