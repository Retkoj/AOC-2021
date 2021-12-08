import fileinput
from typing import List


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    for line in input_list:
        second_part = [n.strip() for n in line.split('|')[1].split()]
        for number in second_part:
            if len(number) in [2, 4, 3, 7]:
                total += 1
    return total


if __name__ == '__main__':
    """
    As your submarine slowly makes its way through the cave system, you notice that the four-digit seven-segment 
    displays in your submarine are malfunctioning; they must have been damaged during the escape. You'll be in a lot of 
    trouble without them, so you'd better figure out what's wrong.
    """
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
