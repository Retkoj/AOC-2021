from collections import deque
import fileinput
from typing import List

CORRUPTION_SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

COUNTERPART = {
    """
    If a chunk opens with (, it must close with ).
    If a chunk opens with [, it must close with ].
    If a chunk opens with {, it must close with }.
    If a chunk opens with <, it must close with >.
    """
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>'
}


def process(input_list: List) -> int:
    """
    A corrupted line is one where a chunk closes with the wrong character - that is, where the characters it opens and
    closes with do not form one of the four legal pairs in COUNTERPART.
    Stop at the first incorrect closing character on each corrupted line.
    To calculate the syntax error score for a line, take the first illegal character on the line and look it up in
    the CORRUPTION_SCORE table.

    Find the first illegal character in each corrupted line of the navigation subsystem.
    What is the total sum of the syntax error score for those errors?

    :param input_list: List of strings, e.g. ['<{([{{}}[<[[[<>{}]]]>[]]', '<{([([[(<>()){}]>(<<{{', ...]
    :return: total sum of the syntax error score
    """
    total = 0
    for line in input_list:
        chunk_parts = list(line)
        left_side = deque()

        for character in chunk_parts:
            if character in COUNTERPART.keys():
                left_side.append(character)
            elif character in COUNTERPART.values():
                left_character = left_side.pop()
                if COUNTERPART[left_character] != character:
                    total += CORRUPTION_SCORE[character]
                    break
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
