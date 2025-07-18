def ingest_input_string() -> list[str]:
    ''' Takes the raw input string and splits it via new-line characters. '''
    with open('./inputs/day5.txt') as file:
        input_string = file.read()

    return input_string.split(sep='\n')

def ingest_test_string() -> list[str]:
    ''' Takes the raw test string and splits it via new-line characters. '''
    with open('./inputs/day5_test.txt') as file:
        input_string = file.read()

    return input_string.split(sep='\n')

def find_lines_with_titles(input_string_split: list[str]) -> list[int]:
    ''' Takes split input string from `ingest_input_string()` and returns a list of
        line numbers for each line with a map title. '''
    lines_with_titles = []
    for i, line in enumerate(input_string_split):
        if ":" in line: 
            lines_with_titles.append(i)
    return lines_with_titles

def split_map_coordinates(input_string_split: list[str], lines_with_titles: list[int]) -> list[list[str|int]]:
    list_of_map_string_lists: list[list[str]] = []
    for i, line_num in enumerate(lines_with_titles):
        start = line_num
        end = lines_with_titles[i+1] if i < (len(lines_with_titles)-1) else (len(input_string_split)-1)
        map_string_list = [x for x in input_string_split[start:end] if x != '']
        list_of_map_string_lists.append(map_string_list)

    output_list = []
    for map_string_list in list_of_map_string_lists[1:len(list_of_map_string_lists)]:
        title_split = map_string_list[0].split(sep="-")
        input_type = title_split[0]
        output_type = (title_split[2].split(sep=' '))[0]
        sub_list = []
        for row in map_string_list[1:len(map_string_list)]:
            sub_list.append([int(x) for x in row.split(' ')])
        output_list.append([input_type, output_type, sub_list])
        
    return [x for x in output_list if len(x) > 0]

def process_maps() -> list[list[str|int]]:
    input_string_split = ingest_input_string()
    lines_with_titles = find_lines_with_titles(input_string_split)
    map_coordinate_lists = split_map_coordinates(input_string_split, lines_with_titles)

    return map_coordinate_lists

def process_seeds() -> list[int]:
    input_string_split = ingest_input_string()
    seeds_string = input_string_split[0]
    seeds_list = seeds_string.split(sep=' ')
    return [int(x) for x in seeds_list[1:len(seeds_list)]]

def process_test_maps() -> list[list[str|int]]:
    input_string_split = ingest_test_string()
    lines_with_titles = find_lines_with_titles(input_string_split)
    map_coordinate_lists = split_map_coordinates(input_string_split, lines_with_titles)

    return map_coordinate_lists

def process_test_seeds() -> list[int]:
    input_string_split = ingest_test_string()
    seeds_string = input_string_split[0]
    seeds_list = seeds_string.split(sep=' ')
    return [int(x) for x in seeds_list[1:len(seeds_list)]]

if __name__ == "__main__":
    print("This is a module, not a script.")