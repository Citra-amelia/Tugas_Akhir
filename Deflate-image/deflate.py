import sys
import zlib
import pickle
import os
from PIL import Image

def compress_image(file_in, file_out, level=9, color_mode='RGB', meta=True):
    try:
        # Open image
       with Image.open(file_in) as im:
            # Get the image information
            format = im.format
            mode = im.mode
            size = im.size
            header = im.info

            with open('metadata.pickle', 'wb') as handle:
                pickle.dump(header, handle, protocol=pickle.HIGHEST_PROTOCOL)
           
            # Validate compression level
            if level < 0 or level > 9:
                raise ValueError('Compression level should be between 0-9')

            # Create a compressor object
            compressor = zlib.compressobj(level)

            # Create a list for compression data
            data = []

            # Compress the image
            if meta:
                # Compress the file header information
                header_bytes = pickle.dumps(header)
                data.append(compressor.compress(header_bytes))
            if color_mode == 'RGB':
                # Compress the image in RGB mode
                im = im.convert("RGB")
                size = im.size
                for y in range(size[1]):
                    for x in range(size[0]):
                        r, g, b = im.getpixel((x, y))
                        data.append(compressor.compress(bytes([r, g, b])))
            elif color_mode == 'RGBA':
                # Compress the image in RGBA mode
                for y in range(size[1]):
                    for x in range(size[0]):
                        r, g, b, a = im.getpixel((x, y))
                        data.append(compressor.compress(bytes([r, g, b, a])))
            else:
                raise ValueError('Unsupported color mode')

            # Add the remaining data
            data.append(compressor.flush())
                
            # Save the compressed image to file
            with open(file_out, 'wb') as f:
                for d in data:
                    f.write(d)
            print(f'Image {file_in} successfully compressed to {file_out}')
            print(f'Reading image from: {os.path.abspath(file_in)}')
    except IOError:
        print(f'Error: Image {file_in} not found')
        sys.exit(1)
    except ValueError as ve:
        print(ve)
        sys.exit(1)

def decompress_image(file_in, file_out):
    
    try:
        # Open compressed file
        with open(file_in, 'rb') as f:
            # Create a decompressor object
            decompressor = zlib.decompressobj()
            # Read the header information
            header_bytes = f.read(1024)
            header = 0
            
            with open('metadata.pickle', 'rb') as handle:
                header = pickle.load(handle)

            # Create a new image with the header
            im = Image.open(file_in)
            im.putinfo(header)

            # Read the compressed image data
            im_bytes = f.read()
            
            # Decompress the image data
            data = decompressor.decompress(im_bytes)
            data_iter = iter(data)
            # Iterate over the image and set the pixels
            for y in range(header['size'][1]):
                for x in range(header['size'][0]):
                    pixels = bytes([next(data_iter) for i in range(3)])
                    im.putpixel((x,y), pixels)

            # Save the decompressed image to file
            im.save(file_out, **header)
            print(f'Image {file_in} successfully decompressed to {file_out}')
    except IOError:
        print(f'Error: Image {file_in} not found')
        sys.exit(1)
    except ValueError as ve:
        print(ve)
        sys.exit(1)

if __name__ == '__main__':
    # # Contoh pemanggilan fungsi
    # compress_image('lambang-pancasila-sila-1.png', 'hasil_kompresi.png', level=9, color_mode='RGB', meta=True)

    # Contoh pemanggilan fungsi
    # decompress_image(file_in='lambang-pancasila-sila-1.png', file_out='gambar_dekompresi.jpg')
