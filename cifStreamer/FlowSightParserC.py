import numpy as np
import builtins
from .tiffParser import TiffParser, IFD
from .FlowSightReaderC.FlowSightReaderC import core as fsr


from enum import Enum



class FlowSightParser(object):
    """A class to represent a hybrid Python and C++ implementation of a FlowSightParser to open cif files. Images and masks are decoded in C++."""
    
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
        if not fsr.openFile(file.encode('UTF-8')):
            return False

        self._fp = builtins.open(file, "r+b")
        self._tiffParser = TiffParser(self._fp)
        return True
        
    
    def loadMetaData(self, verbose=False, overRuleChannelCount = None):
        ifd = self._tiffParser.loadIFD(0)
        self._tiffParser.fillInIFD(ifd)
        if (verbose):
            self._tiffParser.printIFDvalues(ifd)
        xml = ifd[self.METADATA_XML_TAG]

        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml)
        imagingNodes = root.find("Imaging");
        ObjectsToAcquireNodes = imagingNodes.find("ObjectsToAcquire");
        self._numCells = self._tiffParser._numCells

        ChannelsInUseIndicatorNodes = imagingNodes.find("ChannelInUseIndicators_0_11");
        

        self._channelCount = ChannelsInUseIndicatorNodes.text.split(' ').count('1')
        self._channelLayout = ChannelsInUseIndicatorNodes.text

        if overRuleChannelCount:
            self._channelCount = overRuleChannelCount 
            
        if (verbose):
            print("Channels used: %s (%i)" %(ChannelsInUseIndicatorNodes.text , self._channelCount))
            print("Num Cells: %i" %(self._numCells))
            for child in ObjectsToAcquireNodes:
                print(child.tag, child.attrib)

        

    def eof(self):
        return self._tiffParser.eof()
        
    def resetToFirstIFD(self):
        self._tiffParser.resetToFirstIFD()
        
    # returns None when end of file
    def openIFDData(self, idx, verbose=False):
        if (self._tiffParser.eof()):
            return None

        # Loading Image Data of one IFD
        ifd = self._tiffParser.loadNextIFD()

        if verbose:
            self._tiffParser.fillInIFD(ifd) # not required?
            self._tiffParser.printIFDvalues(ifd)
        

        imageWidth = int(ifd[IFD.IMAGE_WIDTH.value] / self._channelCount)
        imageHeight = ifd[IFD.IMAGE_LENGTH.value]
        bitsPerPixel = ifd[IFD.BITS_PER_SAMPLE.value]

        compression = ifd[IFD.COMPRESSION.value]

        if (compression == IFD.GREYSCALE_COMPRESSION.value):
            data = self.openGreyscaleBytesC(ifd, imageWidth, imageHeight, self._channelCount) # C++ version
            # data = self.openGreyscaleBytes(ifd, imageWidth, imageHeight, self._channelCount) #Python version


        elif (compression == IFD.BITMASK_COMPRESSION.value):
            data = self.openBitmaskBytesC(ifd, imageWidth, imageHeight, self._channelCount) # C++ version
            # data = self.openBitmaskBytes(ifd, imageWidth, imageHeight, self._channelCount) #Python version
        else:
            print("Unknown Amnis Compression")
            return None

        bytesPerSample = int(ifd[IFD.BITS_PER_SAMPLE.value] / 8)
        data = data.reshape(imageHeight, imageWidth*self._channelCount, order='C')

        # Convert data [height, width*channels] into [height, width, channels]   TODO: find better trick
        data = np.asarray(np.hsplit(data, self._channelCount))
        data = np.rollaxis(data, 2,0) 
        data = np.rollaxis(data, 2,0) 
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
        fsr.openGreyscaleBytes(imageWidth, imageHeight, self._channelCount, np.asarray(stripByteCounts), np.asarray(stripOffsets), data)
        
        return data
    

    def openBitmaskBytesC(self, ifd, imageWidth, imageHeight, nchannels):
        stripByteCounts = ifd[IFD.STRIP_BYTE_COUNTS.value]
        stripOffsets = ifd[IFD.STRIP_OFFSETS.value]

        if type(stripByteCounts) is list:
            pass
        else:
            stripByteCounts = [stripByteCounts]
            stripOffsets = [stripOffsets]

        data = np.zeros([imageHeight,imageWidth*self._channelCount], dtype=np.float32)
        # TODO: fix pass stripByteCounts and  stripOffsets as array
        fsr.openBitmaskBytes(imageWidth, imageHeight, self._channelCount, np.asarray(stripByteCounts), np.asarray(stripOffsets), data)
        
        return data



    def openBitmaskBytes(self, ifd, imageWidth, imageHeight, nchannels):
        stripByteCounts = ifd[IFD.STRIP_BYTE_COUNTS.value]
        stripOffsets = ifd[IFD.STRIP_OFFSETS.value]
        uncompressed = np.zeros(imageWidth * imageHeight * nchannels, dtype=int)

        off = 0
        if type(stripByteCounts) is list:
            pass
        else:
            self._fp.seek(stripOffsets)
            for j in range(0, stripByteCounts, 2):
                value = self._tiffParser.readByte()
                               
                runLength = self._tiffParser.bytesToInt(self._tiffParser.readByte())
                runLength = (runLength & 0xFF)+1
                if (off + runLength > uncompressed.size):
                    print("Unexpected buffer overrun encountered when decompressing bitmask data")
                    return None
              
                uncompressed[off:off+runLength] = self._tiffParser.bytesToInt(value)
                off = off + runLength
            
        if (off != uncompressed.size):
            print("Buffer shortfall encountered when decompressing bitmask data")


        uncompressed = uncompressed / 0xff
        return uncompressed
        
    
        

