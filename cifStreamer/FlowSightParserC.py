import numpy as np
import builtins
from cifDataset.cifStreamer.tiffParser import TiffParser, IFD

import cifDataset.cifStreamer.FlowSightReaderC.FlowSightReaderC.core as fsr


from enum import Enum




class FlowSightParser(object):
    
    # Amnis specific
    CHANNEL_COUNT_TAG = 33000
    ACQUISITION_TIME_TAG = 33004
    CHANNEL_NAMES_TAG = 33007
    CHANNEL_DESCS_TAG = 33008
    METADATA_XML_TAG = 33027
    GREYSCALE_COMPRESSION = 30817
    BITMASK_COMPRESSION = 30818
 
    def __init__(self):
        self._fp = 0
        self._channelCount = 0
        self._numCells = 0
        self._channelLayout = ""

        pass
    
    def loadFile(self,file):
        self._fp = builtins.open(file, "r+b")
        self.loadFP(self._fp)
        
    def loadFP(self, fp):
        self._fp = fp
        self._tiffParser = TiffParser(self._fp)

    
    def loadMetaData(self, verbose=False):
        
        # ifd = self.getFirstIFD()
        # self.fillInIFD(ifd)
        # self.printIFDvalues(ifd)
        
        ifd = self._tiffParser.loadIFD(0)
        self._tiffParser.fillInIFD(ifd)
        if (verbose):
            self._tiffParser.printIFDvalues(ifd)


        xml = ifd[self.METADATA_XML_TAG]
        # from xml.dom import minidom

        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml)
        imagingNodes = root.find("Imaging");
        ObjectsToAcquireNodes = imagingNodes.find("ObjectsToAcquire");
        self._numCells = int(ObjectsToAcquireNodes.text)

        ChannelsInUseIndicatorNodes = imagingNodes.find("ChannelInUseIndicators_0_11");
        

        self._channelCount = ChannelsInUseIndicatorNodes.text.split(' ').count('1')
        self._channelLayout = ChannelsInUseIndicatorNodes.text

        if (verbose):
            print("Channels used: %s (%i)" %(ChannelsInUseIndicatorNodes.text , self._channelCount))
            print("Num Cells: %i" %(self._numCells))
            for child in ObjectsToAcquireNodes:
                print(child.tag, child.attrib)
        # if (IFD.IMAGE_WIDTH.value in ifd):
        #     print("add lfd")

        # ifds.add(ifd);
        # print(ifd)

        # self.openIFDData(2, channelCount)
        # for i in range(1,numCells*2,2):
        #     self.openIFDData(i, channelCount)
        # for i in range(0,numCells*2,2):
            # self.openIFDData(i, channelCount)
        # self.openIFDData(3, channelCount)

        


        
        
        

    def openIFDData(self, idx, verbose=False):
        # Loading Image Data of one IFD
        ifd = self._tiffParser.loadIFD(idx)
        if verbose:
            self._tiffParser.fillInIFD(ifd) # not required?
            self._tiffParser.printIFDvalues(ifd)
        # 

        imageWidth = int(ifd[IFD.IMAGE_WIDTH.value] / self._channelCount)
        imageHeight = ifd[IFD.IMAGE_LENGTH.value]
        bitsPerPixel = ifd[IFD.BITS_PER_SAMPLE.value]
        # print(imageWidth, imageHeight, bitsPerPixel)

        compression = ifd[IFD.COMPRESSION.value]

        if (compression == IFD.GREYSCALE_COMPRESSION.value):
            # print("Loading Image Data")
            
            
            data = self.openGreyscaleBytesC(ifd, imageWidth, imageHeight, self._channelCount)
            # data = self.openGreyscaleBytes(ifd, imageWidth, imageHeight, self._channelCount)


        elif (compression == IFD.BITMASK_COMPRESSION.value):
            # print("Loading Mask Data")
            data = self.openBitmaskBytes(ifd, imageWidth, imageHeight, self._channelCount)
        else:
            print("Unknown Amnis Compression")
            return None

        bytesPerSample = int(ifd[IFD.BITS_PER_SAMPLE.value] / 8)
        # print("bytesPerSample", bytesPerSample)
        # data = data[0:imageWidth*imageHeight]
        data = data.reshape(imageHeight, imageWidth*self._channelCount, order='C')

        # Convert data [height, width*channels] into [height, width, channels]   TODO: find better trick
        data = np.asarray(np.hsplit(data, self._channelCount))
        data = np.rollaxis(data, 2,0) 
        data = np.rollaxis(data, 2,0) 

        # print(data[1:20,1:40,1])
        return data
            
    
    def openGreyscaleBytesC(self, ifd, imageWidth, imageHeight, nchannels):
        stripByteCounts = ifd[IFD.STRIP_BYTE_COUNTS.value]
        stripOffsets = ifd[IFD.STRIP_OFFSETS.value]

        if type(stripByteCounts) is list:
            pass
        else:
            stripByteCounts = [stripByteCounts]
            stripOffsets = [stripOffsets]

        data = np.zeros([imageHeight,imageWidth*self._channelCount], dtype=np.float32)
        # TODO: fix pass stripByteCounts and  stripOffsets as array
        fsr.openGreyscaleBytes(imageWidth, imageHeight, self._channelCount, stripByteCounts[0], stripOffsets[0], data)
        
        return data
    

    def openBitmaskBytes(self, ifd, imageWidth, imageHeight, nchannels):
        stripByteCounts = ifd[IFD.STRIP_BYTE_COUNTS.value]
        stripOffsets = ifd[IFD.STRIP_OFFSETS.value]
        # print("imageWidth: ", imageWidth, "imageHeight: ", imageHeight)
        # print("stripByteCounts: ", stripByteCounts, ", stripOffsets: " , stripOffsets)

        uncompressed = np.zeros(imageWidth * imageHeight * nchannels, dtype=int)
        # print(uncompressed)

        off = 0
        if type(stripByteCounts) is list:
            pass
            # for i in range(len(stripByteCounts):
        else:
            self._fp.seek(stripOffsets)
            for j in range(0, stripByteCounts, 2):
                value = self._tiffParser.readByte()
                # print("value", value)
                
                runLength = self._tiffParser.bytesToInt(self._tiffParser.readByte())
                # print("runLength1", runLength)
                runLength = (runLength & 0xFF)+1
                # print("runLength: ",off + runLength, uncompressed.size, 0xFF)
                if (off + runLength > uncompressed.size):
                    print("Unexpected buffer overrun encountered when decompressing bitmask data")
                    return None
                # if (self.bytesToInt(value) != 0):
                #     print("v:",value)
                uncompressed[off:off+runLength] = self._tiffParser.bytesToInt(value)
                off = off + runLength
            
        # print("off: ", off)
        
        if (off != uncompressed.size):
            print("Buffer shortfall encountered when decompressing bitmask data")


        uncompressed = uncompressed / 0xff
        # maxVal = np.amax(uncompressed)
        # if (maxVal != 0):
        #     uncompressed = uncompressed / maxVal
            # return None
        # print(uncompressed)
        
        return uncompressed
        
    
        

