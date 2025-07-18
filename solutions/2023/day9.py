'''--- Day 9: Mirage Maintenance ---'''

class ValueHistory():
    def __init__(self, input_str: str):
        self.input_str = input_str
        self.history_line_one = [int(x) for x in self.input_str.split()]
        self.sequence_list = self.generate_sequence_list()
        self.next_value = self.extrapolate_next_value()
        self.previous_value = self.extrapolate_previous_value()

    def generate_sequence_list(self) -> list[str]:
        sequence_list = [self.history_line_one]
        while set(sequence_list[-1]) != {0}:
            current_sequence = sequence_list[-1]
            next_sequence = []
            for i in range(len(current_sequence)):
                if i == 0:
                    continue
                else:
                    next_sequence.append(current_sequence[i] - current_sequence[i-1])
            sequence_list.append(next_sequence)
        return sequence_list
                 
    def extrapolate_next_value(self) -> int:
        output_list = []
        for i in range(len(self.sequence_list)-1, -1, -1):
            if i == 0:
                continue
            else:
                output_list.append(self.sequence_list[i][-1] + self.sequence_list[i-1][-2])
        return sum(output_list)

    def extrapolate_previous_value(self) -> int:
        output_list = []
        new_num = 0
        for i in range(len(self.sequence_list)-1, 0, -1):
            new_num = self.sequence_list[i-1][0] - new_num
            output_list.append(new_num)
        return output_list[-1]
    

def main():
    with open('./inputs/day9.txt') as file:
       line_list = file.read().strip().split(sep='\n')  

    dataset = [ValueHistory(x) for x in line_list]

    print(f"Part One Answer:  {sum([history.next_value for history in dataset])}")
    print(f"Part Two Answer:  {sum([history.previous_value for history in dataset])}")

if __name__ == '__main__':
    main()