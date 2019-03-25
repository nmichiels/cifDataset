import bioformats
import bioformats.formatreader
import javabridge
import javabridge.jutil


class CIFDataset(object):
    
    def __init__(self, cifFile, overRuleChannelCount = None):
        try:
            print('Initializing Dataset: ' + cifFile)
            javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='8G')

            # o = bioformats.get_omexml_metadata(path=cifFile)
            # print("test: ", o)
            self._reader = bioformats.formatreader.get_image_reader("tmp", path=cifFile)

            jmd = javabridge.JWrapper(self._reader.rdr.getMetadataStore())
            print("ChannelName", jmd.getChannelName(1,0),jmd.getChannelName(1,1), jmd.getChannelName(1,2))
    
            
            # print("test", test)
    

            self._nimages = int(jmd.getImageCount() / 2)
            self._nchannels = jmd.getChannelCount(0)
            print("Image Count: " + repr(self._nimages))
            print("Channel Count: " + repr(self._nchannels))

            if (overRuleChannelCount):
                print("BEWARE: overRuleChannelCount is not used in cifDatasetBioformats")
            self._current_image_ID = 0
         
            # test = javabridge.call(self._reader.metadata, "getChannelName", "(II)Ljava/lang/String;", 10,1)
            # self.getChannelName = javabridge.jutil.make_method('getChannelName','(II)Ljava/lang/String;', '''Get the name for a particular channel. imageIndex - image # to query (use C = 0_ channelIndex - channel # to querry''')
            # channelName = self.getChannelName(20,1)
        except javabridge.jutil.JavaException as err:
            print("JavaBridge Error.")
            print("JavaException error: {0}".format(err))

    def nextBatch(self, batch_size):
        print ("Next batch")
        # todo

    def nextImage_withmask(self):
        image = self._reader.read(series=self._current_image_ID)
        mask = self._reader.read(series=self._current_image_ID+1)
        self._current_image_ID += 2
        return image, mask

    def nextImage(self):
        image = self._reader.read(series=self._current_image_ID)
        # mask = self._reader.read(series=self._current_image_ID+1)
        self._current_image_ID += 2
        return image

    # set dataset back to first image
    def reset(self):
        self._current_image_ID = 0

    # check if end of dataset
    def eod(self):
        if (self._current_image_ID >= self._nimages*2):
            return True
        else:
            return False

    def numberOfImages(self):
        return self._nimages

    def numberOfChannels(self):
        return self._nchannels

    def __del__(self):
        javabridge.kill_vm()