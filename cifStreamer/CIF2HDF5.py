from .hdf5Dataset import HDF5Dataset
from .cifDataset import CIFDataset
# from .cifDatasetBioformats import CIFDataset
from .dataPreparation import pad_or_crop,center_crop_pad
# from dataset.dataPreparation import pad_or_crop_zero

import numpy as np
import h5py
import sys



def convertCIF2HDF5(inputFile, outputFile, img_size,  maxImages = None, masked = False, channelsString='', batchSize=1, chunkSize=10):
    
    try:
        
        print('Loading ' + inputFile)
        dataset = CIFDataset(inputFile)
        dataset.reset()

        hdf5 = h5py.File(outputFile, "w")
        # grp = hdf5.create_group("raw")

        
        channels = np.arange(dataset.num_channels)
        if (channelsString):
            channels = channelsString.split(",")
            channels = np.asarray(channels, dtype=int, order=None)
        
        numChannels = channels.shape[0]
        print("channels: ", channels)
        print("numChannels:",numChannels)
 

        print(repr(hdf5.name))  
        imageCounter = 0
        # dsetImg = hdf5.create_dataset("image", (0, img_size,img_size,numChannels), compression='gzip', compression_opts=4, maxshape=(None,img_size,img_size,numChannels), chunks=(chunkSize,img_size,img_size,numChannels))
        # dsetMsk = hdf5.create_dataset("mask", (0, img_size,img_size,numChannels), compression='gzip', compression_opts=4, maxshape=(None,img_size,img_size,numChannels), chunks=(chunkSize,img_size,img_size,numChannels))
        dsetImg = hdf5.create_dataset("image", (0, img_size,img_size,numChannels), maxshape=(None,img_size,img_size,numChannels), chunks=(chunkSize,img_size,img_size,numChannels))
        dsetMsk = hdf5.create_dataset("mask", (0, img_size,img_size,numChannels),  maxshape=(None,img_size,img_size,numChannels), chunks=(chunkSize,img_size,img_size,numChannels))


        i = 1
        #while (not dataset.eod()):
        #    data, mask = dataset.nextBatch_withmask(batchSize, img_size)
        #    if (channelsString):
        #        data = data[:,:,:,channels]
        #        mask = mask[:,:,:,channels]
        #    #imageGrp = grp.create_group("cell_" + repr(imageCounter))
        #    #dsetImg = grp.create_dataset("image", data=data, compression='gzip', compression_opts=4)
            
        #    dsetImg.resize(dsetImg.shape[0]+batchSize, axis=0)  
        #    dsetImg[-batchSize:] = data
        #    dsetMsk.resize(dsetMsk.shape[0]+batchSize, axis=0)  
        #    dsetMsk[-batchSize:] = mask
        #    # print(dsetImg.shape)

        #    #dsetMsk = imageGrp.create_dataset("mask", data=mask, compression='gzip', compression_opts=9)
        #    imageCounter += batchSize
        #    hdf5.flush()
        #    if (i % 10 == 0):
        #        sys.stdout.write("\rConverting image %i / %i" % (i,dataset.num_examples))
        #        sys.stdout.flush()
        #    i = i+1

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

            #imageGrp = grp.create_group("cell_" + repr(imageCounter))
            #dsetImg = grp.create_dataset("image", data=data, compression='gzip', compression_opts=4)
            
            dsetImg.resize(dsetImg.shape[0]+1, axis=0)  
            dsetImg[-batchSize:] = image
            dsetMsk.resize(dsetMsk.shape[0]+1, axis=0)  
            dsetMsk[-batchSize:] = mask
            # print(dsetImg.shape)

            #dsetMsk = imageGrp.create_dataset("mask", data=mask, compression='gzip', compression_opts=9)
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



def convertCIF2HDF5_nomask(inputFile, outputFile, img_size, channelsString='', batchSize=1, chunkSize=10):
    
    try:
        
        print('Loading ' + inputFile)
        dataset = CIFDataset(inputFile)
        dataset.reset()

        hdf5 = h5py.File(outputFile, "w")
        # grp = hdf5.create_group("raw")

        
        channels = np.arange(dataset.num_channels)
        if (channelsString):
            channels = channelsString.split(",")
            channels = np.asarray(channels, dtype=int, order=None)
        
        numChannels = channels.shape[0]
        print("channels: ", channels)
        print("numChannels:",numChannels)
 

        print(repr(hdf5.name))  
        imageCounter = 0
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
        print("Converting CIF file to hdf5 failed.")
        print("RuntimeError error: {0}".format(err))
    finally:
        hdf5.close()
        print("Creating HDF5 file finished.")

        
def __main__():
    import time
    start_time = time.time()
    if (len(sys.argv) < 4 or len(sys.argv) > 5):
        print("Wrong number of input arguments. Usage: python convertCIF2HDF5 input.cif output.hdf5 targetSize")
    else:
        if (len(sys.argv) == 5):
            convertCIF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
        else:
            convertCIF2HDF5(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    print("--- %s seconds ---" % (time.time() - start_time))



if __name__ == "__main__":
    __main__()
