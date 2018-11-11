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
        Diff(std::ifstream& fp, int byteorder, const std::vector<long>& stripByteCounts, const std::vector<long>& stripOffsets) : _fp(fp), _byteorder(byteorder), stripByteCounts(stripByteCounts), stripOffsets(stripOffsets) {
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
                // printf("new byte C: 0x%x\n", (unsigned char)currentByte);
            }
            if (nibbleIdx++ == 0) {
                char nibble = (unsigned char)(currentByte) & 0x0f;
                // printf("new nibble C: 0x%x\n", (unsigned char)nibble);
                return nibble;
                
            } else {
                // char nibble = (char)(currentByte & 0xf0);
                char nibble = (unsigned char)(currentByte)>> 4;
                // printf("new nibble C: 0x%x\n", (unsigned char)nibble);
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
            count = (int)stripByteCounts[index];
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
        int offset = 0;
        int count = 0;
        char currentByte = 0;
        int nibbleIdx = 2;
        short value = 0;
        short shift = 0;
        bool bHasNext = true;
        bool loaded = true;
        std::ifstream& _fp;
        int _byteorder;

        const std::vector<long>& stripByteCounts;
        const std::vector<long>& stripOffsets;

};



 void openGreyscaleBytes(int imageWidth, int imageHeight, int nchannels, int stripByteCounts, int stripOffsets,  MapMatrixf & uncompressed){
    // std::cout << "Start decoding greyscale bytes..." << std::endl;
    if (!opened){
        std::cout << "C++ ERROR: No file opened to read from." << std::endl;
    }
    // std::cout << "Target: " << imageHeight << ", " << imageWidth << std::endl;
    // std::cout << "Uncompressed: " << uncompressed.rows() << ", " << uncompressed.cols() << std::endl;
    // std::cout << "Reading " << stripByteCounts << " bytes starting from " << stripOffsets << std::endl;
    // TODO: int to long may cause bugs
    std::vector<long> stripByteCountsList = std::vector<long>(1, long(stripByteCounts));
    std::vector<long> stripOffsetsList = std::vector<long>(1, long(stripOffsets));

    Diff diffs = Diff(fp, 0, stripByteCountsList, stripOffsetsList);




    // unsigned char currentByte  = 0xf1;
    // printf("test byte: %x\n", (unsigned char) (currentByte));
    // printf("test: %x\n", (unsigned char) (currentByte >> 4));
    // return;

    // diffs.__next__();
    // diffs.__next__();
    // diffs.__next__();
    // diffs.__next__();
    // diffs.__next__();
    // std::cout << "Next: " << (short)(diffs.__next__()) << std::endl;
    // std::cout << "Next: " << (short)(diffs.__next__()) << std::endl;
    // std::cout << "Next: " << (short)(diffs.__next__()) << std::endl;
    // std::cout << "Next: " << (short)(diffs.__next__()) << std::endl;
    // std::cout << "Next: " << (short)(diffs.__next__()) << std::endl;
    // return;
    // std::cout << "Next: " << (short)(diffs.__next__()) << std::endl;
    // std::cout << "Next: " << (short)(diffs.__next__()) << std::endl;
    // std::cout << "Next: " << (short)(diffs.__next__()) << std::endl;
    // std::cout << "Next: " << (short)(diffs.__next__()) << std::endl;

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
    
    // for (int y=0; y<imageHeight; y++) {
    //   for (int x = 0; x<widthAllChannels; x++) {
    //     if (y == 0){
    //         if (x != 0) 
    //             uncompressed(y, x) = (short)(diffs.__next__() + uncompressed(y, x-1));
    //         else 
    //             uncompressed(y, x) = (short)(diffs.__next__() + uncompressed(y-1, x));
            
    //     }
    //     else {
    //         if (x != 0)
    //             uncompressed(y, x) = (short)(diffs.__next__() + uncompressed(y-1, x) + uncompressed(y, x-1) - uncompressed(y-1, x-1));
    //         else
    //             uncompressed(y, x) = (short)(diffs.__next__() + uncompressed(y-1, x));
    //     }
    //   }
    // }

    // float maxV = 0.0;
    // float minV = 9999999.0;
    // for (int y=0; y<imageHeight; y++) {
    //   for (int x = 0; x<widthAllChannels; x++) {
    //     if (uncompressed(y,x) > maxV)
    //         maxV = uncompressed(y,x);
    //     if (uncompressed(y,x) < minV)
    //         minV = uncompressed(y,x);
    // }
    // }
    // std::cout << "maxV: " << maxV << std::endl;
    // std::cout << "minV: " << minV << std::endl;
}
unsigned char readByte(){
    char value = 0;
    fp.read(&value, 1);
    return (unsigned char) value;
}

void openBitmaskBytes(int imageWidth, int imageHeight, int nchannels, int stripByteCounts, int stripOffsets,  MapMatrixf & uncompressed){
    if (!opened){
        std::cout << "C++ ERROR: No file opened to read from." << std::endl;
    }

    std::vector<long> stripByteCountsList = std::vector<long>(1, long(stripByteCounts));
    std::vector<long> stripOffsetsList = std::vector<long>(1, long(stripOffsets));

    int widthAllChannels = imageWidth*nchannels;

    size_t off = 0;
    for (int i=0; i<stripByteCountsList.size(); i++) {
  
        fp.seekg(stripOffsetsList[i]);
        for (int j=0; j<stripByteCountsList[i]; j+=2) {
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