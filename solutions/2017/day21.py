import itertools
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
from rich import print

import advent_of_code as aoc

CURRENT_FILE = Path(__file__)
YEAR = int(CURRENT_FILE.parts[-2])
DAY = int(CURRENT_FILE.stem.removeprefix('day')[0:2])

EXAMPLE = '../.# => ##./#../...\n.#./..#/### => #..#/..../..../#..#'
INPUT = aoc.get_input(YEAR, DAY)

START = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [1, 1, 1]])  

class EnhancementFailed(Exception):
    pass

class NotDivisible(Exception):
    pass

class Not3x3(Exception):
    pass

@dataclass
class Rule:
    input: np.ndarray
    output: np.ndarray

    def check_input(self, input_image: np.ndarray) -> bool:
        if input_image.shape[0] != self.input.shape[0]:
            return False

        return (np.array_equal(input_image, self.input) 
            or np.array_equal(np.flipud(input_image), self.input)
            or np.array_equal(np.fliplr(input_image), self.input)
            
            or np.array_equal(np.rot90(input_image, k=1), self.input)
            or np.array_equal(np.flipud(np.rot90(input_image, k=1)), self.input)
            or np.array_equal(np.fliplr(np.rot90(input_image, k=1)), self.input)
            
            or np.array_equal(np.rot90(input_image, k=2), self.input)
            or np.array_equal(np.flipud(np.rot90(input_image, k=2)), self.input)
            or np.array_equal(np.fliplr(np.rot90(input_image, k=2)), self.input)

            or np.array_equal(np.rot90(input_image, k=3), self.input)
            or np.array_equal(np.flipud(np.rot90(input_image, k=3)), self.input)
            or np.array_equal(np.fliplr(np.rot90(input_image, k=3)), self.input))

    def __repr__(self) -> str:
        return self.input.__str__() + ' => \n' + self.output.__str__()

@dataclass
class ArtGenerator:
    ruleset: list[Rule]
    image: np.ndarray

    def __repr__(self) -> str:
        return self.image.__str__()

    @property
    def image_size(self) -> int:
        ''' Returns the length of the first row of the image '''
        return self.image.shape[0]

    @property
    def num_pixels_on(self) -> int:
        return self.image.sum()

    def enhance_image(self) -> None:
        # if image size = 3, we only have one sub-image, so enhance it and return
        if self.image_size == 3:
            self.image = self._enhance_subimage(self.image, self.ruleset)
            return

        # otherwise, break the pixels up into 2x2 or 3x3 squares
        subimage_list = self._extract_subimages()

        # then enhance each sub-image
        enhanced_subimages = [self._enhance_subimage(si, self.ruleset) for si in subimage_list]

        # then stitch the sub-images back together
        self.image = self._merge_enhanced_subimages(enhanced_subimages)

    def _extract_subimages(self, image: Optional[np.ndarray] = None) -> list[np.ndarray]:
        if not image:
            image = self.image
        subimage_size = 2 if image.shape[0] % 2 == 0 else 3
        
        slices = [(0+(i*subimage_size),subimage_size+(i*subimage_size))
                  for i in range(image.shape[0] // subimage_size)]
        
        output_list = []
        for pair in itertools.product(slices, repeat=2):
            image_copy = self.image.copy()
            s1, s2 = pair
            output_list.append(image_copy[s1[0]:s1[1], s2[0]:s2[1]])
        return output_list

    @staticmethod
    def _enhance_subimage(subimage: np.ndarray,
                          ruleset: list[Rule]
                          ) -> np.ndarray:
        for rule in ruleset:
            if rule.check_input(subimage):
                return rule.output
        raise EnhancementFailed(subimage)

    @staticmethod
    def _merge_enhanced_subimages(subimage_list: list[np.ndarray]) -> np.ndarray:
        num_subimages = len(subimage_list)
        subimages_per_row = math.isqrt(num_subimages)
        num_rows = subimages_per_row

        row_list = []
        for i in range(num_rows):
            start = 0 + i*subimages_per_row
            end = subimages_per_row + i*subimages_per_row
            row_list.append(np.concatenate(*[subimage_list[start:end]], axis=1))

        return np.concatenate([row for row in row_list], axis=0)    

def extract_3_x_3_blocks(image: np.ndarray) -> list[np.ndarray]:
    image_size = image.shape[0]
    if image_size % 3 != 0:
        raise NotDivisible   
    output_list = []
    for row in range(0, image_size, 3):
        for col in range(0, image_size, 3):
            output_list.append(image[row:row+3, col:col+3])
    return output_list

def parse_data(data: str) -> list[Rule]:
    line_list = data.splitlines()
    output_list = []
    for line in line_list:
        line = line.replace('#', '1').replace('.', '0').replace('=>', '/')
        line = [x.strip() for x in line.split('/')]
        break_pt = len(line) // 2   # 2 of 5 OR 3 of 7
        start = np.array([[int(c) for c in num] for num in line[0:break_pt]])
        end = np.array([[int(c) for c in num] for num in line[break_pt:]])
        output_list.append(Rule(start, end))
    return output_list

def part_one(data: str, 
             start_image: np.ndarray = START,
             num_iterations: int = 5):
    ruleset = parse_data(data)
    art_generator = ArtGenerator(ruleset, start_image)
    for _ in range(num_iterations):
        art_generator.enhance_image()
    return art_generator.num_pixels_on

@dataclass(frozen=True)
class BlockHash:
    b1: tuple[int, int, int]
    b2: tuple[int, int, int]
    b3: tuple[int, int, int]

    def __repr__(self) -> str:
        return f"({self.b1}, {self.b2}, {self.b3})"

    def to_numpy(self) -> np.ndarray:
        return np.array([self.b1, self.b2, self.b3])

def part_two(data: str):
    ''' https://www.reddit.com/r/adventofcode/comments/7l78eb/comment/drk8j2m/

    After 3 iterations a 3x3 block will have transformed into 9 more 3x3 blocks whose
    futures can all be calculated independently. Using this fact I just keep track of 
    how many of each "type" of 3x3 block I have at each stage, and can thus easily 
    calculate the number of each type of 3x3 block I'll have 3 iterations later.'''

    ruleset = parse_data(data)
    art_generator = ArtGenerator(ruleset, START)
    for _ in range(3):
        art_generator.enhance_image()

    block_list = extract_3_x_3_blocks(art_generator.image)
    block_count_dict = make_block_count_dict(block_list)
    block_result_dict = make_block_result_dict(block_list, data)

    three_iterations_dict = make_three_iterations_dict(block_list, ruleset)

    for _ in range(4):
        new_block_count_dict = defaultdict(int)
        for block_hash, count in block_count_dict.items():
            next_round_dict = three_iterations_dict[block_hash]
            for next_round_block_hash, next_round_count in next_round_dict.items():
                new_block_count_dict[next_round_block_hash] += next_round_count * count
        block_count_dict = new_block_count_dict

    answer = 0
    for block, pixels_per_block in block_result_dict.items():
        num_blocks = block_count_dict[block]
        answer += num_blocks * pixels_per_block
    return answer

def make_three_iterations_dict(block_list: list[np.ndarray],
                               ruleset: list[Rule]
                               ) -> dict[BlockHash, dict[BlockHash, int]]:
    ''' Returns a dictionary of dictionaries'''
    block_hash_set = {make_block_hash(block) for block in block_list}
    output_dict = {}
    for block_hash in block_hash_set:
        output_dict[block_hash] = run_three_iterations(block_hash.to_numpy(), ruleset)
    return output_dict

def run_three_iterations(block: np.ndarray, ruleset: list[Rule]
                         ) -> dict[BlockHash, int]:
    art_generator = ArtGenerator(ruleset, block)
    for _ in range(3):
        art_generator.enhance_image()
    block_list = extract_3_x_3_blocks(art_generator.image)
    block_count_dict = make_block_count_dict(block_list)
    return block_count_dict

def make_block_hash(block: np.ndarray) -> BlockHash:
    block_list = block.tolist()
    assert len(block_list) == 3 and all(len(x) == 3 for x in block_list)

    block1, block2, block3 = block_list  
    return BlockHash(tuple(block1), tuple(block2), tuple(block3))

def make_block_count_dict(block_list: list[np.ndarray]) -> dict[BlockHash, int]:
    output_dict = defaultdict(int)
    for block in block_list:
        output_dict[make_block_hash(block)] += 1
    return output_dict
    
def make_block_result_dict(block_list: list[np.ndarray], data: str
                           ) -> dict[BlockHash, int]:
    output_dict = {}
    for block in block_list:
        block_hash = make_block_hash(block)
        output_dict[block_hash] = int(part_one(data, block, 3))
    return output_dict

def main():
    print(f"Part One (example):  {part_one(EXAMPLE, num_iterations=2)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()