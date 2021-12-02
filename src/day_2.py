import fileinput
from typing import List


def process(input_list: List) -> int:
    """
    - forward X increases the horizontal position by X units.
    - down X increases the depth by X units.
    - up X decreases the depth by X units.
    :param input_list: list of strings containing the direction and X/steps, e.g. 'forward 5', 'down 3'
    :return: depth * horizontal position
    """
    depth = 0
    horizontal = 0
    for move in input_list:
        direction, steps = move.split(' ')
        if direction == 'forward':
            horizontal += int(steps)
        elif direction == 'up':
            depth -= int(steps)
        elif direction == 'down':
            depth += int(steps)

    return depth * horizontal


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
