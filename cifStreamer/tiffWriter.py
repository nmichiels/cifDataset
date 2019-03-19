import numpy as np
import sys

from .tiffConstants import *


class TiffWriter(object):
    

 
    def __init__(self, fp, byteorder='little', verbose=False):
        self._fp = fp
        self._byteorder = 'little'
        
        self._bigTiff = False
        self._fakeBigTiff = False

        self.printHeader()

        # Write first the offset integer of the IFD 
        self.writeOffset()
            
        # Write the number of entries for the IFD
        nEntries = 0
        if (self._bigTiff or self._fakeBigTiff):
            self.writeBytes(nEntries , 8)
        else:
            self.writeBytes(nEntries , 2)





        # littleEndian = self.checkHeader()
        # self._fp.seek(startFp)

        # if (littleEndian == None):
        #     print("Wrong header")
        #     return

        # self._byteorder = 'little'
        # if littleEndian:
        #     self._byteorder = 'little'
        # else:
        #     self._byteorder = 'big'

        # if verbose:
        #     print("Reading IFDs");
        # self._ifdOffsets = self.getIFDOffsets()
        # self._numCells = len(self._ifdOffsets) -1 # first one is not a cell

        # if (len(self._ifdOffsets) < 2):
        #     print("No IFDs found");
        #     return

    def writeOffset(self):
        # Write first the offset integer of the IFD 
        self._currentOffset = self._fp.tell() + 4 
        print("Writing offset ", self._currentOffset)
        if (self._bigTiff or self._fakeBigTiff):
            self.writeBytes(self._currentOffset , 8)
        else:
            self.writeBytes(self._currentOffset , 4)

        
    def writeBytes(self, val, nbytes):
        self._fp.write(val.to_bytes(nbytes, self._byteorder))



    def writeTiffIFDEntry(self):
        entryTag = self.readUnsignedShort()
        entryType = self.readUnsignedShort()

        # print(entryTag, entryType, IFDType[entryType])

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


    def printHeader(self):
        if (self._byteorder == 'little'):
            self._fp.write(TiffConstants.LITTLE.to_bytes(1, 'little'))
            self._fp.write(TiffConstants.LITTLE.to_bytes(1, 'little'))
        elif (self._byteorder == 'big'):
            self._fp.write(TiffConstants.BIG.to_bytes(1, 'big'))
            self._fp.write(TiffConstants.BIG.to_bytes(1, 'big'))
        else:
            print("Unknown Byteorder to write.")
            return

        if self._bigTiff:
            self._fp.write(TiffConstants.BIG_TIFF_MAGIC_NUMBER.to_bytes(2, self._byteorder))
        else:
            self._fp.write(TiffConstants.MAGIC_NUMBER.to_bytes(2, self._byteorder))
 