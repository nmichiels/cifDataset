A Python parser for *.cif or *.cif files coming from Amnis Image Flow Cytometry.
The project supports the streaming of CIF files for deep learning purposes or converting the cif files to hdf5 datasets.
Decoding the cif files is done in Python and uses C++ functions for decoding images and masks and is no longer dependend on Bioformats and Javabridge.