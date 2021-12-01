import fileinput
from typing import List


def count_increases(input_list: List) -> int:
    """
    Count the number of times a number in a list is increased compared to the previous number.
    First number in the list doesn't have a previous number
    :param input_list:
    :return: Number of increases counted
    """
    total = 0
    previous_num = None
    for i, number in enumerate(input_list):
        if i > 0:
            if number > previous_num:
                total += 1
        previous_num = number

    return total


if __name__ == '__main__':
    lines = [int(i.strip('\n')) for i in fileinput.input()]
    print(lines[0:10])
    output = count_increases(lines)
    print(f'Output: {output}')
