import h5py


class HDF5Dataset(object):
    
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