import numpy as np
import builtins
from .tiffParser import TiffParser, IFD


from enum import Enum



class FlowSightParser(object):
    """A class to represent a Python implementation of a FlowSightParser to open cif files."""
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
        self._tiffParser = TiffParser(self._fp) #self.loadFP(self._fp)
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
        return self._tiffParser.resetToFirstIFD()

    def openIFDData(self, idx, verbose=False):
        if (self._tiffParser.eof()):
            return None

        # Loading Image Data of one IFD
        ifd = self._tiffParser.loadNextIFD()#self._tiffParser.loadIFD(idx)
        if verbose:
            self._tiffParser.fillInIFD(ifd) # not required?
            self._tiffParser.printIFDvalues(ifd)
        # 

        imageWidth = int(ifd[IFD.IMAGE_WIDTH.value] / self._channelCount)
        imageHeight = ifd[IFD.IMAGE_LENGTH.value]
        bitsPerPixel = ifd[IFD.BITS_PER_SAMPLE.value]

        compression = ifd[IFD.COMPRESSION.value]

        if (compression == IFD.GREYSCALE_COMPRESSION.value):
            data = self.openGreyscaleBytes(ifd, imageWidth, imageHeight, self._channelCount)
        elif (compression == IFD.BITMASK_COMPRESSION.value):
            data = self.openBitmaskBytes(ifd, imageWidth, imageHeight, self._channelCount)
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
            
    
    def openGreyscaleBytes(self, ifd, imageWidth, imageHeight, nchannels):
        stripByteCounts = ifd[IFD.STRIP_BYTE_COUNTS.value]
        stripOffsets = ifd[IFD.STRIP_OFFSETS.value]

        if type(stripByteCounts) is list:
            pass
        else:
            stripByteCounts = [stripByteCounts]
            stripOffsets = [stripOffsets]
            

        class Diff:
            """Iterator for bytes and nibbles"""
            def __init__(self, fp, byteorder):
                self.index = -1
                self.offset = 0
                self.count = 0
                self.currentByte = None
                self.nibbleIdx = 2
                self.value = 0
                self.shift = 0
                self.bHasNext = True
                self.loaded = self.bHasNext
                self.__fp = fp
                self.__byteorder = byteorder

            def hasNext(self):
                if (self.loaded): return self.bHasNext

                self.shift = 0
                self.value = 0
                while (not self.loaded):
                    nibble = self.getNextNibble()
                    if (nibble == None):
                        print("IOException during read of greyscale image")
                        self.loaded = True
                        self.bHasNext = False
                        return self.bHasNext

                    self.value += ((nibble & 0x7)  << self.shift);
                    self.shift += 3
                    if ((nibble & 0x8) == 0):
                        self.loaded = True
                        self.bHasNext = True
                        if ((nibble & 0x4) != 0):
                            # The number is negative
                            # and the bits at 1 << shift and above
                            # should all be "1". This does it.
                            # two's complement
                            # print("before",self.value, bin(self.value))
                            self.value = self.value | (-(1 << self.shift))
                            # print("after:",self.value, bin(self.value))
                return self.bHasNext
                           
                    

            def getNextNibble(self):
                if (self.nibbleIdx >= 2):
                    self.nibbleIdx = 0
                    if (not self.getNextByte()):
                        return None #int(0xff) #return bytes([0xff])

                if (self.nibbleIdx == 0):
                    self.nibbleIdx = self.nibbleIdx + 1
                    nibble =  (self.currentByte) & 0x0f 
                    return nibble
                else:
                    self.nibbleIdx = self.nibbleIdx + 1
                    nibble = self.currentByte >> 4 # returing as is integer because no proper way to convert to bytes object
                    return nibble
            
            def bytesToInt(self, bytes):
                return int.from_bytes(bytes, self.__byteorder)

            def getNextByte(self):
                # pass
                while (self.offset == self.count):
                    self.index = self.index + 1
                    if (self.index == len(stripByteCounts)):
                        self.loaded = True
                        self.bHasNext = False
                        return False
                
                    self.__fp.seek(stripOffsets[self.index])
                    self.offset = 0
                    self.count = stripByteCounts[self.index]
                
                self.currentByte = self.__fp.read(1)[0]
                self.offset = self.offset + 1
                return True
            


            def __iter__(self):
                return self

            def __next__(self):
                if (not self.hasNext()):
                     print("Tried to read past end of IFD data")
                     return None
                self.loaded = False
                return self.value
        

        diffs = Diff(self._fp, self._tiffParser._byteorder)

        uncompressed = np.zeros((imageWidth * nchannels) * imageHeight , dtype=int)
        lastRow = np.zeros(imageWidth * nchannels, dtype=int)
        thisRow = np.zeros(imageWidth * nchannels, dtype=int)

        skip = diffs.__next__()  # TODO: now skipping one value, but why?
       
        index = 0
        for y in range(imageHeight):
            for x in range(imageWidth*nchannels):
                if (x != 0):
                    thisRow[x] = (diffs.__next__() + lastRow[x] + thisRow[x-1] - lastRow[x-1])
                else:
                    thisRow[x] = (diffs.__next__() + lastRow[x])
                uncompressed[index] = int(thisRow[x])
                index += 1
            temp = lastRow
            lastRow = thisRow
            thisRow = temp

        uncompressed = uncompressed / 0xffff # Scale with maximum 16bit value
        return uncompressed


    #TODO: fix little endian        
    def unpackBytes(self, value, bytebuffer, ndx, nBytes, little):
        if (little):
            for i in range(0,nBytes):
                bytebuffer[ndx + i] = ((value >> (8*i)) & 0xff).to_bytes(1, self._tiffParser._byteorder)
        else:
            for i in range(0,nBytes):
                bytebuffer[ndx + i] = ((value >> (8*(nBytes - i - 1))) & 0xff).to_bytes(1, self._tiffParser._byteorder)
            

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
                    # return None
                uncompressed[off:off+runLength] = self._tiffParser.bytesToInt(value)
                off = off + runLength
            
        
        if (off != uncompressed.size):
            print("Buffer shortfall encountered when decompressing bitmask data")

        uncompressed = uncompressed / 0xff
        return uncompressed
        
    
        

