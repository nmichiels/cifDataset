#include <stdio.h>
#include <iostream>
#include <fstream>
#include <cstring> // for std::strlen
#include <cstddef> // for std::size_t -> is a typedef on an unsinged int

#include <iostream>
#include "FlowSightReaderC.h"
#include <vector>

#include <chrono>
#include <ctime>
using namespace std ;


std::ifstream fp;
bool opened = false;

bool openFilePointer(const std::string& fileName){
    std::cout << "Opening " << fileName << std::endl;
    
	size_t size = 0; // here
    fp.open(fileName , ios::in|ios::binary|ios::ate );
    if (!fp.is_open()){
        std::cout << "C++ Error: Failed to open input file." << std::endl;
        return false;
    }

    opened = true;
    return true;
}


bool openFile(const std::string& filename){
    return openFilePointer(filename);
}



struct Diff {
    public:
        Diff(std::ifstream& fp, int byteorder, ConstMapVecl& stripByteCounts, ConstMapVecl& stripOffsets) : _fp(fp), _byteorder(byteorder), stripByteCounts(stripByteCounts), stripOffsets(stripOffsets) {
                    index = -1;
                    offset = 0;
                    count = 0;
                    currentByte = 0;
                    nibbleIdx = 2;
                    value = 0;
                    shift = 0;
                    bHasNext = true;
                    loaded = bHasNext;
        }


        bool hasNext() {
            if (loaded) 
                return bHasNext;

            shift = 0;
            value = 0;
            while (! loaded) {
                unsigned char nibble = getNextNibble();
                if (nibble != ((unsigned char) (0xff))){
                    value += ((short) (nibble & 0x7) ) << shift;
                    shift += 3;
                    if ((nibble & 0x8) == 0) {
                        loaded = true;
                        bHasNext = true;
                        if ((nibble & 0x4) != 0) {
                            /*
                            * The number is negative
                            * and the bits at 1 << shift and above
                            * should all be "1". This does it.
                            */
                            value |= - (1 << shift);
                        }
                    }
                }
                else {
                    std::cout << "C++ Error: IOException during read of greyscale image" << std::endl;
                    loaded = true;
                    bHasNext = false;
                    return bHasNext;
            
                }
          
                
            }
            return bHasNext;
        }


        unsigned char getNextNibble() {
            if (nibbleIdx >= 2) {
                if (! getNextByte()) {
                    return (unsigned char)0xff;
                }
                nibbleIdx = 0;
            }
            if (nibbleIdx++ == 0) {
                char nibble = (unsigned char)(currentByte) & 0x0f;
                return nibble;
                
            } else {
                char nibble = (unsigned char)(currentByte)>> 4;
                return nibble;
            }
        }


        bool getNextByte(){
            while (offset == count) {
            index++;
            if (index == stripByteCounts.size()) {
                loaded = true;
                bHasNext = false;
                return false;
            }
            _fp.seekg(stripOffsets[index]);
            offset = 0;
            count = (long)stripByteCounts[index];
            }
            _fp.read(&currentByte, 1);
            offset++;
            return true;
        }

        short __next__() {
            if (! hasNext())
                std::cout << "C++ Error: Tried to read past end of IFD data" << std::endl;
            loaded = false;
            return value;
        }

    public:
        int index = -1;
        long offset = 0;
        long count = 0;
        char currentByte = 0;
        int nibbleIdx = 2;
        short value = 0;
        short shift = 0;
        bool bHasNext = true;
        bool loaded = true;
        std::ifstream& _fp;
        int _byteorder;

        ConstMapVecl& stripByteCounts;
        ConstMapVecl& stripOffsets;

};



 void openGreyscaleBytes(int imageWidth, int imageHeight, int nchannels, ConstMapVecl&  stripByteCounts, ConstMapVecl& stripOffsets,  MapMatrixf & uncompressed){
    if (!opened){
        std::cout << "C++ ERROR: No file opened to read from." << std::endl;
    }

    Diff diffs = Diff(fp, 0, stripByteCounts, stripOffsets);


    short skip = diffs.__next__();  // TODO: now skipping one value, but why?

    int widthAllChannels = imageWidth*nchannels;
    
    std::vector<short> lastRow = std::vector<short>(imageWidth*nchannels, 0);
    std::vector<short> thisRow = std::vector<short>(imageWidth*nchannels, 0);
    int index = 0;
    for (int y=0; y<imageHeight; y++) {
      for (int x = 0; x<widthAllChannels; x++) {
        if (x != 0) {
          thisRow[x] = (short)(diffs.__next__() + lastRow[x] + thisRow[x-1] - lastRow[x-1]);
        } else {
          thisRow[x] = (short)(diffs.__next__() + lastRow[x]);
        }
        uncompressed(y, x) = short(thisRow[x]);

        index += 1;
      }
      std::vector<short> temp = lastRow;
      lastRow = thisRow;
      thisRow = temp;

    }
    uncompressed = uncompressed / 0xffff;  // Scale with maximum 16bit value
    
}
unsigned char readByte(){
    char value = 0;
    fp.read(&value, 1);
    return (unsigned char) value;
}

void openBitmaskBytes(int imageWidth, int imageHeight, int nchannels, ConstMapVecl&  stripByteCounts, ConstMapVecl& stripOffsets,  MapMatrixf & uncompressed){
    if (!opened){
        std::cout << "C++ ERROR: No file opened to read from." << std::endl;
    }

    int widthAllChannels = imageWidth*nchannels;

    size_t off = 0;
    for (int i=0; i<stripByteCounts.size(); i++) {
  
        fp.seekg(stripOffsets[i]);
        for (long j=0; j<stripByteCounts[i]; j+=2) {
            unsigned char value = readByte();

            int runLength = (readByte() & 0xFF)+1;
            if (off + runLength > uncompressed.size()) {
                std::cout << "C++ ERROR (openBitmaskBytes): Unexpected buffer overrun encountered when decompressing bitmask data" <<std::endl;
            }
            for (unsigned b = off; b < off+runLength; ++b)
                uncompressed(b) = value;
   

            off += runLength;
        }
       
    }
    if (off != uncompressed.size()) 
        std::cout << "C++ ERROR (openBitmaskBytes): Buffer shortfall encountered when decompressing bitmask data" << std::endl;

    uncompressed = uncompressed / 0xFF;  // Scale with maximum 8bit value
}