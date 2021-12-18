import ast
import fileinput
import re
from math import floor, ceil


def find_exploding_pair(snail_number):
    chunk_parts = list(snail_number)
    nested_count = 0
    nested_pair = ''
    nested_pair_index = float('inf')
    for index, character in enumerate(chunk_parts):
        if character == '[':
            nested_count += 1
        if nested_count > 4:
            nested_pair_index = index if index < nested_pair_index else nested_pair_index
            nested_pair += character
        if character == ']':
            nested_count -= 1
        if nested_count <= 4 and len(nested_pair) > 0:
            break
    nested_pairs = re.findall(r'\[\d+,\d+\]', nested_pair)

    left_nested_pair = None
    if len(nested_pairs) > 0:
        left_nested_pair = nested_pairs[0]
        nested_pair_index += nested_pair.find(left_nested_pair)  # add index discrepancy to first pair
    print(f"exploding pair: {left_nested_pair}, at index: {nested_pair_index}")
    return left_nested_pair, nested_pair_index


def explode_pair(snail_number, exploding_pair, index_exploding_pair):
    lhs, rhs = ast.literal_eval(exploding_pair)

    left_side_string = snail_number[0:index_exploding_pair]
    number_to_left = re.findall(r'\d+', left_side_string)
    if len(number_to_left) > 0:
        number_to_left = number_to_left[-1]
        add_index = left_side_string.rindex(number_to_left)
        new_number = int(number_to_left) + int(lhs)
        left_side_string = left_side_string[0:add_index] + \
                           str(new_number) + \
                           left_side_string[add_index + len(str(number_to_left)): index_exploding_pair]

    right_side_string = snail_number[index_exploding_pair + len(exploding_pair):]
    number_to_right = re.findall(r'\d+', right_side_string)
    if len(number_to_right) > 0:
        number_to_right = number_to_right[0]
        add_index = right_side_string.index(number_to_right)
        new_number = int(number_to_right) + int(rhs)
        right_side_string = right_side_string[0:add_index] + \
                           str(new_number) + \
                           right_side_string[add_index + len(str(number_to_right)):]

    new_snail_number = left_side_string + '0' + right_side_string
    print(f"After explosion: {new_snail_number}")
    return new_snail_number


def requires_split(snail_number):
    double_digits = re.findall(r'\d{2,}', snail_number)
    split_index = None
    split_number = None
    if len(double_digits) > 0:
        split_number = int(double_digits[0])
        split_index = snail_number.index(double_digits[0])
    print(f"Double digit {split_number} at index {split_index}")
    return split_index, split_number


def split_snail_number(snail_number, split_index, split_number):
    insert_pair = f"[{floor(split_number / 2)},{ceil(split_number / 2)}]"
    new_snail_number = snail_number[0:split_index] + insert_pair + snail_number[split_index + len(str(split_number)):]
    print(f"after split: {new_snail_number}")
    return new_snail_number


def reduce(snail_number: str) -> str:
    """

    :param snail_number:
    :return:
    """
    prev_snail_number = snail_number
    while True:
        action = False
        new_snail_number = prev_snail_number
        exploding_pair, exploding_index = find_exploding_pair(new_snail_number)
        if exploding_pair:
            action = True
            new_snail_number = explode_pair(new_snail_number, exploding_pair, exploding_index)
        else:
            split_index, split_number = requires_split(new_snail_number)
            if split_index:
                action = True
                new_snail_number = split_snail_number(new_snail_number, split_index, split_number)

        if not action:
            break
        prev_snail_number = new_snail_number
    return new_snail_number


def calculate_magnitude(final_number):
    final_numbers_list = ast.literal_eval(final_number)
    total_sum = reduce_sum(final_numbers_list)
    return total_sum


def reduce_sum(sub_list):
    lhs, rhs = sub_list
    if type(lhs) == list:
        lhs = reduce_sum(lhs)
    if type(rhs) == list:
        rhs = reduce_sum(rhs)
    return (3 * lhs) + (2 * rhs)


def process(input_list: list):
    index = 1
    lhs = reduce(input_list[0])
    while index < len(input_list):
        rhs = reduce(input_list[index])
        snail_number = f'[{lhs},{rhs}]'
        print(f"after addition: {snail_number}")
        lhs = reduce(snail_number)
        index += 1
    final_sum = lhs
    print(f"final sum: {lhs}")
    return calculate_magnitude(final_sum)


if __name__ == '__main__':
    # lines = {i: ast.literal_eval(l.strip('\n')) for i, l in enumerate(fileinput.input())}
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines)
    output = process(lines)
    print(f'Output: {output}')
