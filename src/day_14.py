import fileinput
import string
from collections import Counter
from typing import List

from setuptools._vendor.more_itertools import pairwise


class PolymerBuilder:
    """The submarine manual contains instructions for finding the optimal polymer formula; specifically, it offers a
    polymer template and a list of pair insertion rules (your puzzle input). You just need to work out what polymer
    would result after repeating the pair insertion process a few times."""
    def __init__(self, start_polymer, polymer_mapping, max_depth):
        self.start_polymer = start_polymer

        self.polymer_letter_mapping = {}
        self.polymer_graph_mapping = {}
        self.build_polymer_mapping(polymer_mapping)

        self.polymer_counts = {letter: 0 for letter in string.ascii_uppercase}
        self.max_depth = max_depth

    def process_all(self):
        for letter in self.start_polymer:  # add the initial letters to the count
            self.polymer_counts[letter] += 1
        polymer_dict = dict(Counter([left + right for left, right in list(pairwise(self.start_polymer))]))
        for d in range(0, self.max_depth):
            polymer_dict = self.get_next_polymers(polymer_dict)

    def get_next_polymers(self, current_polymers: dict) -> dict:
        next_polymers = {}
        for polymer, count in current_polymers.items():
            letter_to_add = self.polymer_letter_mapping[polymer]
            self.polymer_counts[letter_to_add] += count
            for p in self.polymer_graph_mapping[polymer]:
                next_polymers[p] = next_polymers.get(p, 0) + count
        return next_polymers

    def calculate_score(self):
        filtered_zeros = {letter: count for letter, count in self.polymer_counts.items() if count != 0}
        highest = int(sorted(filtered_zeros.values(), reverse=True)[0])
        lowest = int(sorted(filtered_zeros.values())[0])
        print(filtered_zeros)
        return highest - lowest

    def build_polymer_mapping(self, polymer_mapping):
        for line in polymer_mapping:
            left, right = line.split(' -> ')
            self.polymer_letter_mapping[left] = right
            first_letter, second_letter = list(left)
            self.polymer_graph_mapping[left] = [first_letter + right, right + second_letter]


def process(input_list: List) -> {}:
    """
    The first line is the polymer template - this is the starting point of the process.
    The following section defines the pair insertion rules. A rule like AB -> C means that when elements A and B
    are immediately adjacent, element C should be inserted between them. These insertions all happen simultaneously.
    :param input_list:
    :return:
    """
    all_scores = {}
    for i in [10, 40]:
        polymer_builder = PolymerBuilder(input_list[0], input_list[2:], max_depth=i)
        polymer_builder.process_all()
        all_scores[i] = polymer_builder.calculate_score()
    return all_scores


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output 10: {output[10]}, output 40: {output[40]}')
