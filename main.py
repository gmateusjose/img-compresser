import sys
import os

from PIL import Image


MAX_FILESIZE = 10**6  # bytes
MIN_QUALITY = 1  # Minimum quality
MAX_QUALITY = 95 # Maximum quality


def compress(filepath, quality):
    filename = os.path.basename(filepath)
    compressed_filename = os.path.join('cmp', filename)

    with Image.open(filepath) as img:
        print(f'saving {compressed_filename} with quality {quality}')
        img.save(compressed_filename, optimized=True, quality=quality)

    return os.path.getsize(compressed_filename)


def main():
    filepath = sys.argv[1]
    if (size := os.path.getsize(filepath)) < MAX_FILESIZE:
        print(f'{filepath} {size} bytes does not need a compression')
        return

    possible_qualities = [i for i in range(MIN_QUALITY, MAX_QUALITY + 1)]

    if sys.argv[2] == 'linear':
        linear_search(filepath, possible_qualities)
    elif sys.argv[2] == 'binary':
        binary_search(filepath, possible_qualities)
    else:
        print('USAGE: python main.py [filename] [linear | binary]')


def linear_search(filepath, possible_qualities):
    for quality in reversed(possible_qualities):
        if (filesize := compress(filepath, quality)) < MAX_FILESIZE:
            print(f'{filepath} compressed to {filesize} bytes')
            break


def binary_search(filepath, possible_qualities):
    min_quality_index = 0
    max_quality_index = len(possible_qualities) - 1
    while True:
        mid_quality_index = int((min_quality_index + max_quality_index) / 2)
        filesize = compress(filepath, possible_qualities[mid_quality_index])

        if filesize > MAX_FILESIZE:
            max_quality_index = mid_quality_index
        elif (filesize < MAX_FILESIZE) and (min_quality_index < mid_quality_index):
            min_quality_index = mid_quality_index
        else:
            print(f'{filepath} compressed to {filesize} bytes')
            break


if __name__ == '__main__':
    main()
