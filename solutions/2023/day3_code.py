'''--- Day 3: Gear Ratios ---'''

from dataclasses import dataclass, field
from pprint import pprint

SYMBOL_LIST = ['$', '&', '@', '%', '\n', '+', '*', '-', '/', '#', '=']

@dataclass
class SchematicNumber():
    row_num: int
    num_string: str
    idx_start: int
    idx_end: int
    schematic_list: list[str] = field(repr=False)
    num_int: int = field(init=False)
    adjacent_to_symbol: bool = field(init=False)
    adjacent_to_asterisk: bool = field(init=False)
    location_of_adjacent_asterisk: dict = field(init=False)

    def __post_init__(self):
        self.num_int = int(self.num_string)
        self.previous_row = ('' if (self.row_num) == 0 else self.schematic_list[self.row_num - 1])
        self.same_row = self.schematic_list[self.row_num]
        self.next_row = ('' if self.row_num == (len(self.schematic_list)-1) else self.schematic_list[self.row_num+1])
        self.final_index = (len(self.schematic_list[self.row_num]) - 1)
        self.adjacent_to_symbol = self.test_number_adjacency()
        self.adjacent_to_asterisk = self.test_number_adjacency_to_asterisk()
        self.location_of_adjacent_asterisk = self.find_adjacent_asterisk_index() if self.adjacent_to_asterisk else None

    def test_number_adjacency(self) -> bool:
        ''' Tests whether this `SchematicNumber` is adjacent to a symbol.'''
        start_minus_one = (0 if (self.idx_start == 0) else (self.idx_start - 1))
        end_plus_one = (self.final_index if (self.idx_end == self.final_index) else (self.idx_end + 1))
        
        characters_to_check = (
            self.same_row[start_minus_one:end_plus_one] +
            self.previous_row[start_minus_one:end_plus_one] +
            self.next_row[start_minus_one:end_plus_one]
        )

        if any([(x in SYMBOL_LIST) for x in characters_to_check]):
            return True
        else:
            return False
        
    def test_number_adjacency_to_asterisk(self) -> bool:
        ''' Tests whether this `SchematicNumber` is adjacent to an asterisk.'''
        start_minus_one = (0 if (self.idx_start == 0) else (self.idx_start - 1))
        end_plus_one = (self.final_index if (self.idx_end == self.final_index) else (self.idx_end + 2))
        
        characters_to_check = (
            self.same_row[start_minus_one:end_plus_one] +
            self.previous_row[start_minus_one:end_plus_one] +
            self.next_row[start_minus_one:end_plus_one]
        )

        if any([(x in ['*']) for x in characters_to_check]):
            return True
        else:
            return False

    def find_adjacent_asterisk_index(self) -> int | None:
        ''' Finds the row & index number of the asterisk to which this `SchematicNumber` is adjacent.'''
        start_minus_one = (0 if (self.idx_start == 0) else (self.idx_start - 1))
        end_plus_one = (self.final_index if (self.idx_end == self.final_index) else (self.idx_end + 2))

        for n, row in enumerate([self.previous_row, self.same_row, self.next_row], start=(self.row_num-1)):
            for i, char in enumerate(row[start_minus_one:end_plus_one], start=start_minus_one):
                if char == "*":
                    return {'row_num': n, 'index': i}
        else:
            return None
        
        
        
@dataclass
class SchematicAsterisk():
    row_num: int
    index: int
    schematic_list: list[str] = field(repr=False)
    is_gear: bool = field(init=False)
    num1: SchematicNumber = None
    num2: SchematicNumber = None
    gear_ratio: int = None
    nums_in_adjacent_rows: list[SchematicNumber] = None ## FOR TESTING PURPOSES ONLY

    def __post_init__(self):
        self.previous_row = ('' if (self.row_num) == 0 else self.schematic_list[self.row_num - 1])
        self.same_row = self.schematic_list[self.row_num]
        self.next_row = ('' if self.row_num == (len(self.schematic_list)-1) else self.schematic_list[self.row_num+1])
        self.final_index = (len(self.schematic_list[self.row_num]) - 1)
        self.characters_to_check = (self.previous_row[self.index-1:self.index+2] +
                                    self.same_row[self.index-1:self.index+2] +
                                    self.next_row[self.index-1:self.index+2])
        self.is_gear = self.test_gear_status()

    def test_gear_status(self) -> bool:
        ''' Tests whether this `SchematicAsterisk` qualifies as a "gear," and outputs a boolean.  
            If output is `True`, this method proceeds to set values for `self.num1`, `self.num2`, and `self.gear_ratio`'''

        # print(f"\nChecking asterisk found in Row #{self.row_num} at index #{self.index}...")
        


        
        # print(f"\nChecking asterisk found in Row #{self.row_num} at index #{self.index}... Chars to check:  {self.characters_to_check}")
        # if len([x for x in self.characters_to_check if x.isnumeric()]) <= 1:
        #     return False
        # else:
        #     # print(f"Found at least two adjacent numeric characters!  Processing...")
        #     full_numbers = self.__process_numeric_characters()
        #     if (len(full_numbers) == 2) and full_numbers[0] is not None and full_numbers[1] is not None:
        #         self.num1 = full_numbers[0].num_int
        #         self.num2 = full_numbers[1].num_int
        #         self.gear_ratio = self.num1 * self.num2
        #         # print(f"**GEAR FOUND!**  Row #{self.row_num}:  {self.num1} * {self.num2} = {self.gear_ratio}")
        #         # print(full_numbers)
        #         return True
        #     else:
        #         # print("FAILURE:  Did not find exactly two full numbers.")
        #         # print(full_numbers)
        #         return False
            
    def __process_numeric_characters(self) -> list[SchematicNumber]:
        ''' Private method, to be called only if `test_gear_status()` determines that there exist at least two 
            numeric characters adjacent to this `SchematicAsterisk`.  This method:
            
            - (1) determines whether the set of found numeric characters include exactly two discrete, non-adjacent integers;
            - (2) if so, sets values for `self.num1`, `self.num2`, and `self.gear_ratio`'''
            
        char_dicts_list = self.__create_char_dictionaries()
        # print(char_dicts_list)
        full_numbers = self.__find_full_numbers_from_list_of_dicts(char_dicts_list)
        return full_numbers
         
    def __create_char_dictionaries(self) -> list[dict]:
        ''' Returns a list of dictionaries containing, for each numeric character found:
            - (a) the character
            - (b) the row number
            - (c) the index position'''
        list_of_dicts = []
        for n, row in enumerate([self.previous_row, self.same_row, self.next_row]):
            row_num = self.row_num + (n - 1)
            for i, char in enumerate(row[self.index-1:self.index+2]):
                if char.isnumeric():
                    # print(f"Found a numeric character!  {char} in row {row_num} at index {i}")
                    char_dict = {'character': char, 'row_num': row_num, 'index': (self.index + i)}
                    list_of_dicts.append(char_dict)
        return list_of_dicts
              
    def __find_full_numbers_from_list_of_dicts(self, input_list_of_dicts: list[dict]) -> list[SchematicNumber]:
        ''' Private method.  Takes a list of dictionaries from `__create_char_dictionaries()` and
            determines the corresponding full number for each.  Outputs a list of `SchematicNumber` objects.'''
        
        prev_row_dicts = [x for x in input_list_of_dicts if x['row_num'] == (self.row_num - 1)]
        same_row_dicts = [x for x in input_list_of_dicts if x['row_num'] == (self.row_num + 0)]
        next_row_dicts = [x for x in input_list_of_dicts if x['row_num'] == (self.row_num + 1)]
        
        output_list= []
        for n, char_dicts_list in enumerate([prev_row_dicts, same_row_dicts, next_row_dicts]):
            row_num = self.row_num + (n - 1)
            # print(f"Length of current 'char_dicts_list' (row {row_num}):  {len(char_dicts_list)}")
            # if the current row has no num chars, just move on to the next row
            if len(char_dicts_list) == 0:
                continue  
            
            # if the current row has ONE num char (or THREE, which means one continguous one), find its full number & move on
            elif (len(char_dicts_list) == 1):# or len(char_dicts_list) == 3):
                # print(f"Found 1 num char in Row {row_num}:  '{char_dicts_list[0]['character']}' at Index #{char_dicts_list[0]['index']}")
                full_num_dict_list = self.__find_full_number_for_num_char(char_dicts_list[0])
                if len(full_num_dict_list) == 1:
                    output_list.append(full_num_dict_list[0])
                else:
                    print(f"\nERROR with 1 num char in Row {row_num}:  '{char_dicts_list[0]['character']}' at Index #{char_dicts_list[0]['index']}")
                    print(f"Row {self.row_num - 1}:    {self.previous_row}") if self.row_num > 0 else print('')
                    print(f"*Row {self.row_num}*:  {self.same_row}")
                    print(f"Row {self.row_num + 1}:    {self.next_row}") if self.row_num < len(self.schematic_list)-1 else print('END')
                    print(full_num_dict_list)
                continue

            elif len(char_dicts_list) == 3:
                # print(f"Found 3 num chars in Row {row_num}:  '{char_dicts_list[0]['character']}{char_dicts_list[1]['character']}{char_dicts_list[2]['character']}' at Index #{char_dicts_list[0]['index']}")
                full_num_dict_list = self.__find_full_number_for_num_char(char_dicts_list[0])
                if len(full_num_dict_list) == 1:
                    output_list.append(full_num_dict_list[0])
                else:
                    print(f"\nERROR with 3 num chars in Row {row_num}:  '{char_dicts_list[0]['character']}{char_dicts_list[1]['character']}{char_dicts_list[2]['character']}' at Index #{char_dicts_list[0]['index']}")
                    print(f"Row {self.row_num - 1}:    {self.previous_row}") if self.row_num > 0 else print('')
                    print(f"*Row {self.row_num}*:  {self.same_row}")
                    print(f"Row {self.row_num + 1}:    {self.next_row}") if self.row_num < len(self.schematic_list)-1 else print('END')
                    print(full_num_dict_list)
                continue
                
            # if the current row has EXACTLY TWO num chars, check if they're contiguous;
            elif ((char_dicts_list[1]['index'] - char_dicts_list[0]['index']) == 1):
                # print(f"Found a two-digit contiguous num in Row {row_num}:  '{char_dicts_list[0]['character']}{char_dicts_list[1]['character']}' at Index #{char_dicts_list[0]['index']}")
                combined_dict = {'character': (char_dicts_list[0]['character'] + char_dicts_list[1]['character']), 'row_num': char_dicts_list[0]['row_num'], 'index': char_dicts_list[0]['index']}
                full_num_dict_list = self.__find_full_number_for_num_char(combined_dict)
                if len(full_num_dict_list) == 1:
                    output_list.append(full_num_dict_list[0])
                else:
                    print(f"\nERROR with two-digit contiguous num in Row {row_num}:  '{char_dicts_list[0]['character']}{char_dicts_list[1]['character']}' at Index #{char_dicts_list[0]['index']} ")
                    print(f"Row {self.row_num - 1}:    {self.previous_row}") if self.row_num > 0 else print('')
                    print(f"*Row {self.row_num}*:  {self.same_row}")
                    print(f"Row {self.row_num + 1}:    {self.next_row}") if self.row_num < len(self.schematic_list)-1 else print('END')         
                    print(full_num_dict_list)     
                continue
            
            # if the current row has EXACTLY TWO num char and they're NOT contiguous, find the full number for each one
            else:
                # print(f"Found two NON-contiguous num chars in Row {row_num}:  '{char_dicts_list[0]['character']}' and '{char_dicts_list[1]['character']}' at Index #{char_dicts_list[0]['index']}")
                full_num_dict_list_1 = self.__find_full_number_for_num_char(char_dicts_list[0])
                full_num_dict_list_2 = self.__find_full_number_for_num_char(char_dicts_list[1])
                if len(full_num_dict_list_1) == 1:
                    if (full_num_dict_list_1 == full_num_dict_list_2):
                        print(f"ERROR:  Found the same number twice for Row {self.row_num} at Index #{self.index}.")
                    else:
                        output_list.append(full_num_dict_list_1[0])
                        output_list.append(full_num_dict_list_1[0])
                elif (len(full_num_dict_list_1) == 2):
                    if (full_num_dict_list_1 == full_num_dict_list_2):
                        output_list.append(full_num_dict_list_1[0])
                        output_list.append(full_num_dict_list_1[1])
                    else:
                        output_list.append(full_num_dict_list_1[0])
                        output_list.append(full_num_dict_list_2[0])
        self.list_of_dicts = output_list   ## FOR TESTING ONLY
        return output_list
    
    def __find_full_number_for_num_char(self, input_dict: dict) -> [SchematicNumber]:
        # print(f"Finding full number for {input_dict}")
        numbers_in_adjacent_rows = self.__find_numbers_in_adjacent_rows()
        number_list = []
        for number in numbers_in_adjacent_rows:
            if (number.row_num == input_dict['row_num']):
                if number.num_string.startswith(input_dict['character'][0]) and (input_dict['index'] == number.idx_start):
                    number_list.append(number)
                elif number.num_string.endswith(input_dict['character'][-1]) and (input_dict['index'] == number.idx_end):
                    number_list.append(number)
                elif (input_dict['character'] in number.num_string) and (number.idx_start <= input_dict['index']) and (number.idx_end >= input_dict['index']):  # ((abs(input_dict['index'] - number.idx_start) == 1) or (abs(input_dict['index'] - number.idx_end) == 1)):
                    number_list.append(number)
                # print(f"Number: {number.num_int} in Row {number.row_num} at Index #{number.idx_start}")
                # number_list.append(number)
        if len(number_list) == 0:
            # print(f"FAILURE:  Did not find a number for '{input_dict['character']}' in Row {input_dict['row_num']} at Index #{input_dict['index']}.")
            return number_list
        elif len(number_list) == 2:
            # return [x for x in number_list if (x.location_of_adjacent_asterisk['index'] == input_dict['index'])]
            print(f"\nPOTENTIAL ISSUE:  Found TWO numbers for '{input_dict['character']}' in Row {input_dict['row_num']} at Index #{input_dict['index']}:  {[x.num_int for x in number_list]}.")
            print(f"Row {self.row_num - 1}:    {self.previous_row}") if self.row_num > 0 else print('')
            print(f"*Row {self.row_num}*:  {self.same_row}")
            print(f"Row {self.row_num + 1}:    {self.next_row}") if self.row_num < len(self.schematic_list)-1 else print('END')       
            return number_list
        elif len(number_list) > 2:
            print(f"ERROR:  Found MORE THAN TWO numbers for '{input_dict['character']}' in Row {input_dict['row_num']} at Index #{input_dict['index']}.")
            return number_list
        else:
            return number_list
              
    def __find_numbers_in_adjacent_rows(self) -> list[SchematicNumber]:
        ''' Finds all numbers adjacent to an asterisk in this `SchematicRow` plus the two immediately adjacent rows,
            and outputs a list of `SchematicNumber` objects.'''
        output_list = []
        for n, row in enumerate([self.previous_row, self.same_row, self.next_row]):
            row_num = self.row_num + (n - 1)
            for i, char in enumerate(row):
                if char.isnumeric() and (row[i-1].isnumeric() == False):
                    num_string = char
                    for x in range(i+1,len(row)):
                        if row[x].isnumeric():
                            num_string = num_string + row[x]
                            continue
                        else:
                            break
                    output_list.append(SchematicNumber(row_num, num_string, i, i+len(num_string), self.schematic_list))
                else:
                    continue
        self.nums_in_adjacent_rows = [x for x in output_list if x.adjacent_to_asterisk] ### FOR TESTING ONLY
        # print(f"Asterisk-adjacent numbers in Row {self.row_num} and adjoining rows: {[x.num_int for x in self.nums_in_adjacent_rows]}")
        return [x for x in output_list if x.adjacent_to_asterisk]
        
        
@dataclass
class SchematicRow():
    row_num: int
    row: str = field(repr=False)
    schematic_list: list[str] = field(repr=False)
    numbers_in_row: list[SchematicNumber] = field(init=False, repr=False)
    adjacent_nums: list[int] = field(init=False, repr=False)
    sum_of_adjacent_nums: int = field(init=False, repr=False)
    asterisks_in_row: list[SchematicAsterisk] = field(init=False, repr=False)
    contains_gear: bool = field(init=False, repr=False)
    
    def __post_init__(self) -> None:
        self.numbers_in_row = self.find_numbers()
        self.previous_row = ('' if self.row_num == 0 else self.schematic_list[self.row_num - 1])
        self.next_row = ('' if (self.row_num == (len(self.schematic_list)-1)) else self.schematic_list[self.row_num + 1])
        self.adjacent_nums = [x.num_int for x in self.numbers_in_row if x.adjacent_to_symbol]
        self.sum_of_adjacent_nums = sum(self.adjacent_nums)
        self.asterisks_in_row = self.find_asterisks()
        self.contains_gear = True if any(x.is_gear for x in self.asterisks_in_row) else False
        
    def find_numbers(self) -> list[SchematicNumber]:
        ''' Finds numbers in this `SchematicRow` and outputs a list of `SchematicNumber` objects.'''
        output_list = []
        for i, char in enumerate(self.row):
            if char.isnumeric() and (self.row[i-1].isnumeric() == False):
                num_string = char
                for x in range(i+1,len(self.row)):
                    if self.row[x].isnumeric():
                        num_string = num_string + self.row[x]
                        continue
                    else:
                        break
                output_list.append(SchematicNumber(self.row_num, num_string, i, i+(len(num_string)-1), self.schematic_list))
            else:
                continue
        return output_list
    
    def find_asterisks(self) -> list[SchematicAsterisk]:      
        ''' Finds asterisk symbols in this `SchematicRow` and outputs a list of `SchematicAsterisk` objects.'''
        output_list = []
        for i, char in enumerate(self.row):
            if char == '*':
                output_list.append(SchematicAsterisk(self.row_num, i, self.schematic_list))
            else:
                continue
        return output_list

class Schematic():
    def __init__(self, input: str):
        self.input_string = input
        self.row_list = self.input_string.split(sep='\n')
        self.symbol_list = [x for x in set(self.input_string) if x.isnumeric() == False and x != '.']
        self.row_objects = [SchematicRow(i, x, self.row_list) for (i, x) in enumerate(self.row_list)]
        self.part_one_row_sums = [x.sum_of_adjacent_nums for x in self.row_objects]
        self.all_asterisks = self.find_asterisks_in_schematic()
    
    def find_part_one_total(self) -> int:
        ''' Finds the sum of all `SchematicNumber` objects in this `Schematic`.'''
        total = 0
        for subtotal in self.part_one_row_sums:
            total = total + subtotal
        return total
    
    def find_part_two_total(self) -> int:
        ''' Finds the sum of all "gear ratios" 'in this `Schematic`.'''
        gear_ratio_total = self.match_numbers_to_asterisks()

        return gear_ratio_total

    def find_asterisks_in_schematic(self) -> list[SchematicAsterisk]:
        output_list = []
        for row in self.row_objects:
            output_list += [x for x in row.asterisks_in_row]
        return output_list

    def match_numbers_to_asterisks(self) -> int:
        gear_ratio_total = 0
        
        rows_in_schematic = [x for x in self.row_objects]
        nums_adjacent_to_asterisk = []
        for row in rows_in_schematic:
            nums_adjacent_to_asterisk += [x for x in row.numbers_in_row if x.adjacent_to_asterisk]
        print(f"Total # of nums:  {len(nums_adjacent_to_asterisk)}")

        print(f"Total # of asterisks:  {len(self.all_asterisks)}")
        for asterisk in self.all_asterisks:
            sublist = []
            for num in nums_adjacent_to_asterisk:
                loc_dict = num.location_of_adjacent_asterisk
                if (loc_dict['row_num'] == asterisk.row_num) and (loc_dict['index'] == asterisk.index):
                    # print("found a submatch")
                    sublist.append(num)
            if len(sublist) == 2:
                gear_ratio = (sublist[0].num_int * sublist[1].num_int)
                print(f"FOUND A GEAR!  {sublist[0].num_int} * {sublist[1].num_int} = {gear_ratio}")
                gear_ratio_total += gear_ratio

        print(f"GEAR RATIO TOTAL:  {gear_ratio_total}")
        return gear_ratio_total


    def print_adjacent_rows(self) -> None:
        for row in self.row_objects:
            print(f"\nRow {row.row_num - 1}:    {row.previous_row}") if row.row_num > 0 else print('')
            print(f"*Row {row.row_num}*:  {row.row}")
            print(f"Row {row.row_num + 1}:    {row.next_row}") if row.row_num < len(row.schematic_list)-1 else print('END')\
        
    def print_adjacent_rows_part_two(self) -> None:
        for row in self.row_objects:
            print(f"\nRow {row.row_num - 1}:    {row.previous_row}") if row.row_num > 0 else print('START')
            print(f"*Row {row.row_num}*:  {row.row}")
            print(f"Row {row.row_num + 1}:    {row.next_row}") if row.row_num < len(row.schematic_list)-1 else print('END')

        
    
    

### TESTED & CONFIRMED:  THERE ARE NO NUMBERS WITH MORE THAN 3 DIGITS ####
### TESTED & CONFIRMED:  EVERY SCHEMATICNUMBER HAS TRUE OR FALSE IN ADJACENT_TO_ASTERISK

    
def part_two(puzzle_string: str) -> None:
    schematic = Schematic(puzzle_string)
    schematic.match_numbers_to_asterisks()


def part_one(puzzle_string: str) -> None:
    schematic = Schematic(puzzle_string)
    
    for row in schematic.row_objects:
        row.print_adjacent_rows_part_one()
        
    print(f"\nGRAND TOTAL:  {schematic.find_part_one_total()}")


def main():
    with open('./inputs/day3.txt') as file:
        puzzle_input_string = file.read()
        
    with open('./inputs/day3_test.txt') as file:
        test_input_string = file.read()

    with open('./inputs/day3_row13test.txt') as file:
        row13_test_input_string = file.read()
        
    # part_one(puzzle_input_string) 
    part_two(puzzle_input_string) 
    

if __name__ == '__main__':
    main()