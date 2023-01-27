from PIL import Image
import zlib

# membuka gambar
image = Image.open("lambang-pancasila-sila-1.png")

# mengubah gambar ke format bytes
image_bytes = image.tobytes()

# mengompresi gambar
compressed_image = zlib.compress(image_bytes)

# menyimpan gambar yang telah di-compress ke dalam file
with open("compressed_image.zlib", "wb") as f:
    f.write(compressed_image)