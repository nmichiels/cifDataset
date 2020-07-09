"""
This module allows the user to convert a dataset of tiff files to a hdf5 dataset.
The main function will call convertTIFF2HDF5() and requires the same input parameters.
"""


from .hdf5Dataset import HDF5Dataset
from .tiffDataset import TiffDataset
# from .cifDatasetBioformats import CIFDataset
from .dataPreparation import pad_or_crop,center_crop_pad

import numpy as np
import h5py
import sys



def convertTIFF2HDF5(inputPattern, maskPattern, outputFile, img_size,  maxImages = None, masked = False, channelsString='', batchSize=1, chunkSize=10):
    """
    This function converts a set of tiff files with inputPattern to a hdf5 dataset (`outputFile`).
    Masks are exported as separate dataset in HDF5 output.
    All images are cropped, centered and padded to an output resolution of `img_size`.

    Args:
        inputPattern (str): Directory and pattern of tiff images (e.g. `images_%d.tiff`).
        maskPattern (str): Directory and pattern of tiff masks
        outputFile (str): Output hdf5 file.
        img_size (int): Target resolution of the images.  All images are cropped, centered and padded to an output resolution of `img_size`.
        maxImages (int, optional): Number of images to convert.
        masked (bool, optional): Apply mask to output file. Remove all pixels outside of mask.
        channelsString (str, optional): Channels to keep in the output dataset. (E.g `0,2,3,5`).
        batchSize (int, optional): Specify batch size of HDF5 file format.
        chunkSize (int, optional): Specify chunk size of HDF5 file format.
    """

    try:
        
        print('Loading TIFF dataset:  ' + inputPattern, ' with mask', maskPattern)
        dataset = TiffDataset(inputPattern, maskPattern)
        dataset.reset()

        channels = np.arange(dataset.num_channels)
        if (channelsString):
            channels = channelsString.split(",")
            channels = np.asarray(channels, dtype=int, order=None)
        numChannels = channels.shape[0]
        imageCounter = 0


        hdf5 = h5py.File(outputFile, "w")
        # dsetImg = hdf5.create_dataset("image", (0, img_size,img_size,numChannels), compression='gzip', compression_opts=4, maxshape=(None,img_size,img_size,numChannels), chunks=(chunkSize,img_size,img_size,numChannels))
        # dsetMsk = hdf5.create_dataset("mask", (0, img_size,img_size,numChannels), compression='gzip', compression_opts=4, maxshape=(None,img_size,img_size,numChannels), chunks=(chunkSize,img_size,img_size,numChannels))
        dsetImg = hdf5.create_dataset("image", (0, img_size,img_size,numChannels), maxshape=(None,img_size,img_size,numChannels), chunks=(chunkSize,img_size,img_size,numChannels))
        dsetMsk = hdf5.create_dataset("mask", (0, img_size,img_size,numChannels),  maxshape=(None,img_size,img_size,numChannels), chunks=(chunkSize,img_size,img_size,numChannels))


        i = 1
        imgNumber = 0
        while (not dataset.eod()):
            if maxImages is not None:
                if imgNumber >= maxImages:
                    break
            imgNumber = imgNumber + 1
            image, mask = dataset.nextImage_withmask()
    
            if (channelsString):
                image = image[:,:,channels]
                mask = mask[:,:,channels]
      
            centerChannel = 0
            # use mask of first channel (bright field) to center the data
            uniqueVals, uniqueCount = np.unique(mask[:,:,centerChannel], return_counts = True)
            if uniqueCount.shape[0] == 1: # only black pixels in mask, no reference to center the cell
                print("skipping ", imageCounter)
                imageCounter += 1
                continue

            blobIntensity = uniqueVals[np.argmax(uniqueCount[1:]) + 1] # ignore black pixels in mask
            image, mask = center_crop_pad(image, mask, centerChannel, blobIntensity, img_size)

            if masked:
                image[mask == 0] = 0.0
            
            dsetImg.resize(dsetImg.shape[0]+1, axis=0)  
            dsetImg[-batchSize:] = image
            dsetMsk.resize(dsetMsk.shape[0]+1, axis=0)  
            dsetMsk[-batchSize:] = mask

            imageCounter += batchSize
            hdf5.flush()
            # if (i % 100 == 0):
            sys.stdout.write("\rConverting image %i / %i" % (i,dataset.num_examples))
            sys.stdout.flush()
            i = i+1


    except RuntimeError as err:
        print("Converting CIF file to hdf5 failed.")
        print("RuntimeError error: {0}".format(err))
    finally:
        hdf5.close()
        print("Creating HDF5 file finished.")



def convertTIFF2HDF5_nomask(inputPattern, outputFile, img_size, channelsString='', batchSize=1, chunkSize=10):
    """
    This function converts a set of tiff files with inputPattern to a hdf5 dataset (`outputFile`).
    Masks of cif file are not exported.
    All images are cropped, centered and padded to an output resolution of `img_size`.

    Args:
        inputPattern (str): Directory and pattern of tiff images (e.g. `images_%d.tiff`).
        outputFile (str): Output hdf5 file.
        img_size (int): Target resolution of the images.  All images are cropped, centered and padded to an output resolution of `img_size`.
        channelsString (str, optional): Channels to keep in the output dataset. (E.g `0,2,3,5`).
        batchSize (int, optional): Specify batch size of HDF5 file format.
        chunkSize (int, optional): Specify chunk size of HDF5 file format.
    """

    try:
        print('Loading TIFF dataset with pattern:' + inputPattern)
        dataset = TiffDataset(inputPattern)
        dataset.reset()

        channels = np.arange(dataset.num_channels)
        if (channelsString):
            channels = channelsString.split(",")
            channels = np.asarray(channels, dtype=int, order=None)
        numChannels = channels.shape[0]
        imageCounter = 0

        hdf5 = h5py.File(outputFile, "w")
        dsetImg = hdf5.create_dataset("image", (0, img_size,img_size,numChannels), compression='gzip', compression_opts=4, maxshape=(None,img_size,img_size,numChannels), chunks=(chunkSize,img_size,img_size,numChannels))
      
        i = 0
        while (not dataset.eod()):
            data = dataset.nextBatch(batchSize, img_size)
            if (channelsString):
                data = data[:,:,:,channels]

            dsetImg.resize(dsetImg.shape[0]+batchSize, axis=0)  
            dsetImg[-batchSize:] = data
        
            imageCounter += batchSize
            i = i+1
            if (i % 50 == 0):
                hdf5.flush()
                sys.stdout.write("\rConverting image %i / %i" % (i,dataset.num_examples))
                sys.stdout.flush()
            
        hdf5.flush()


    except RuntimeError as err:
        print("Converting TIFF file to hdf5 failed.")
        print("RuntimeError error: {0}".format(err))
    finally:
        hdf5.close()
        print("Creating HDF5 file finished.")

        
def __main__():
    import time
    start_time = time.time()
    if (len(sys.argv) < 4 or len(sys.argv) > 5):
        print("Wrong number of input arguments. Usage: python convertTIFF2HDF5 inputTiffPattern output.hdf5 targetSize")
    else:
        if (len(sys.argv) == 5):
            convertTIFF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
        else:
            convertTIFF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == "__main__":
    __main__()

