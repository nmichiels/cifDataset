import sys
import numpy as np
from cifStreamer.hdf5Dataset import HDF5Dataset

inputFile = "../../data/20190411_healthy_donor_peptide_specific_stimulation/test_ours.hdf5"

dataset = HDF5Dataset(inputFile)
data, masks = dataset.nextBatch_withmask(dataset.num_examples)


doubleData = False
for slice1 in range(data.shape[0]):
    # if slice1%500:
    #     print(slice1)
    for slice2 in range(slice1+1,data.shape[0]):
        theSame = np.array_equal(data[slice1,:,:,:], data[slice2,:,:,:])
        if theSame is True:
            print(slice1, "==", slice2)
            print(data[slice1,:,:,:])
            print("\n")
            print(data[slice2,:,:,:]  )
        doubleData = doubleData or theSame
print("Double data: ", doubleData)
