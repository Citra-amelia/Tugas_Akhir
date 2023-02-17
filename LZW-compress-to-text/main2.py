import cv2
import numpy as np


# Algoritma kompresi LZW
def compress_image_lzw(img):
    img = img.flatten()
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    current_string = ""
    compressed_data = []
    for symbol in img:
        if current_string + chr(symbol) in dictionary:
            current_string = current_string + chr(symbol)
        else:
            compressed_data.append(dictionary[current_string])
            dictionary[current_string + chr(symbol)] = dict_size
            dict_size += 1
            current_string = chr(symbol)
    compressed_data.append(dictionary[current_string])
    return compressed_data, dictionary


# Algoritma dekompresi LZW
def decompress_image_lzw(compressed_img, dictionary):
    dict_size = 256
    current_string = chr(compressed_img[0])
    decompressed_data = [current_string]
    for code in compressed_img[1:]:
        if code in dictionary:
            new_string = dictionary[code]
        elif code == dict_size:
            new_string = current_string + current_string[0]
        else:
            raise ValueError("Kode tidak ditemukan di kamus.")
        decompressed_data.append(new_string)
        dictionary[dict_size] = current_string + new_string[0]
        dict_size += 1
        current_string = new_string
    return np.array(decompressed_data)


# Baca gambar
img = cv2.imread("lambang-pancasila.png")

# Pisahkan komponen R, G, dan B
b, g, r = cv2.split(img)

# Kompresi gambar
compressed_img = []
for i, channel in enumerate([b, g, r]):
    compressed_data, dictionary = compress_image_lzw(channel)
    compressed_img.append(compressed_data)

# Simpan hasil kompresi sebagai teks
with open("compressed_image-2.txt", "w") as f:
    for i in range(3):
        f.write(" ".join(str(x) for x in compressed_img[i]))
        f.write("\n")

# Dekompresi gambar
file_name = input("Masukkan nama file teks hasil kompresi: ")
height, width, _ = img.shape
decompressed_img = []
with open(file_name, "r") as f:
    for i in range(3):
        compressed_data = f.readline().split()
        compressed_data = [int(x) for x in compressed_data]
        decompressed_data = decompress_image_lzw(compressed_data, dict([(v,k) for k,v in dictionary.items()]))
        decompressed_img.append(decompressed_data)
decompressed_img = np.dstack(decompressed_img)

# Tampilkan dan simpan gambar
cv2.imshow("Gambar asli", img)
decompressed_img = decompressed_img.reshape(height, width, 3)
decompressed_img = decompressed_img.astype(np.uint8)
cv2.imshow("Gambar dekompresi", decompressed_img)
cv2.imwrite("decompressed_image.png", decompressed_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
