import fileinput
from typing import List


def find_most_common_at_index(binary_list: List, index: int) -> str:
    """
    find the most common bit in the corresponding position (index) of all numbers in the list of binary numbers
    example:
        100
        010
        111
    gives:
        Most common on first position ([1, 0, 1]) is 1
        Most common on second position ([0, 1, 1]) is 1
        Most common on third position ([0, 0, 1]) is 0
    If 0 and 1 appear an equal amount of times, 'equal' is returned, otherwise 1 or 0 is returned as a string

    :param binary_list: List of binary numbers
    :param index: The position of interest
    :return: '1', '0' or 'equal'
    """
    sum = 0
    for binary in binary_list:
        sum += int(str(binary)[index])
    total = len(binary_list)
    most_common = 'equal'
    if sum > (total - sum):
        most_common = '1'
    elif sum < (total - sum):
        most_common = '0'
    return most_common


def find_oxygen_generator_rating(binary_list: List) -> str:
    """
    To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep
    only numbers in the binary list with that bit in that position. If 0 and 1 are equally common, keep values with a 1
    in the position being considered.

    - Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard
      numbers which do not match the bit criteria.
    - If you only have one number left, stop; this is the rating value for which you are searching.
    - Otherwise, repeat the process, considering the next bit to the right.

    :param binary_list: List of binary numbers
    :return: Binary number as string from the list that fits the criteria
    """
    max_index = len(binary_list[0])
    sub_list = binary_list
    oxygen_generator_rate = ''
    for index in range(0, max_index):
        most_common = find_most_common_at_index(sub_list, index)
        most_common = '1' if most_common == 'equal' else most_common
        sub_list = [b for b in sub_list if str(b)[index] == most_common]
        if len(sub_list) == 1:
            oxygen_generator_rate = sub_list[0]
            break
    return oxygen_generator_rate


def find_co2_scrubber_rating(binary_list: List) -> str:
    """
    To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and keep only
    numbers in the binary list with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in
    the position being considered.

    - Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard
      numbers which do not match the bit criteria.
    - If you only have one number left, stop; this is the rating value for which you are searching.
    - Otherwise, repeat the process, considering the next bit to the right.

    :param binary_list: List of binary numbers
    :return: Binary number as string from the list that fits the criteria
    """
    max_index = len(binary_list[0])
    sub_list = binary_list
    co2_scrubber_rate = ''
    for index in range(0, max_index):
        most_common = find_most_common_at_index(sub_list, index)
        least_common = '0' if most_common == '1' or most_common == 'equal' else '1'
        sub_list = [b for b in sub_list if str(b)[index] == least_common]
        if len(sub_list) == 1:
            co2_scrubber_rate = sub_list[0]
            break
    return co2_scrubber_rate


def process(input_list: List) -> int:
    """
    Use the binary numbers in your diagnostic report (input list) to calculate the oxygen generator rating and CO2
    scrubber rating, then multiply them together. What is the life support rating of the submarine? (Be sure to
    represent your answer in decimal, not binary.)

    :param input_list: binary numbers in your diagnostic report
    :return: product of the decimal representations of oxygen generator rating and co2 scrubber rating
    """
    oxygen_generator_rating = find_oxygen_generator_rating(input_list)
    co2_scrubber_rating = find_co2_scrubber_rating(input_list)

    return int(co2_scrubber_rating, 2) * int(oxygen_generator_rating, 2)


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
