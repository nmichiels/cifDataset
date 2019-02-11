import numpy as np
import sys

class TiffConstants:

    # /** The number of bytes in each IFD entry. */
    BYTES_PER_ENTRY = int(12)

    # /** The number of bytes in each IFD entry of a BigTIFF file. */
    BIG_TIFF_BYTES_PER_ENTRY = int(20)

    # // TIFF header constants
    MAGIC_NUMBER = int(42)
    BIG_TIFF_MAGIC_NUMBER = int(43)
    LITTLE = int("0x49",16)
    BIG = int("0x4d",16)




IFDType =  {1: 2, 2: 1, 3: 2, 4: 4, 5: 8, 6: 1, 7: 1, 8: 2, 9: 4, 10: 8, 11: 4, 12: 8, 13: 4, 16: 8, 17: 8, 18: 8}
IFDTypeName =  {1: "BYTE", 2: "ASCII", 3: "SHORT", 4: "LONG", 5: "RATIONAL", 6: "SBYTE", 7: "UNDEFINED", 8: "SSHORT", 9: "SLONG", 10: "SRATIONAL", 11: "FLOAT", 12: "DOUBLE", 13: "IFD", 16: "LONG8", 17: "SLONG8", 18: "IFD8"}

from enum import Enum
class IFD(Enum):
    NEW_SUBFILE_TYPE = 254
    IMAGE_WIDTH = 256
    IMAGE_LENGTH = 257
    BITS_PER_SAMPLE = 258
    COMPRESSION = 259
    PHOTOMETRIC_INTERPRETATION = 262
    FILL_ORDER = 266
    STRIP_OFFSETS = 273
    SAMPLES_PER_PIXEL = 277
    ROWS_PER_STRIP = 278
    STRIP_BYTE_COUNTS = 279
    X_RESOLUTION = 282
    Y_RESOLUTION = 283
    PLANAR_CONFIGURATION = 284
    COLOR_MAP = 320
    RESOLUTION_UNIT = 296
    DATE_TIME = 306

    # Amnis specific
    CHANNEL_COUNT_TAG = 33000
    ACQUISITION_TIME_TAG = 33004
    CHANNEL_NAMES_TAG = 33007
    CHANNEL_DESCS_TAG = 33008
    METADATA_XML_TAG = 33027
    GREYSCALE_COMPRESSION = 30817
    BITMASK_COMPRESSION = 30818
    
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

class TiffIFDEntry(object):
        def __init__(self, entryTag, entryType, valueCount, valueOffset):
            self._entryTag = entryTag
            self._entryType = entryType
            self._valueCount = valueCount
            self._valueOffset = valueOffset
