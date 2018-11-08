import builtins
from cifDataset.cifStreamer.FlowSightParser import FlowSightParser

class CIFDataset(object):
    
    def __init__(self, cifFile):
      
        print('Initializing Dataset: ' + cifFile)
        
        fp = builtins.open(cifFile, "r+b")

        self._flowSightParser = FlowSightParser()
        self._flowSightParser.loadFP(fp)
        self._flowSightParser.loadMetaData()

        self._nimages = self._flowSightParser._numCells
        self._nchannels = self._flowSightParser._channelCount
        print("Image Count: " + repr(self._nimages))
        print("Channel Count: " + repr(self._nchannels))

        self._current_image_ID = 1
        

      

    def nextBatch(self, batch_size):
        print ("Next batch")
        # todo

    def nextImage(self):
        image = self._flowSightParser.openIFDData(self._current_image_ID , verbose=False)
        mask = self._flowSightParser.openIFDData(self._current_image_ID+1 , verbose=False)
        self._current_image_ID += 2
        return image, mask

    def nextImage_nomask(self):
        image = self._flowSightParser.openIFDData(self._current_image_ID , verbose=False)
        # mask = self._flowSightParser.openIFDData(self._current_image_ID+1 , verbose=False)
        self._current_image_ID += 2
        return image

    # set dataset back to first image
    def reset(self):
        self._current_image_ID = 1

    # check if end of dataset
    def eod(self):
        if (self._current_image_ID >= self._nimages+1):
            return True
        else:
            return False

    def numberOfImages(self):
        return self._nimages

    def numberOfChannels(self):
        return self._nchannels

    def __del__(self):
        pass