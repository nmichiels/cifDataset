
class Dataset(object):
    """A generic class to represent training datasets. It can contain a multichannel dataset of images."""

    def __init__(self):
        self._num_examples = 0
        self._num_classes = 0
        self._num_channels = 0
        self._epochs_done = 0
        self._index_in_epoch = 0

      
    def nextBatch(self, batch_size, image_size = None):
        """An overload of this function should return the next `batch_size` images of this dataset."""
        raise NotImplementedError()

    def nextBatch_withmask(self, batch_size, image_size = None):
        """An overload of this function should return the next `batch_size` images of this dataset, as well as its mask."""
        raise NotImplementedError()

    def nextImage(self):
        """An overload of this function should return the next image of this dataset."""
        return self.nextBatch(1)

    def nextImage_withmask(self):
        """An overload of this function should return the next image of this dataset, as well as its mask."""
        return self.nextBatch_withmask(1)

    def get_batch(self, idx, batch_size, image_size):
        """An overload of this function should return the next `batch_size` images at position `idx` of this dataset."""
        raise NotImplementedError()
        
    def get(self, index, image_size = None):
        """An overload of this function should return the images at position `idx` of this dataset."""
        raise NotImplementedError()

    def skip(self, n):
        """This function will skip `n` images of this dataset."""
        self._index_in_epoch += n
        if self._index_in_epoch > self._num_examples:
            self._epochs_done += 1
            self._index_in_epoch = 0

    def reset(self):
        """This function reset the dataset and will restart at the first image."""
        self._index_in_epoch = 0
        self._epochs_done = 0

    def maxIntensityOfChannel(self, channel):
        """An overload of this function should return the maximum intensity of the entire dataset for specific `channel`."""
        raise NotImplementedError()

    def minIntensityOfChannel(self, channel):
        """An overload of this function should return the minimum intensity of the entire dataset for specific `channel`."""
        raise NotImplementedError()
        

    @property
    def num_classes(self):
        """Returns the number of classes in this dataset."""
        return self._num_classes

    @property
    def num_channels(self):
        """Returns the number of channels in this dataset."""
        return self._num_channels

    @property
    def num_examples(self):
        """Returns the number of images in this dataset."""
        return self._num_examples

    @property
    def epochs_done(self):
        """Returns the amount of epochs, i.e. the number of times iterated over the entire dataset."""
        return self._epochs_done

    # check if end of dataset
    def eod(self):
        """Returns if the end of the dataset is reached, i.e. iterated over all the images of the dataset."""
        if (self._index_in_epoch >= self._num_examples or self._epochs_done > 0):
            return True
        else:
            return False
    
        
    def __del__(self):
        pass