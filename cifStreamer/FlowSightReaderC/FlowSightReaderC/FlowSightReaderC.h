#ifndef GABOR_H
#define GABOR_H

#include "matrixVector.h"

#include <stdio.h>
#include <iostream>
#include "FlowSightReaderC.h"
#include <vector>


void openGreyscaleBytes(int imageWidth, int imageHeight, int nchannels, int stripByteCounts, int stripOffsets,  MapMatrixf & uncompressed);

#endif
