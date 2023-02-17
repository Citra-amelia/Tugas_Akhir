def compress_image_lzw(image_path, compressed_path):
    # Read image file
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Convert image data to bytearray
    image_data = bytearray(image_data)
    
    # Create initial dictionary with all possible byte values
    dictionary = {bytes([i]): i for i in range(256)}
    
    # Initialize variables
    current_string = b''
    compressed = []
    
    # Loop through image data
    for byte in image_data:
        # Add current byte to current string
        new_string = current_string + bytes([byte])
        # Check if new string is in dictionary
        if new_string in dictionary:
            current_string = new_string
        else:
            # Add current string to compressed data
            compressed.append(dictionary[current_string])
            # Add new string to dictionary
            dictionary[new_string] = len(dictionary)
            # Set current string to current byte
            current_string = bytes([byte])
    
    # Add final string to compressed data
    if current_string:
        compressed.append(dictionary[current_string])
    
    # Write compressed data to file
    with open(compressed_path, 'w') as f:
        for byte in compressed:
            f.write(str(byte) + ' ')
    
    return compressed


def decompress_image_lzw(compressed_path, decompressed_path):
    # Read compressed file
    with open(compressed_path, 'r') as f:
        compressed_data = f.read()
    
    # Convert compressed data to list of integers
    compressed_data = [int(byte) for byte in compressed_data.split() if byte]
    
    # Create initial dictionary with all possible byte values
    dictionary = {i: bytes([i]) for i in range(256)}
    
    # Initialize variables
    current_string = bytes([compressed_data[0]])
    decompressed = bytearray(current_string)
    
    # Loop through compressed data
    for byte_code in compressed_data[1:]:
        # Get string for current byte code
        if byte_code in dictionary:
            new_string = dictionary[byte_code]
        elif byte_code == len(dictionary):
            new_string = current_string + bytes([current_string[0]])
        else:
            raise ValueError('Bad compressed byte: %s' % byte_code)
        
        # Add new string to decompressed data
        decompressed += new_string
        
        # Add current string + new string[0] to dictionary
        dictionary[len(dictionary)] = current_string + bytes([new_string[0]])
        
        # Set current string to new string
        current_string = new_string
    
    # Write decompressed data to file
    with open(decompressed_path, 'wb') as f:
        f.write(decompressed)
    
    return decompressed

compressed_img = compress_image_lzw("obat-tradisional.jpg", "compressed.txt")
decompressed_img = decompress_image_lzw("compressed.txt", "decompressed.jpg")
