import fileinput
from typing import List


def get_windowed_sum(input_list: List) -> List:
    """
    Get a windowed sum over the range of three numbers, return the new list
    Example:
        199  A
        200  A B
        208  A B C
        210    B C D
        200  E   C D
        207  E F   D
        240  E F G
        269    F G H
        260      G H
        263        H
    Returns:
        [607, 618, 618, 617, 647, 716, 769, 792]
    :param input_list:
    :return:
    """
    return [sum(input_list[i:i + 3]) for i in range(0, len(input_list) - 2)]


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
    windowed_list = get_windowed_sum(lines)
    print(windowed_list[0:10])
    output = count_increases(windowed_list)
    print(f'Output: {output}')
