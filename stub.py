import fileinput
from typing import List


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
