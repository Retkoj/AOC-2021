import fileinput
from typing import List

from Submarine import Submarine


def process(input_list: List) -> int:
    """
    - down X increases your aim by X units.
    - up X decreases your aim by X units.
    - forward X does two things:
        - It increases your horizontal position by X units.
        - It increases your depth by your aim multiplied by X.
    :param input_list: list of strings containing the direction and X/steps, e.g. 'forward 5', 'down 3'
    :return: depth * horizontal position
    """
    depth = 0
    horizontal = 0
    aim = 0
    for move in input_list:
        direction, steps = move.split(' ')
        if direction == 'forward':
            horizontal += int(steps)
            depth += (int(steps) * aim)
        elif direction == 'up':
            aim -= int(steps)
        elif direction == 'down':
            aim += int(steps)

    return depth * horizontal


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')

    yellow_submarine = Submarine()
    yellow_submarine.multiple_moves(lines)
    horizontal, depth, _ = yellow_submarine.get_position()
    submarine_output = horizontal * depth
    print(f'Submarine output: {submarine_output}')
