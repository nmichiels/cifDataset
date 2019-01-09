import h5py


class HDF5Dataset(object):
    
    def __init__(self, hdf5File):
        print('Initializing Dataset: ' + hdf5File)
        self._hdf5 = h5py.File(hdf5File, "r")
        # images = len(rawDataset.keys())
        # print (repr(images))

        self._dsetImg = None 
        self._dsetMask = None
        self._nimages = 0
        self._nchannels = 0

        if "image" in self._hdf5.keys():
            self._dsetImg = self._hdf5["image"]
            self._nimages = self._dsetImg.len()
            self._nchannels = self._dsetImg.shape[3]
        if "mask" in self._hdf5.keys():
            self._dsetMask = self._hdf5["mask"]
   
        print("Image Count: " + repr(self._nimages))
        print("Channel Count: " + repr(self._nchannels))
        if not self._dsetMask:
            print("No mask info found.")
        self._current_image_ID = 0

    def nextBatch(self, batch_size):

        print ("Next batch")
        batch = self._dsetImg[self._current_image_ID:self._current_image_ID+batch_size,]

        batch_mask = None
        if (self._dsetMask):
            batch_mask = self._dsetMask[self._current_image_ID:self._current_image_ID+batch_size,]
        self._current_image_ID += batch_size
        return batch, batch_mask
        # todo

    def nextImage(self):
        
        image = self._dsetImg[self._current_image_ID]

        mask = None
        if (self._dsetMask):
            mask = self._dsetMask[self._current_image_ID]
        # mask = self._reader.read(series=self._current_image_ID+1)
        self._current_image_ID += 1
        return image, mask

    def skip(self, n):
        self._current_image_ID += n*2
        
    # set dataset back to first image
    def reset(self):
        self._current_image_ID = 0

    def numberOfImages(self):
        return self._nimages

    def numberOfChannels(self):
        return self._nchannels

    # check if end of dataset
    def eod(self):
        if (self._current_image_ID >= self._nimages):
            return True
        else:
            return False