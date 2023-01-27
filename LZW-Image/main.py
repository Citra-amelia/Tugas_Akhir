from LZW import LZW
import os

compressor = LZW(os.path.join("Images","lambang-pancasila-sila-1.png"))
compressor.compress()

decompressor = LZW(os.path.join("CompressedFiles","indexCompressed.lzw"))
decompressor.decompress()