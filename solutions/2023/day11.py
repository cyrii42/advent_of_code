'''--- Day 11: Cosmic Expansion ---'''

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from pprint import pprint

@dataclass
class ImageRow():
    pre_expansion_row_num: int
    data: str = ''
    has_galaxy: bool = field(init=False)
    post_expansion_row_num: Optional[int] = None

    def __post_init__(self) -> None:
        self.has_galaxy = True if '#' in self.data else False
        

@dataclass
class ImageColumn():
    pre_expansion_col_num: int
    data: str = ''
    has_galaxy: bool = field(init=False)
    post_expansion_col_num: Optional[int] = None

    def __post_init__(self) -> None:
        self.has_galaxy = True if '#' in self.data else False 


@dataclass
class Galaxy():
    pass


@dataclass
class Universe():
    rows: list[ImageRow]
    columns: list[ImageColumn] = field(init=False)
    galaxies: list[Galaxy] = field(init=False)
    expanded: bool = False

    def __post_init__(self) -> None:
        self.columns = self.create_column_list()
        self.galaxies = self.create_galaxy_list()

    def create_column_list(self) -> list[ImageColumn]:
        num_cols = len(self.rows[0].data)

        output_list = []
        for i in range(num_cols):
            col_data = ''.join(row.data[i] for row in self.rows)
            col = ImageColumn(i, col_data)
            output_list.append(col)

        return output_list

    def create_galaxy_list(self) -> list[Galaxy]:
        ...

    def expand_universe(self) -> None:
        ...

        
            

 



def main():
   image = create_image()
   pprint(image.columns)



    
def create_image() -> Universe:
    with open('./inputs/day11.txt') as file:
        line_list = file.read().split(sep='\n')
    row_list = [ImageRow(i, data) for i, data in enumerate(line_list)]
    
    return Universe(row_list)




class ConnectionNumError(Exception):
    ''' To be raised when a `MapChar` has less or more than 2 connections.'''
    pass

if __name__ == '__main__':
    main()