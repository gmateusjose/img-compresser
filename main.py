import base64
import sys
import os
import tempfile

from PIL import Image


UHD_HEIGHT = 2160  # Amount of y-pixels in Ultra HD images
MAX_FILESIZE = 10**6  # Maximum filesize of image output
MIN_QUALITY, MAX_QUALITY = 1, 95 # Quality configuration


def main():
    input = sys.argv[1]
    with open(input, 'rb') as f:
        doc = generate_compressed_base64(f)

    _save_b64(input, doc)


def generate_compressed_base64(file):
    file.seek(0, os.SEEK_END)
    if file.tell() < MAX_FILESIZE:
        file.seek(0)
        return base64.b64encode(file.read()).decode('utf-8')

    with tempfile.TemporaryFile() as filecopy:
        # Resizing UHD Images
        with Image.open(file) as img:
            _, img_height = img.size
            if img_height > UHD_HEIGHT:
                new_img = img.reduce(int(img_height / UHD_HEIGHT))
                new_img.save(filecopy, format=img.format)
            else:
                img.save(filecopy, format=img.format)

        filecopy.seek(0, os.SEEK_END)
        if filecopy.tell() < MAX_FILESIZE:
            filecopy.seek(0)
            return base64.b64encode(filecopy.read()).decode('utf-8')

        # Reducing image quality
        for quality in reversed(range(MIN_QUALITY, MAX_QUALITY + 1)):
            with Image.open(filecopy) as img:
                img.save(filecopy, format=img.format, optimize=True, quality=quality)

            filecopy.seek(0, os.SEEK_END)
            if filecopy.tell() < MAX_FILESIZE:
                filecopy.seek(0)
                return base64.b64encode(filecopy.read()).decode('utf-8')

    raise Exception('Could not further compress')


def _save_b64(input, base64_utf8_string):
    filename = os.path.basename(input)
    output = os.path.join('b64', f'{os.path.splitext(filename)[0]}.txt')

    with open(output, 'wt') as f:
        f.write(base64_utf8_string)


if __name__ == '__main__':
    main()
