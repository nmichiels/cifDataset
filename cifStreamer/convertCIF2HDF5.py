from cifDataset import CIFDataset
# from cifDatasetBioformats import CIFDataset
from hdf5Dataset import HDF5Dataset
import h5py
import sys


def convertCIF2HDF5(inputFile, outputFile):
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
            dsetImg = imageGrp.create_dataset("image", data=image, compression='gzip', compression_opts=9)
            dsetMsk = imageGrp.create_dataset("mask", data=mask, compression='gzip', compression_opts=9)
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

def __main__():
    if (len(sys.argv) != 3):
        print("Wrong number of input arguments. Usage: python convertCIF2HDF5 input.cif output.hdf5")
    else:
        convertCIF2HDF5(sys.argv[1], sys.argv[2])
  
# # dataset = CIFDataSet("../05-Aug-2015_A04-noBF.cif")
# # # dataset = HDF5DataSet("test.dhf5")
# # visualizeCIFDataset(dataset)
#convertCIF2HDF5("../../../data/05-Aug-2015_A04-noBF.cif", "../../../data/test3.dhf5")
convertCIF2HDF5("../../../data/20180515_testData/DONOR1714_living single cells_321987.cif", "../../../data/20180515_testData/DONOR1714_living single cells_321987.dhf5")

if __name__ == "__main__":
    __main__()