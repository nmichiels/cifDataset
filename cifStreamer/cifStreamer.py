import numpy as np
import cv2

import bioformats
import bioformats.formatreader

import javabridge
import javabridge.jutil

import scipy.misc

import h5py

   
class CIFDataSet(object):
    
    def __init__(self, cifFile):
        print('Initializing Dataset: ' + cifFile)
        javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='8G')
        self._reader = bioformats.formatreader.get_image_reader("tmp", path=cifFile)

        self._nimages = javabridge.call(self._reader.metadata, "getImageCount", "()I")
        self._nchannels = javabridge.call(self._reader.metadata, "getChannelCount", "(I)I", 0)
        print("Image Count: " + repr(self._nimages))
        print("Channel Count: " + repr(self._nchannels))

        self._current_image_ID = 0

    def nextBatch(self, batch_size):
        print ("Next batch")
        # todo

    def nextImage(self):
        image = self._reader.read(series=self._current_image_ID)
        mask = self._reader.read(series=self._current_image_ID+1)
        self._current_image_ID += 2
        return image, mask

    # set dataset back to first image
    def reset(self):
        self._current_image_ID = 0

    # check if end of dataset
    def eod(self):
        if (self._current_image_ID >= self._nimages):
            return True
        else:
            return False


    def __del__(self):
        javabridge.kill_vm()


class HDF5DataSet(object):
    
    def __init__(self, hdf5File):
        print('Initializing Dataset: ' + hdf5File)
        self._hdf5 = h5py.File(hdf5File, "r")
        # images = len(rawDataset.keys())
        # print (repr(images))
        self._nimages = len(self._hdf5['raw'].keys())
        self._nchannels = 0
        print("Image Count: " + repr(self._nimages))
        print("Channel Count: " + repr(self._nchannels))

        self._current_image_ID = 0

    def nextBatch(self, batch_size):
        print ("Next batch")
        # todo

    def nextImage(self):
        imageGrp = self._hdf5["raw/cell_" + repr(self._current_image_ID )]
        image = imageGrp['image']
        mask = imageGrp['mask']
        # mask = self._reader.read(series=self._current_image_ID+1)
        self._current_image_ID += 1
        return image, mask

    # set dataset back to first image
    def reset(self):
        self._current_image_ID = 0

    # check if end of dataset
    def eod(self):
        if (self._current_image_ID >= self._nimages):
            return True
        else:
            return False


    def __del__(self):
        javabridge.kill_vm()

def visualizeCIFDataset(dataset):
    dataset.reset()

    imageCounter = 0
    while (not dataset.eod()):

        image, maskImage = dataset.nextImage()
        print ("Image " + repr(imageCounter), image.shape)
       
        for channel in range(image.shape[-1]):#range(0,1):#
            img = image[:,:,channel]
            img /= np.amax(img)
            mask = maskImage[:,:,channel]
            maxMask = np.amax(mask)
            if (maxMask != 0):
                mask /= maxMask
            # else:
                # break
            # scipy.misc.imsave('outfile.jpg', img)

            cv2.imshow('image',img)
            cv2.imshow('mask',mask)
            chr = cv2.waitKey(500)
        
        imageCounter += 1
        if chr==27: # Esc key to exit
            break 

    cv2.destroyAllWindows()




def convertToHDF5(inputFile, outputFile):
    try:
        print('Loading ' + inputFile)
        dataset = CIFDataSet(inputFile)
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
    except javabridge.jutil.JavaException as err:
        print("JavaBridge Error.")
        print("JavaException error: {0}".format(err))
    finally:
        hdf5.close()
        print("Creating HDF5 file finished.")

    # print(image)

# dataset = CIFDataSet("../05-Aug-2015_A04-noBF.cif")
dataset = HDF5DataSet("test.dhf5")
visualizeCIFDataset(dataset)
# convertToHDF5("../05-Aug-2015_A04-noBF.cif", "test.dhf5")
# if __name__ == "__main__":
#     __main__()
