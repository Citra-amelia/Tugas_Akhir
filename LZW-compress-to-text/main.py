import numpy as np
import cv2

def compress_image_lzw(img):
    # Mendapatkan ukuran gambar
    height, width = img.shape

    # Inisialisasi dictionary
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}

    # Menyimpan hasil kompresi sebagai list integer
    result = []
    w = ""

    for row in img:
        for pixel in row:
            # Menambahkan string
            p = w + chr(pixel)

            # Jika string sudah ada di dictionary, update w
            if p in dictionary:
                w = p
            else:
                # Tambahkan w ke hasil dan tambahkan p ke dictionary
                result.append(dictionary[w])
                dictionary[p] = dict_size
                dict_size += 1
                w = chr(pixel)

    # Tambahkan w ke hasil jika masih ada
    if w:
        result.append(dictionary[w])

    return result

def decompress_image_lzw(compressed_img_file, height, width):
    # Baca hasil kompresi
    with open(compressed_img_file, "r") as f:
        compressed_img = [int(x) for x in f.read().split()]

    # Inisialisasi dictionary
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}

    result = []
    w = chr(compressed_img.pop(0))
    result.append(w)

    for k in compressed_img:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError("Tidak ditemukan kunci di dictionary")

        result.append(entry)

        # Tambahkan w + entry[0] ke dictionary
        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry

    # Decode result dan konversi ke array numpy
    decoded_result = [int(ord(p)) for p in "".join(result)]
    return np.array(decoded_result).reshape((height, width))

# Contoh pemakaian
if __name__ == "__main__":
    # Baca gambar
    img = cv2.imread("obat-tradisional.jpg", cv2.IMREAD_GRAYSCALE)

    # Kompresi gambar
    compressed_img = compress_image_lzw(img)
    print("Hasil kompresi:", compressed_img)

    # Simpan hasil kompresi sebagai teks
    with open("compressed_image.txt", "w") as f:
        f.write(" ".join(str(x) for x in compressed_img))

    # Dekompresi gambar
    file_name = input("Masukkan nama file teks hasil kompresi: ")
    height, width = img.shape
    decompressed_img = decompress_image_lzw(file_name, height, width)

    # Tampilkan dan simpan gambar
    cv2.imshow("Gambar asli", img)
    decompressed_img = decompressed_img.astype(np.uint8)
    cv2.imshow("Gambar dekompresi", decompressed_img)
    cv2.imwrite("decompressed_image.png", decompressed_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




