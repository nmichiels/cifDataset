import builtins
from .dataset import Dataset
import numpy as np
# from .FlowSightParser import FlowSightParser
from .FlowSightParserC import FlowSightParser
from .dataPreparation import pad_or_crop

class CIFDataset(Dataset):
    
    def __init__(self, cifFile, overRuleChannelCount = None):
      
        print('Initializing Dataset: ' + cifFile)
        Dataset.__init__(self)


        self._flowSightParser = FlowSightParser()
        if not self._flowSightParser.loadFile(cifFile):
            print("ERROR (CIFDataset): Could not open file \"", cifFile, "\"")
            self._nimages = 0
            self._nchannels = 0
            return

        self._flowSightParser.loadMetaData(verbose=False, overRuleChannelCount = overRuleChannelCount)

        self._num_examples = int(self._flowSightParser._numCells / 2)
        self._num_channels = self._flowSightParser._channelCount
        
        print("Image Count: " + repr(self._num_examples))
        print("Channel Count: " + repr(self._num_channels))

        self._index_in_epoch = 0
        
    def eod(self):
        if (self._epochs_done > 0):
            return True
        else:
            return False


    # Target resolution required! ==> not all images are of the same size
    def nextBatch_withmask(self, batch_size, image_size):
        # old implementation, requires known number of images in dataset and it is to slow to know up front
        raise NotImplementedError()
        """Return the next `batch_size` examples from this data set."""
        # start = self._index_in_epoch
        # self._index_in_epoch += batch_size
        # end = self._index_in_epoch
        
        # if end > self._num_examples:
        #     end = self._num_examples
        #     self._epochs_done += 1
        #     self._index_in_epoch = 0

        # count = end-start
        # # print("batch:", batch_size)
        # # print("end: ", count)
        # batch = np.ndarray(shape=(count, image_size,image_size, self.num_channels))
        # batch_mask = np.ndarray(shape=(count, image_size,image_size, self.num_channels))

        # for i in range(0,count):
        #     current_image_ID = (self._index_in_epoch-count+i) * 2 +1 

        #     image = self._flowSightParser.openIFDData(current_image_ID , verbose=False)
        #     mask = self._flowSightParser.openIFDData(current_image_ID+1 , verbose=False)

        #     for channel in range(image.shape[-1]):
        #         img = image[:,:,channel]
        #         msk = mask[:,:,channel]

        #         batch[i][:,:,channel] = pad_or_crop(img, image_size, 'symmetric')# pad_or_crop(img, image_size, 'symmetric', constant_values=(0))
        #         batch_mask[i][:,:,channel] = pad_or_crop(msk, image_size, 'symmetric')# pad_or_crop(img, image_size, 'symmetric', constant_values=(0))
        #         # print (imgCropped)
        # return batch, batch_mask



    def nextImage_withmask(self):

        # Calculate the exact position in the cif file
        # *2 because of interleaved image/mask
        # +1 because first element contains only metadata
        current_image_ID = self._index_in_epoch * 2 +1 

        self._index_in_epoch += 1
        #if self._index_in_epoch > self._num_examples:
        #    self._epochs_done += 1
        #    self._index_in_epoch = 0

        

        image = self._flowSightParser.openIFDData(current_image_ID , verbose=False)
        mask = self._flowSightParser.openIFDData(current_image_ID+1 , verbose=False)


        if self._flowSightParser.eof():
            self._num_examples = self._index_in_epoch
            self._epochs_done += 1
            self._index_in_epoch = 0
            self._flowSightParser.resetToFirstIFD()

        return image, mask

    def nextImage(self):
        current_image_ID = self._index_in_epoch * 2 +1

        self._index_in_epoch += 1
        if self._index_in_epoch > self._num_examples:
            self._epochs_done += 1
            self._index_in_epoch = 0

        image = self._flowSightParser.openIFDData(current_image_ID , verbose=False)
        mask = self._flowSightParser.openIFDData(current_image_ID+1 , verbose=False)

        return image

    def nextMask(self):
        current_image_ID = self._index_in_epoch * 2 +1

        self._index_in_epoch += 1
        if self._index_in_epoch > self._num_examples:
            self._epochs_done += 1
            self._index_in_epoch = 0

        image = self._flowSightParser.openIFDData(current_image_ID+1 , verbose=False)

        return image


    # Target resolution required! ==> not all images are of the same size
    def nextBatch(self, batch_size, image_size):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        end = self._index_in_epoch
        
        if end > self._num_examples:
            end = self._num_examples
            self._epochs_done += 1
            self._index_in_epoch = 0

        count = end-start
        # print("batch:", batch_size)
        # print("end: ", count)
        batch = np.ndarray(shape=(count, image_size,image_size, self.num_channels))

        for i in range(0,count):
            current_image_ID = (self._index_in_epoch-count+i) * 2 +1 

            image = self._flowSightParser.openIFDData(current_image_ID , verbose=False)

            for channel in range(image.shape[-1]):
                img = image[:,:,channel]
        
                batch[i][:,:,channel] = pad_or_crop(img, image_size, 'symmetric')# pad_or_crop(img, image_size, 'symmetric', constant_values=(0))

 
        return batch


    def __del__(self):
        pass