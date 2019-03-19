from cifDataset.cifStreamer.hdf5Dataset import HDF5Dataset
from cifDataset.cifStreamer.cifDataset import CIFDataset
# from cifDataset.cifStreamer.cifDatasetBioformats import CIFDataset
import numpy as np
import h5py
import sys

from dataset.dataPreparation import __pad_or_crop
# from dataset.dataPreparation import __pad_or_crop_zero

def next_batch(dataset, image_size, batch_size):
    
    batch = np.ndarray(shape=(batch_size, image_size,image_size, dataset.numberOfChannels()))
    # batch_mask = np.ndarray(shape=(batch_size, image_size,image_size, dataset.numberOfChannels()))

    for i in range(0,batch_size):
        image = dataset.nextImage_nomask()

        # if (i % 100 == 0):
        #     print(i)

        for channel in range(image.shape[-1]):
            img = image[:,:,channel]

            batch[i][:,:,channel] = __pad_or_crop(img, image_size, 'symmetric')# __pad_or_crop(img, image_size, 'symmetric', constant_values=(0))
            
            # print (imgCropped)
    return batch


def convertCIF2HDF5(inputFile, outputFile, img_size, channelsString='', batchSize=1, chunkSize=10):
    
    try:
        
        print('Loading ' + inputFile)
        dataset = CIFDataset(inputFile)
        dataset.reset()

        hdf5 = h5py.File(outputFile, "w")
        # grp = hdf5.create_group("raw")

        
        channels = np.arange(dataset.numberOfChannels())
        if (channelsString):
            channels = channelsString.split(",")
            channels = np.asarray(channels, dtype=int, order=None)
        
        numChannels = channels.shape[0]
        print("channels: ", channels)
        print("numChannels:",numChannels)
 

        print(repr(hdf5.name))  
        imageCounter = 0
        dsetImg = hdf5.create_dataset("image", (0, img_size,img_size,numChannels), compression='gzip', compression_opts=4, maxshape=(None,img_size,img_size,numChannels), chunks=(chunkSize,img_size,img_size,numChannels))
        # dsetMsk = hdf5.create_dataset("mask", (0, img_size,img_size,numChannels), compression='gzip', compression_opts=4, maxshape=(None,img_size,img_size,numChannels), chunks=(chunkSize,img_size,img_size,numChannels))

        i = 0
        while (not dataset.eod()):
            data = next_batch(dataset, img_size, batchSize)
            if (channelsString):
                data = data[:,:,:,channels]
            #imageGrp = grp.create_group("cell_" + repr(imageCounter))
            #dsetImg = grp.create_dataset("image", data=data, compression='gzip', compression_opts=4)
            
            dsetImg.resize(dsetImg.shape[0]+batchSize, axis=0)  
            dsetImg[-batchSize:] = data
            # dsetMsk.resize(dsetMsk.shape[0]+batchSize, axis=0)  
            # dsetMsk[-batchSize:] = mask
            # print(dsetImg.shape)

            #dsetMsk = imageGrp.create_dataset("mask", data=mask, compression='gzip', compression_opts=9)
            
            imageCounter += batchSize
            i = i+1
            if (i % 50 == 0):
                hdf5.flush()
                sys.stdout.write("\rConverting image %i / %i" % (i,dataset.numberOfImages()/2))
                sys.stdout.flush()
            
        hdf5.flush()



    except RuntimeError as err:
        print("Converting CIF file to hdf5 failed.")
        print("RuntimeError error: {0}".format(err))
    finally:
        hdf5.close()
        print("Creating HDF5 file finished.")

def __main__():
    if (len(sys.argv) < 4 or len(sys.argv) > 5):
        print("Wrong number of input arguments. Usage: python convertCIF2HDF5 input.cif output.hdf5 targetSize")
    else:
        if (len(sys.argv) == 5):
            convertCIF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
        else:
            convertCIF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]))
  
# # dataset = CIFDataSet("../05-Aug-2015_A04-noBF.cif")
# # # dataset = HDF5DataSet("test.hdf5")
# # visualizeCIFDataset(dataset)
#convertCIF2HDF5("../../../data/05-Aug-2015_A04-noBF.cif", "../../../data/test3.hdf5")


# convertCIF2HDF5("../data/20180424 Labeled cells/DONOR1714 CD8+ T cells.cif", "../data/20180424 Labeled cells/DONOR1714 CD8+ T cells_40x40.hdf5")
#convertCIF2HDF5("../data/20180424 Labeled cells/d1665_Neg cells_Living.cif", "../data/20180424 Labeled cells/d1665_Neg cells_Living_40x40.hdf5")
# convertCIF2HDF5("../data/20180515_testData/DONOR1665_living cells_9670.cif", "../data/20180515_testData/DONOR1665_living cells_9670_40x40.hdf5", img_size=40)



if __name__ == "__main__":
    __main__()
