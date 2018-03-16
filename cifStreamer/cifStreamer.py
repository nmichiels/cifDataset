
import numpy as np


from .cifDataset import CIFDataset
from .hdf5Dataset import HDF5Dataset
import h5py





def convertCIFToHDF5(inputFile, outputFile):
    try:
        print('Loading ' + inputFile)
        dataset = CIFDataset(inputFile)
        dataset.reset()

        hdf5 = h5py.File(outputFile, "w")
        grp = hdf5.create_group("raw")
        print(repr(hdf5.name))  
        imageCounter = 0
        while (not dataset.eod()):
            image, mask = dataset.nextImage()

            imageGrp = grp.create_group("cell_" + repr(imageCounter))
            dsetImg = imageGrp.create_dataset("image", data=image)
            dsetMsk = imageGrp.create_dataset("mask", data=mask)
            imageCounter += 1

            if (imageCounter % 100 == 0):
               hdf5.flush()
               print("Image " + repr(imageCounter) + " written to file.")



    except RuntimeError as err:
        print("Converting CIF file to hdf5 failed.")
        print("RuntimeError error: {0}".format(err))
    finally:
        hdf5.close()
        print("Creating HDF5 file finished.")

    # print(image)

# dataset = CIFDataSet("../05-Aug-2015_A04-noBF.cif")
# # dataset = HDF5DataSet("test.dhf5")
# visualizeCIFDataset(dataset)
# # convertToHDF5("../05-Aug-2015_A04-noBF.cif", "test.dhf5")
# # if __name__ == "__main__":
# #     __main__()
