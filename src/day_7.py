import fileinput
from typing import List


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    input_list.sort()
    median = input_list[round(len(input_list) / 2)]
    total = sum([abs(n - median) for n in input_list])
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    lines = [int(n) for n in lines[0].split(',')]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
