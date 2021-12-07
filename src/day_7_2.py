import fileinput
from math import floor, ceil
from typing import List


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    floor_mean = floor(sum(input_list) / len(input_list))
    floor_total = sum([sum(range(0, abs(n - floor_mean) + 1)) for n in input_list])

    ceil_mean = ceil(sum(input_list) / len(input_list))
    ceil_total = sum([sum(range(0, abs(n - ceil_mean) + 1)) for n in input_list])

    total = floor_total if floor_total < ceil_total else ceil_total
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    lines = [int(n) for n in lines[0].split(',')]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
