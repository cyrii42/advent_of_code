'''--- Day 3: Gear Ratios ---'''

import pandas as pd

from day3_input import day3_input_full as input_string
from day3_input import day3_input_list as input_list

input_string = input_string.replace('\n','')
symbol_list = [x for x in set(input_string) if x.isnumeric() == False and x != '.']
input_series = pd.Series(input_list)

test_list = ['467..114..', '...*......', '..35..633.', '......#...', '617*......', '.....+.58.', '..592.....', '......755.', '...$.*....', '.664.598..']
test_string = ("467..114.....*........35..633.......#...617*...........+.58...592...........755....$.*.....664.598..")
test_series = pd.Series(test_list)


def find_numbers_in_schematic(schematic: list[str]) -> list[tuple[int, str, int, int]]:
    ''' Takes a schematic (in a list of strings) and finds the numbers that can be found in that line.  

    Outputs a list of lists of tuples.  Each sub-list contains a number of tuples, and each tuple contains:

    - (1)  an integer corresponding to the line number in the schematic;
    - (2)  a string containing the number itself;
    - (3)  an integer corresponding to the starting index for the number; and
    - (4)  an integer corresponding to the ending index for the number.'''

    line_list = []
    for n, line in enumerate(schematic):
        output_list = []
        for i, char in enumerate(line):
            if char.isnumeric() and (line[i-1].isnumeric() == False):
                num_string = char
                for x in range(i+1,(len(line)-1)):
                    if line[x].isnumeric():
                        num_string = num_string + line[x]
                        continue
                    else:
                        break
                output_list.append((n, num_string, i, i+len(num_string)))
            else:
                continue
        line_list.append(output_list)
    return line_list


def check_symbol(test_char: str) -> bool:
    return any([test_char == x for x in symbol_list])
   
            

def test_number_adjacency(num_tuple: tuple[str, int, int], schematic: list[str]) -> int:
    ''' Takes a tuple from `find_numbers_in_string()` and determines whether the corresponding number
        is adjacent to a symbol.'''
    line_num = num_tuple[0]
    final_index = len(schematic[line_num]) - 1
    num_string = num_tuple[1]
    start = num_tuple[2]
    start_minus_one = (0 if start == 0 else (start - 1))
    end = num_tuple[3]
    end_plus_one = (final_index if end == final_index else (end + 1))
    # print(f"start:  {start}  -  end: {end}")
    # print(f"start_minus_one:  {start_minus_one}  -  end_plus_one: {end_plus_one}")
    # print(f"Final index:  {final_index}")

    same_line = schematic[line_num]
    previous_line = schematic[line_num - 1]
    next_line = '' if line_num == len(schematic)-1 else schematic[line_num + 1]

    # print(f"Start: {start}; End: {end}")
    symbols_to_check = (
        same_line[start_minus_one:end_plus_one] +
        previous_line[start_minus_one:end_plus_one] +
        next_line[start_minus_one:end_plus_one]
    )

    # print('')
    # print(f"TUPLE:  {num_tuple}")
    # print(f"{previous_line} \n{same_line} \n{next_line}")
    # print(f"SYMBOLS TO CHECK: {symbols_to_check} - {any([(x in symbol_list) for x in symbols_to_check])}")

    if any([(x in symbol_list) for x in symbols_to_check]):
        return int(num_string)
    else:
        return 0
            


    
list_of_lists = find_numbers_in_schematic(input_list)
asdf = []
for list in list_of_lists:
    asdf = asdf + [int(x[1]) for x in list]
print(len(asdf))


num_list = []
for list in list_of_lists:
    for tuple in list:
        num_list.append(test_number_adjacency(tuple, input_list))

print(len([x for x in num_list if x > 0]))

print(f"So, there are {len(asdf) - len([x for x in num_list if x > 0]):,} numbers that aren't adjacent to a symbol...")






# for x in test_list:
#     print(x)
# for list in list_of_lists:
#     print(list)
#     print([test_number_adjacency(x, test_list) for x in list])



# print(f"\nIs star in star?  {'*' in symbol_list}")


# nums_with_adjacency = []
# for list in list_of_lists[0:10]:
#     for tuple in list:
#         print(f"Checking tuple {tuple}:  {test_number_adjacency(tuple)}")




# for tuple in list_of_lists[0]:
#         line_num = tuple[0]
#         num_string = tuple[1]
#         start = tuple[2]
#         end = tuple[3]

#         same_line = input_list[line_num]
#         previous_line = input_list[line_num - 1]
#         next_line = input_list[line_num + 1]

#         symbols_to_check = [
#             same_line[start-1],
#             same_line[end+1],
#             previous_line[(start-1):(end+1)],
#             next_line[(start-1):(end+1)]
#         ]

#         print(f"TUPLE:  {tuple}")
#         print(f"{previous_line} \n{same_line} \n{next_line}")
#         print(symbols_to_check)
#         print('')








# def find_numbers_in_string_pandas(input_series: pd.Series) -> pd.DataFrame:
#     ''' Takes a schematic in a Pandas Series and finds the numbers that can be found in that line.  

#     Outputs a DataFrame with the following columns:

#     - (1) the line string
#     - (2) a "num tuple":
#         - (a) a string containing the number itself;
#         - (b) an integer corresponding to the starting index for the number; and
#         - (c) an integer corresponding to the ending index for the number.
#     '''

#     tuples_series = input_series.apply(find_numbers_in_string)

#     return pd.DataFrame({'line_string': input_series, 'num_tuple': tuples_series})

# df = find_numbers_in_string_pandas(test_series)
# print(df)




# for line in test_list:
#     print(f"Testing line:  \'{line}\'")
#     print(find_numbers_in_string(line))
    


            
        



def get_stats() -> None:   
    print(f"# of lines in input list:  {len(input_list)}")
    print(f"# of characters in each line:  {len(input_list[0])}")
    print(f"# of total characters in input string:  {len(input_string)}")  
    print(f"Unique symbols in input string:  {symbol_list}")
    
    print(f"\n# of lines in test list:  {len(test_list)}")
    print(f"# of characters in each line:  {len(test_list[0])}")
    print(f"# of total characters in test string:  {len(test_string)}")
    

def main():
    get_stats()

if __name__ == '__main__':
    main()








# def find_numbers_in_string(line: str) -> list[tuple[str, int, int]]:
#     ''' Takes a single line from a schmatic and finds the numbers that can be found in that line.  

#     Outputs a list of tuples, each of which contains:

#     - (1)  a string containing the number itself;
#     - (2)  an integer corresponding to the starting index for the number; and
#     - (3)  an integer corresponding to the ending index for the number.
#     '''

#     output_list = []
#     for i, char in enumerate(line):
#         if char.isnumeric() and (line[i-1].isnumeric() == False):
#             num_string = char
#             for x in range(i+1,(len(line)-1)):
#                 if line[x].isnumeric():
#                     num_string = num_string + line[x]
#                     continue
#                 else:
#                     break
#             output_list.append((num_string, i, i+len(num_string)))
#         else:
#             continue

#     return(output_list)





# def find_number_indices(line: str) -> list[int]:
#     ''' Takes a single line from a schematic and returns a list of indices 
#         at which integers can be found in the line.'''

#     return [i for (i, char) in enumerate(line) if char.isnumeric()]