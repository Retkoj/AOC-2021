import fileinput
from typing import List

from src.day_3_2 import find_most_common_at_index


def find_gamma_rate(binary_list: List) -> str:
    """
    Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all
    numbers in the diagnostic report.

    :param binary_list: List of binary numbers
    :return: gamma rate as binary string
    """
    gamma_rate = ''
    max_index = len(binary_list[0])
    for index in range(0, max_index):
        gamma_rate += find_most_common_at_index(binary_list, index)
    return gamma_rate


def find_epsilon_rate(binary_list: List) -> str:
    """
    The epsilon rate can be determined by finding the the least common bit in the corresponding position of all
    numbers in the diagnostic report. i.e. the inverse of the most common bit

    :param binary_list: List of binary numbers
    :return: epsilon rate as binary string
    """
    epsilon_rate = ''
    max_index = len(binary_list[0])
    for index in range(0, max_index):
        most_common = find_most_common_at_index(binary_list, index)
        least_common = '1' if most_common == '0' else '0'
        epsilon_rate += least_common
    return epsilon_rate


def process(input_list: List) -> int:
    """
    Use the binary numbers in your diagnostic report to calculate the gamma rate and epsilon rate, then multiply them
    together. What is the power consumption of the submarine? (Be sure to represent your answer in decimal, not binary.)

    :param input_list: List of binary numbers
    :return: product of the decimal representations of gamma rate and epsilon rate
    """
    epsilon_rate = find_epsilon_rate(input_list)
    gamma_rate = find_gamma_rate(input_list)

    return int(gamma_rate, 2) * int(epsilon_rate, 2)


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
