import numpy as np
from .dataset import Dataset

class NPDataset(Dataset):

  def __init__(self, images, labels):
    Dataset.__init__(self)

    self._num_examples = images.shape[0]
    self._num_classes = labels.shape[1]
    self._num_channels = images.shape[3]


    self._images = images
    self._labels = labels
    

  @property
  def images(self):
    return self._images

  @property
  def labels(self):
    return self._labels
          
  def nextBatch(self, batch_size, image_size = None):
    """Return the next `batch_size` examples from this data set."""
    start = self._index_in_epoch
    self._index_in_epoch += batch_size
    end = self._index_in_epoch
    
    if end > self._num_examples:
      end = self._num_examples
      self._epochs_done += 1
      self._index_in_epoch = 0

    return self._images[start:end], self._labels[start:end]
  
  def maxIntensityOfChannel(self, channel):
    if channel >= self.num_channels:
      raise Exception('Channel %d does not exist, num channels is %d'%(channel, self.num_channels))
    return np.max(self.images[:,:,:,channel])

  def minIntensityOfChannel(self, channel):
    if channel >= self.num_channels:
      raise Exception('Channel %d does not exist, num channels is %d'%(channel, self.num_channels))
    return np.min(self.images[:,:,:,channel])


  def nextImage(self):
    return self.nextBatch(1)   

  def get_batch(self, idx, batch_size, image_size):

    start = idx*batch_size
    end = (idx+1)*batch_size
    if end > self._num_examples:
        end = self._num_examples
     
    return self._images[start:end], self._labels[start:end]

  def permutate(self):
    p = np.random.permutation(self._images.shape[0])
    self._images = self._images[p]
    self._labels = self._labels[p]