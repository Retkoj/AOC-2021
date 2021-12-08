import fileinput
from typing import List


LETTERS = {
0: 'cagedb',
    1: 'ab',
    2: 'gcdfa',
    3: 'fbcad',
    4: 'eafb',
    5: 'cdfbe',
    6: 'cdfgeb',
    7: 'dab',
    8: 'acedgfb',
    9: 'cefabd'
}


def contains_letters(number_in_letters, mapping):
    """
    Map a lettercode to a number
    Returns number as string as to concatenate later
    :param number_in_letters: string
    :param mapping: mapping of letter combinations to numbers
    :return: single integer as string
    """
    final_number = ''
    for key, value in mapping.items():
        if sorted(number_in_letters) == sorted(value):
            final_number += str(key)
            break
    return final_number


def get_mapping(all_numbers):
    """
    For each display, you watch the changing signals for a while, make a note of all ten unique signal patterns you see,
    and then write down a single four digit output value (your puzzle input). Using the signal patterns, you should be
    able to work out which pattern corresponds to which digit.

    :param all_numbers: List with numbers as strings of display locations (e.g. 'abd')
    :return: mapping of single integers to string of letters in a dict
    """
    mapping = {}
    mapping[1] = [n for n in all_numbers if len(n) == 2][0]
    mapping[4] = [n for n in all_numbers if len(n) == 4][0]
    mapping[7] = [n for n in all_numbers if len(n) == 3][0]
    mapping[8] = [n for n in all_numbers if len(n) == 7][0]

    # len 6 = 6, 9, 0
    six_length_numbers = [n for n in all_numbers if len(n) == 6]
    mapping[6] = [n for n in six_length_numbers if (mapping[1][0] not in n or mapping[1][1] not in n)][0]
    mapping[9] = [n for n in six_length_numbers if len(set(mapping[4]) & set(n)) == len(mapping[4])][0]
    mapping[0] = [n for n in six_length_numbers if (set(n) not in [set(mapping[6]), set(mapping[9])])][0]

    # len 5 = 5, 3, 2
    five_length_numbers = [n for n in all_numbers if len(n) == 5]
    mapping[3] = [n for n in five_length_numbers if len(set(mapping[1]) & set(n)) == len(mapping[1])][0]
    mapping[5] = [n for n in five_length_numbers if len(set(mapping[4]) & set(n)) == 3 and set(n) != set(mapping[3])][0]
    mapping[2] = [n for n in five_length_numbers if (set(n) not in [set(mapping[3]), set(mapping[5])])][0]

    return mapping


def process(input_list: List) -> int:
    """
    - Get the mapping from each unique ten digit part of a line
    - use mapping on second, output part, of the line (i.e. following the '|')
    - Sum the output numbers together

    :param input_list: e.g. acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
    :return:
    """
    total = 0
    for line in input_list:
        first_part = [n.strip() for n in line.split('|')[0].split()]
        mapping = get_mapping(first_part)

        second_part = [n.strip() for n in line.split('|')[1].split()]
        concatenated_number = ''
        for number in second_part:
            concatenated_number += contains_letters(number, mapping)
        total += int(concatenated_number)
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
