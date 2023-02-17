import numpy as np
import cv2
from typing import Tuple, List
from PIL import Image
import sys

def compress(data: np.ndarray) -> Tuple[List[int], dict]:
    dictionary_size = 256
    dictionary = {chr(i): i for i in range(dictionary_size)}

    s = ""
    result = []
    for i in range(len(data)):
        char = data[i]

        if s + chr(char) in dictionary:
            s = s + chr(char)
        else:
            result.append(dictionary[s])
            dictionary[s + chr(char)] = dictionary_size
            dictionary_size += 1
            s = chr(char)

    if s:
        result.append(dictionary[s])

    compressed_data = np.array(result)
    compressed_data = compressed_data.astype(np.uint16)

    return compressed_data, dictionary

def decompress(compressed_data: List[int], dictionary: dict) -> np.ndarray:
    dictionary_size = 256
    dictionary = {i: chr(i) for i in range(dictionary_size)}

    s = chr(compressed_data[0])
    result = [s]
    for i in compressed_data[1:]:
        if i in dictionary:
            entry = dictionary[i]
        elif i == dictionary_size:
            entry = s + s[0]
        else:
            raise ValueError('Bad compressed k: %s' % i)

        result.append(entry)

        dictionary[dictionary_size] = s + entry[0]
        dictionary_size += 1

        s = entry

    # convert list to array of uint8
    decompressed_data = np.array([ord(c) for c in "".join(result)], dtype=np.uint8)

    return decompressed_data

def compress_image(img: np.ndarray) -> Tuple[List[List[int]], dict]:
    if img.shape[2] == 1:
        # grayscale image
        compressed_data, dictionary = compress(img.flatten())
        return [compressed_data], {0: dictionary}
    elif img.shape[2] == 3:
        # color image
        compressed_data = []
        dictionary = {}

        for c in range(img.shape[2]):
            data = img[:, :, c].flatten()
            compressed, d = compress(data)
            compressed_data.append(compressed)
            dictionary[c] = d

        return compressed_data, dictionary

def decompress_image(compressed_data: List[List[int]], dictionary: dict, shape: Tuple[int, int, int]) -> np.ndarray:
    if len(compressed_data) == 1:
        # grayscale image
        decompressed_data = decompress(compressed_data[0], dictionary[0])
        decompressed_data = decompressed_data.reshape(shape[:2])
    else:
        # color image
        decompressed_data = np.zeros(shape, dtype=np.uint8)

        for c in range(decompressed_data.shape[2]):
            decompressed = decompress(compressed_data[c], dictionary[c])
            decompressed_data[:, :, c] = decompressed.reshape(shape[:2])

    return decompressed_data

# melakukan kompresi gambar
filename = "obat-tradisional.jpg"
image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
if image is None:
    print("Gagal membuka file")
    sys.exit()

print(f"Ukuran gambar: {image.shape}")

compressed_data, dictionary = compress_image(image)

# simpan hasil kompresi ke dalam file text
with open("compressed.txt", "w") as f:
    for i in compressed_data:
        for j in i:
            f.write(str(j) + " ")
        f.write("\n")

# lakukan dekompresi
with open("compressed.txt", "r") as f:
    compressed_data = []
    for line in f:
        compressed_data.append(np.fromstring(line.strip()[1:-1], sep=",").astype(np.uint16))

    if len(compressed_data) == 1:
        # grayscale image
        decompressed_data = decompress(compressed_data[0], dictionary)
        decompressed_data = decompressed_data.reshape(image.shape[:2])
    else:
        # color image
        decompressed_data = decompress_image(compressed_data, dictionary, image.shape)

#konversi dari numpy array ke PIL image dan tampilkan hasil dekompresi
decompressed_image = Image.fromarray(decompressed_data)
decompressed_image.show()

#simpan hasil dekompresi ke dalam file gambar
decompressed_image.save("decompressed.png")

print("Selesai")
