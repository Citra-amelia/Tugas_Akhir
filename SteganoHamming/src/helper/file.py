import cv2


class File:
    def __init__(self, filename):
        self.filename = filename

    def read_ndarray_image_file(self):
        return cv2.imread(self.filename)

    def write_image_file(self, image):
        cv2.imwrite(self.filename, image)


    def get_extention(self):
        has_extention = self.filename.split("/")[-1].find(".") != -1
        self.extension = ""

        if (has_extention):
            self.extension = self.filename.split(".")[-1]

        return self.extension

    def read_files(self):
        with open(self.filename, "r") as f:
            byte_file = f.read()

        return byte_file

    def write_files(self, bytes_file):
        with open(self.filename, 'wb') as fd:
            fd.write(bytes_file)
