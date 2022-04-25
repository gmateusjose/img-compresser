import sys
import os

from PIL import Image


UHD_HEIGHT = 2160  # Amount of y-pixels in Ultra HD images
MAX_FILESIZE = 10**6  # Maximum filesize of image output
MIN_QUALITY = 1  # Minimum quality
MAX_QUALITY = 95 # Maximum quality


def check_image_status(path):
    with Image.open(path) as img:
        print(f"[+] {path} {img.size[0]}x{img.size[1]} {os.path.getsize(path)} bytes")


def main():
    input = sys.argv[1]
    filename = os.path.basename(input)
    output = os.path.join('cmp', filename)

    check_image_status(input)

    if (size := os.path.getsize(input)) < MAX_FILESIZE:
        print(f'{input} {size} bytes does not need a compression')
        return

    with Image.open(input) as img:
        _, img_height = img.size
        if img_height > UHD_HEIGHT:
            new_img = img.reduce(int(img_height / UHD_HEIGHT))
            new_img.save(output)
            input = output

    check_image_status(output)

    available_qualities = [q for q in range(MIN_QUALITY, MAX_QUALITY + 1)]
    min_quality_index = 0
    max_quality_index = len(available_qualities) - 1

    last_quality_used = None
    while True:
        mid_quality_index = int((min_quality_index + max_quality_index) / 2)
        quality = available_qualities[mid_quality_index]

        if (last_quality_used is not None) and (last_quality_used == 1) and quality == 1:
            print('Could not further compress')
            break

        with Image.open(input) as img:
            img.save(output, optimized=True, quality=quality)
            check_image_status(output)

        if (filesize := os.path.getsize(output)) > MAX_FILESIZE:
            max_quality_index = mid_quality_index
        elif (filesize < MAX_FILESIZE) and (min_quality_index < mid_quality_index):
            min_quality_index = mid_quality_index
        else:
            print(f'[+] {output} compressed to {filesize} bytes')
            break

        last_quality_used = quality
        input = output

if __name__ == '__main__':
    main()
