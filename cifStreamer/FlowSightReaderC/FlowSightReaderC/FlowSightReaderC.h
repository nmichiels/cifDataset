#ifndef GABOR_H
#define GABOR_H

#include "matrixVector.h"

#include <stdio.h>
#include <iostream>
#include "FlowSightReaderC.h"
#include <vector>

bool openFile(const std::string& filename);
void openGreyscaleBytes(int imageWidth, int imageHeight, int nchannels, ConstMapVecl& stripByteCounts, ConstMapVecl& stripOffsets,  MapMatrixf & uncompressed);
void openBitmaskBytes(int imageWidth, int imageHeight, int nchannels, ConstMapVecl&  stripByteCounts, ConstMapVecl& stripOffsets,  MapMatrixf & uncompressed);

#endif
