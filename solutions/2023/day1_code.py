'''--- Day 1: Trebuchet?! ---'''

import day1_input

input_list = day1_input.day1_input

test_list_1 = ['1abc2', 'pqr3stu8vwx', 'a1b2c3d4e5f', 'treb7uchet']
    
def part_one():
    total = 0
    for input_string in input_list:
        num_char_list = []
        
        for char in input_string:
            if char.isnumeric():
                num_char_list.append(char)

        n = len(num_char_list)

        if n == 0:
            num_int = 0
        elif n == 1:
            num_int = int(num_char_list[0] + num_char_list[0])
        else:
            num_int = int(num_char_list[0] + num_char_list[n-1])

        # print(f"Input string:  {input_string} - {num_char_list} - {num_int}")

        total = total + num_int

    print(f"Day 1, part 1:  {total}")


num_dict = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

num_words_list = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
]

test_list_2 = [
    'two1nine',
    'eightwothree',
    'abcone2threexyz',
    'xtwone3four',
    '4nineeightseven2',
    'zoneight234',
    '7pqrstsixteen',
]


def part_two():
    total = 0
    # Go forwards from beginining of string
    for input_string in input_list:
        print(f"Current test string:  {input_string} (length:  {len(input_string)})")
        num_char_list = []
        for i in range(0, (len(input_string)-1)):   # loop from 0 through one minus the length of input_string
            test_char = input_string[i]  # pull the ith character 
            substring = input_string[:(i+1)]   # pull the 0th through ith characters
            # print(f"Forwards test char: {test_char}")
            # print(f"Forwards substring: {substring}")
            if test_char.isnumeric():
                print(f"Found \'{test_char}\' in \'{substring}\'")
                num_char_list.append(test_char)
                break
            elif any(num_string in substring for num_string in num_dict.keys()):
                for key, value in num_dict.items():
                    if key in substring:
                        print(f"Found \'{key}\' in \'{substring}\'")
                        num_char_list.append(value)
                        break
                break
        print(f"First num char:  {num_char_list}")

    # Go backwards from end of string
        for i in range(-1, -abs(len(input_string)+1), -1):  # loop from -1 through the absolute negative value of len(input_string), stepping by -1
            end = len(input_string)
            test_char = input_string[i]  # pull the ith character (going backwards)
            substring = input_string[end:i-1:-1][::-1]    # pull the last through the ith character (going backwards), then reverse the string again
            # print(f"Backwards test char: {test_char}")
            # print(f"Backwards substring: {substring}") 
            if test_char.isnumeric():
                print(f"Found \'{test_char}\' in \'{substring}\'")
                num_char_list.append(test_char)
                break
            elif any(num_string in substring for num_string in num_words_list):
                for key, value in num_dict.items():
                    if key in substring:
                        print(f"Found \'{key}\' in \'{substring}\'")
                        num_char_list.append(value)
                        break
                break
        print(f"Both num chars:  {num_char_list}")

        n = len(num_char_list)

        if n == 0:
            num_int = 0
        elif n == 1:
            num_int = int(num_char_list[0] + num_char_list[0])
        else:
            num_int = int(num_char_list[0] + num_char_list[n-1])

        total = total + num_int

    print(f"Day 1, part 2:  {total}")




if __name__ == "__main__":
    part_one()
    part_two()