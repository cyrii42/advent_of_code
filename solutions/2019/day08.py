import functools
from enum import Enum
from pathlib import Path
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

INPUT = aoc.get_input(YEAR, DAY)

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6

class PixelColor(Enum):
    BLACK = 0
    WHITE = 1
    TRANSPARENT = 2

def create_layer_list(data: str):
    width = IMAGE_WIDTH
    height = IMAGE_HEIGHT
    layer_size = width * height

    start = 0
    end = layer_size
    output_list = []
    while end <= len(data):
        output_list.append(''.join(data[start:end]))
        start += layer_size
        end += layer_size
        
    return output_list

def get_char_count(layer: str, target_char: str) -> int:
    return len([char for char in layer if char == target_char])

get_zeroes_count = functools.partial(get_char_count, target_char='0')
get_ones_count = functools.partial(get_char_count, target_char='1')
get_twos_count = functools.partial(get_char_count, target_char='2')

def part_one(data: str):
    layer_list = create_layer_list(data)
    layer_list_sorted = sorted(layer_list, key=get_zeroes_count)
    fewest_zeroes = layer_list_sorted[0]
    return get_ones_count(fewest_zeroes) * get_twos_count(fewest_zeroes)

def determine_pixel_color(layer_list: list[str], idx: int) -> str:
    ''' Assumes layer list is ordered, with top layer first. '''
    for layer in layer_list:
        pixel_color = PixelColor(int(layer[idx]))
        if pixel_color == PixelColor.TRANSPARENT:
            continue
        else:
            return str(pixel_color.value)
    raise ValueError(f"All layers at index {idx} are transparent.")

def print_image(image: list[str], width: int = IMAGE_WIDTH) -> None:
    start = 0
    end = width
    while end <= len(image):
        row = ''.join(image[start:end]).replace('1', '*').replace('0',' ')
        print(row)
        start += width
        end += width
    
def part_two(data: str):
    width = IMAGE_WIDTH
    height = IMAGE_HEIGHT
    
    layer_list = create_layer_list(data)
    num_pixels = width * height
    image = [determine_pixel_color(layer_list, x) for x in range(num_pixels)]
    print_image(image, width)

def main():
    print(f"Part One (input):  {part_one(INPUT)}")
    part_two(INPUT)

if __name__ == '__main__':
    main()