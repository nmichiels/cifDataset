"""
This module provides code for parsing multichannel tiff files. This module is used by FlowSightParser to decode specialized tiff channels in the cif files.
"""

import numpy as np
import sys

from .tiffConstants import *

class TiffParser(object):
    """Class to seek through tiff files with multiple IFDs. The actual content is not decoded in this class."""

 
    def __init__(self, fp, verbose=False):
        self._fp = fp
        self._fakeBigTiff = False
        self._bigTiff = False
        self._length = -1

        startFp = self._fp.tell()
        self._fp.seek(0,2) # move the cursor to the end of the file
        self._length  = self._fp.tell()
        self._fp.seek(startFp)
        self._channelCount = 0
        self._numCells = 0
        self._verbose = verbose

        littleEndian = self.checkHeader()
        self._fp.seek(startFp)

        if (littleEndian == None):
            print("Wrong header")
            return

        self._byteorder = 'little'
        if littleEndian:
            self._byteorder = 'little'
        else:
            self._byteorder = 'big'

        
        if self._verbose:
            print("BYTE: ", self._byteorder)
            print("Reading IFDs");

        self._eofReached = False
        self._ifdOffsets = [self.getFirstOffset()]#self.getIFDOffsets()#[self.getFirstOffset()]# self.getIFDOffsets() #
        self._currentOffset = self.getNextIFDOffset(self._ifdOffsets[0])

        #empty file
        if (self._currentOffset <= 0 or self._currentOffset >= self._length):
            self._eofReached = True


        # without preprocessing all offsets there is no way to know how many IFD or cells there are
        self._numCells = len(self._ifdOffsets) -1 # first one is not a cell

    
    def eof(self):
        return self._eofReached

    def resetToFirstIFD(self):
        """Go back to first IFD of the tiff file. This is actually the second, because the first IFD contains all the metadata."""
        self._eofReached = False
        self._currentOffset = self.getNextIFDOffset(self._ifdOffsets[0])

        #empty file
        if (self._currentOffset <= 0 or self._currentOffset >= self._length):
            self._eofReached = True


    def skipBytes(self, numBytes):
        """Skip `numBytes` in the tiff file."""
        self._fp.seek(self._fp.tell() + numBytes)


    def readTiffIFDEntry(self):
        entryTag = self.readUnsignedShort()
        entryType = self.readUnsignedShort()

        # // Parse the entry's "ValueCount"
        valueCount = 0
        if self._bigTiff:  valueCount = self.readLong()
        else : valueCount =  self.readInt()
        if (valueCount < 0):
           print("Count of '" + valueCount + "' unexpected.")
           return None
        
        nValueBytes = valueCount * IFDType[entryType]
        threshhold = 4
        if self._bigTiff: threshhold =  8

        offset = 0
        if( nValueBytes > threshhold):
            offset = self.getNextOffset(0)
        else:
            offset = self._fp.tell();
      
        return TiffIFDEntry(entryTag, entryType, valueCount, offset)


    def loadIFD(self, idxOff):
        offset = self._ifdOffsets[idxOff]
        return self.getIFD(offset)


    def loadNextIFD(self):
        ifd = self.getIFD(self._currentOffset)
        self._currentOffset = self.getNextIFDOffset(self._currentOffset)

        if (self._currentOffset <= 0 or self._currentOffset >= self._length):
            self._eofReached = True
            
        return ifd


    def getIFD(self, offset):
        ifd = {}

        if (offset < 0 or offset >= self._length): return None
        
        self._fp.seek(offset)
        numEntries = 0
        if self._bigTiff: numEntries = self.readLong()
        else : numEntries = self.readUnsignedShort()

        if (numEntries == 0 or numEntries == 1): return None;

        bytesPerEntry = TiffConstants.BYTES_PER_ENTRY
        if (self._bigTiff): bytesPerEntry = TiffConstants.BIG_TIFF_BYTES_PER_ENTRY
        baseOffset = 2
        if (self._bigTiff): baseOffset = 8

        for i in range(numEntries):
            
            self._fp.seek(offset + baseOffset + bytesPerEntry * i);
            entry = self.readTiffIFDEntry()
            if (entry == None): 
                print("break")
                break

            count = entry._valueCount
            tag = entry._entryTag
            pointer = entry._valueOffset
            bpe = IFDType[entry._entryType]

            if (count < 0 or bpe <= 0):
                # // invalid data
                if (self._bigTiff):
                    self.skipBytes(bytesPerEntry - 4 - (8))
                else:
                    self.skipBytes(bytesPerEntry - 4 - (4))
                continue

            inputLen = self._length
            if (count * bpe + pointer > inputLen) :
                oldCount = count
                count = int((inputLen - pointer) / bpe)
                if (count < 0): count = oldCount
            
            if (count < 0 or count > self._length): break;

            value = None
            if (pointer != self._fp.tell()):
                value = entry
            else: 
                value = self.getIFDValue(entry)
        
            if (value != None and not(tag in ifd)):
                ifd[tag] = value
          

        newOffset =offset + baseOffset + bytesPerEntry * numEntries;
        if (newOffset < self._length):
            self._fp.seek(newOffset)
        else:
            self._fp.seek(self._length)
        return ifd


    def fillInIFD(self, ifd):
        """"Fill in IFD entries that are stored at an arbitrary offset."""
        
        for key in ifd:
            entry = ifd[key]
            if (isinstance(entry, TiffIFDEntry)):
                if ((entry._valueCount < 10 * 1024 * 1024 or entry._entryTag < 32768) and entry._entryTag != IFD.COLOR_MAP.value):
                    ifd[entry._entryTag] = self.getIFDValue(entry)
                    

    def printIFDvalues(self, ifd):
        """"Show all entry data."""
       
        for key in ifd:
            if (IFD.has_value(key)):
                print(IFD(key).name , ifd[key], type(ifd[key]))
            else:
                print(key , ifd[key], type(ifd[key]))

    def getIFDValue(self, entry):
        typeName = IFDTypeName[entry._entryType ]
        count = entry._valueCount
        offset = entry._valueOffset

        if (offset >= self._length):
            return None
        
        if (offset != self._fp.tell()):
            if (self._fakeBigTiff and (offset < 0 or offset > self._fp.tell())):
                pass
                offset = offset & 0xffffffff;
                offset = offset + 0x100000000;
        
            self._fp.seek(offset);
        
        if (typeName == "LONG" or type == "IFD"):
            # // 32-bit (4-byte) unsigned integer
            if (count == 1):
                return self.readUnsingedInt()
            longs = [0] * count
            for j in range(count):
                if (self._fp.tell() + 4 <= self._length):
                    longs[j] = self.readUnsingedInt()
            return longs;
        elif (typeName == "SHORT"):
            #  // 16-bit (2-byte) unsigned integer
            if (count == 1): 
                return self.readUnsignedShort()
            shorts = [0] * count
            for j in range(count):
                shorts[j] = self.readUnsignedShort()
            return shorts;


        elif (typeName == "DOUBLE"):
            pass
            # # print("reading DOUBLE")
            # # // Double precision (8-byte) IEEE format
            # if (count == 1): 
            #     return self.readDouble()
            # doubles = [0.0] * count
            # for j in range(count):
            #     doubles[j] = self.readDouble()
            # return doubles
            

        elif (typeName == "ASCII"):
            binary_data = self._fp.read(count)
            text = binary_data.decode('utf-8')
            return text
        return None


    def bytesToInt(self, bytes):
        return int.from_bytes(bytes, self._byteorder)

    def loadBytesToInt(self, numBytes):
        return self.bytesToInt(self._fp.read(numBytes))

    def readByte(self):
        return self._fp.read(1)

    def readInt(self):
        return self.loadBytesToInt(4)

    def readDouble(self):
        pass#return self.loadBytesToDouble(8)

    def readLong(self):
        return self.loadBytesToInt(4)

    def readUnsingedInt(self):
        return self.loadBytesToInt(4)

    def readUnsignedShort(self):
        return self.loadBytesToInt(2)

    def getNextOffset(self, previous):
        if (self._bigTiff or self._fakeBigTiff):
            return self._fp.read(8)  # readLong

        offset = (previous & ~0xffffffff | (self.loadBytesToInt(4)))
      
        # // Only adjust the offset if we know that the file is too large for 32-bit
        # // offsets to be accurate; otherwise, we're making the incorrect assumption
        # // that IFDs are stored sequentially.
        if (offset < previous and offset != 0 and self._length > sys.maxsize):
            offset += int(0x100000000,16);
        
        return offset;
        

    def getFirstIFD(self):
        offset = self.getFirstOffset()
        ifd = self.getIFD(offset)
        return ifd
  

    def getFirstOffset(self):
        header = self.checkHeader()
        if (header == None): return -1
        if (self._bigTiff): self.skipBytes(4)
        return self.getNextOffset(0)
    

    def getNextIFDOffset(self, previousOffset):
        self._fp.seek(previousOffset)
        nEntries = 0
        if self._bigTiff:
            nEntries = self.loadBytesToInt(8)
        else:
            nEntries = self.loadBytesToInt(2)
        self.skipBytes(nEntries * TiffConstants.BYTES_PER_ENTRY)
        return self.getNextOffset(previousOffset)


    def getIFDOffsets(self):
        # check TIFF header
        bytesPerEntry = TiffConstants.BYTES_PER_ENTRY
        if (self._bigTiff):
            bytesPerEntry = TiffConstants.BIG_TIFF_BYTES_PER_ENTRY
        offset = self.getFirstOffset()
        offsets = []
        while (offset > 0 and offset < self._length):
            self._fp.seek(offset);
            offsets.append(offset);
            nEntries = 0
            if self._bigTiff: nEntries = self.loadBytesToInt(8) 
            else: nEntries = self.loadBytesToInt(2)
            self.skipBytes(nEntries * bytesPerEntry)
            offset = self.getNextOffset(offset)
        return offsets

    def checkHeader(self):
        self._fp.seek(0)
        data = self._fp.read(12)
        if data[0:4] in [b'II*\x00', b'MM\x00*']:
            # it's a TIFF file
            # print("TIFF format recognized in data[0:4]")
            self._fp.seek(0)
            endianOne = int.from_bytes(self._fp.read(1), byteorder='little')
            endianTwo = int.from_bytes(self._fp.read(1), byteorder='little')

            littleEndian = endianOne == TiffConstants.LITTLE and endianTwo == TiffConstants.LITTLE
            bigEndian = endianOne == TiffConstants.BIG and endianTwo == TiffConstants.BIG

            if (not littleEndian and not bigEndian):
                print("TiffParser:checkHeader(): Unknown Endian Format")
                return None
            
            byteorder = 'little'
            if bigEndian:
                byteorder = 'big'

            magic = int.from_bytes(self._fp.read(2), byteorder)
            self._bigTiff = magic == TiffConstants.BIG_TIFF_MAGIC_NUMBER
            if (magic != TiffConstants.MAGIC_NUMBER and  magic != TiffConstants.BIG_TIFF_MAGIC_NUMBER):
                print("TiffParser:checkHeader(): Magic Number")
                return None
            if self._verbose:
                print("self._bigTiff: ", self._bigTiff)
        
            return littleEndian
        print("TiffParser:checkHeader(): First bytes are not a Tiff header")
        
