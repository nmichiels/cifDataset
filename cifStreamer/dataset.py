
class Dataset(object):
    
    def __init__(self):
        self._num_examples = 0
        self._num_classes = 0
        self._num_channels = 0
        self._epochs_done = 0
        self._index_in_epoch = 0

      
    def nextBatch(self, batch_size, image_size = None):
        raise NotImplementedError()


    def nextImage(self):
        return self.nextBatch(1)

    def skip(self, n):
        self._index_in_epoch += n
        if self._index_in_epoch > self._num_examples:
            self._epochs_done += 1
            self._index_in_epoch = 0

    def reset(self):
            self._index_in_epoch = 0
            self._epochs_done = 0

    @property
    def num_classes(self):
        return self._num_classes

    @property
    def num_channels(self):
        return self._num_channels

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_done(self):
        return self._epochs_done

    # check if end of dataset
    def eod(self):
        if (self._index_in_epoch >= self._num_examples or self._epochs_done > 0):
            return True
        else:
            return False
    
        
    def __del__(self):
        pass