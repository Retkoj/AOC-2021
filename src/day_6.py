import copy
import fileinput
from typing import List

import tqdm as tqdm


def procreate(fish_list):
    tmp_list = copy.deepcopy(fish_list)
    for i, fish in enumerate(fish_list):
        if fish == 0:
            tmp_list[i] = 6
            tmp_list.append(8)
        elif fish > 0:
            tmp_list[i] = fish - 1
    return tmp_list


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    fish_list = input_list
    for r in tqdm.tqdm(range(0, 80)):
        fish_list = procreate(fish_list)
    return len(fish_list)


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    lines = [int(n) for n in lines[0].split(',')]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
