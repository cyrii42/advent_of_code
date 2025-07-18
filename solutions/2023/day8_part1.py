'''--- Day 8: Haunted Wasteland ---'''

with open('./inputs/day8.txt') as file:
    line_list = file.read().split(sep='\n')
    
instructions_str = line_list.pop(0)
maps_dict = {row[0:3]: (row[7:10], row[12:15]) for row in line_list[2:]}


total = 0
next_location = 'AAA'
found = False
while found == False:
    for dir in instructions_str:
        print(f"Testing {dir}...")
        total += 1
        current_location = maps_dict[next_location]
        if dir == 'L':
            next_location = current_location[0]
        else:
            next_location = current_location[1]
            
        if next_location == 'ZZZ':
            print(f"Found ZZZ in {total} steps!")
            found = True
            break
        

# if __name__ == '__main__':
#     main()