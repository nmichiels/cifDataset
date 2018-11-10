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

        pass
    
    def loadFile(self,file):
        self._fp = builtins.open(file)
        self.loadFP(self._fp)
        
    def loadFP(self, fp):
        self._fp = fp
        self._tiffParser = TiffParser(self._fp)

    
    def loadMetaData(self):
        
        # ifd = self.getFirstIFD()
        # self.fillInIFD(ifd)
        # self.printIFDvalues(ifd)
        
        ifd = self._tiffParser.loadIFD(0)
        self._tiffParser.fillInIFD(ifd)
        # self.printIFDvalues(ifd)


        xml = ifd[self.METADATA_XML_TAG]
        # from xml.dom import minidom

        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml)
        imagingNodes = root.find("Imaging");
        ObjectsToAcquireNodes = imagingNodes.find("ObjectsToAcquire");
        self._numCells = int(ObjectsToAcquireNodes.text)

        ChannelsInUseIndicatorNodes = imagingNodes.find("ChannelInUseIndicators_0_11");
        

        self._channelCount = ChannelsInUseIndicatorNodes.text.split(' ').count('1')

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


    def openGreyscaleBytes(self, ifd, imageWidth, imageHeight, nchannels):
        stripByteCounts = ifd[IFD.STRIP_BYTE_COUNTS.value]
        stripOffsets = ifd[IFD.STRIP_OFFSETS.value]
        # print("stripByteCounts: ", stripByteCounts, ", stripOffsets: " , stripOffsets)

        if type(stripByteCounts) is list:
            pass
        else:
            stripByteCounts = [stripByteCounts]
            stripOffsets = [stripOffsets]
            
        # print("Data is a list of", len(stripByteCounts))

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
                # print("value: ", self.value)
                return self.bHasNext
                           
                    

            def getNextNibble(self):
                if (self.nibbleIdx >= 2):
                    self.nibbleIdx = 0
                    if (not self.getNextByte()):
                        return None #int(0xff) #return bytes([0xff])

                    # print("new byte P: ", hex(self.currentByte))
                if (self.nibbleIdx == 0):
                    self.nibbleIdx = self.nibbleIdx + 1
                    nibble =  (self.currentByte) & 0x0f # bytes([self.bytesToInt(self.currentByte) & 0x0f]);
                    # print("new nibble P: ", hex(nibble))
                    return nibble
                else:
                    self.nibbleIdx = self.nibbleIdx + 1
                    nibble = self.currentByte >> 4 # returing as is integer because no proper way to convert to bytes object
                    # print("new nibble P: ", hex(nibble))
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
                
                self.currentByte = self.__fp.read(1)[0] ##self.bytesToInt(self.__fp.read(1))
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

        # uncompressedBytes = np.zeros(imageWidth * imageHeight * 2 * nchannels, dtype=bytes)
        uncompressed = np.zeros((imageWidth * nchannels) * imageHeight , dtype=int)
        lastRow = np.zeros(imageWidth * nchannels, dtype=int)
        thisRow = np.zeros(imageWidth * nchannels, dtype=int)
        # print("first val: ", diffs.__next__())

        # diffs.__next__()
        # diffs.__next__()
        # diffs.__next__()
        # diffs.__next__()
        # diffs.__next__()
        # print("next P: ", diffs.__next__())
        # print("next P: ", diffs.__next__())
        # print("next P: ", diffs.__next__())
        # print("next P: ", diffs.__next__())
        # print("next P: ", diffs.__next__())
        # return uncompressed

        skip = diffs.__next__()  # TODO: now skipping one value, but why?
       
        index = 0
        for y in range(imageHeight):
            for x in range(imageWidth*nchannels):
                if (x != 0):
                    thisRow[x] = (diffs.__next__() + lastRow[x] + thisRow[x-1] - lastRow[x-1])
                else:
                    thisRow[x] = (diffs.__next__() + lastRow[x])
                uncompressed[index] = int(thisRow[x])
                # self.unpackBytes(int(thisRow[x]), uncompressedBytes, index, 2, self._byteorder)
                index += 1
            temp = lastRow
            lastRow = thisRow
            thisRow = temp

        # print(uncompressed.tobytes())
        # uncompressed = uncompressed / np.amax(uncompressed)
        # print(uncompressed)
        # uncompressed = np.frombuffer(uncompressedBytes.tobytes(), dtype=np.float16, count=imageWidth * imageHeight * nchannels)
        return uncompressed
        # import struct
        # print(struct.unpack('f', uncompressed.tobytes()))
        # return uncompressed
        # print(diffs.hasNext())
        # print(diffs.hasNext())
        # print(diffs.hasNext())
    #TODO: fix little endian        
    def unpackBytes(self, value, bytebuffer, ndx, nBytes, little):
        if (little):
            for i in range(0,nBytes):
                bytebuffer[ndx + i] = ((value >> (8*i)) & 0xff).to_bytes(1, self._tiffParser._byteorder)
        else:
            for i in range(0,nBytes):
                bytebuffer[ndx + i] = ((value >> (8*(nBytes - i - 1))) & 0xff).to_bytes(1, self._tiffParser._byteorder)
            
    
        # print(value, bin(value))

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

        maxVal = np.amax(uncompressed)
        if (maxVal != 0):
            uncompressed = uncompressed / maxVal
            # return None
        # print(uncompressed)
        
        return uncompressed
        
    
        

