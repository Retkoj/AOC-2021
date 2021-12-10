from collections import deque
import fileinput
from math import floor
from typing import List

from src.day_10 import COUNTERPART

COMPLETION_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}


def process(input_list: List) -> int:
    """
    discard the corrupted lines. The remaining lines are incomplete.

    Incomplete lines don't have any incorrect characters - instead, they're missing some closing characters at the end
    of the line. To repair the navigation subsystem, you just need to figure out the sequence of closing characters
    that complete all open chunks in the line.

    You can only use closing characters (), ], }, or >), and you must add them in the correct order so that only legal
    pairs are formed and all chunks end up closed.

    Start with a total score of 0. Then, for each character, multiply the total score by 5 and then increase the total
    score by the point value given for the character in the COMPLETION_SCORE table

    Find the completion string for each incomplete line, score the completion strings, and sort the scores.
    What is the middle (median) score?

    :param input_list: List of strings, e.g. ['<{([{{}}[<[[[<>{}]]]>[]]', '<{([([[(<>()){}]>(<<{{', ...]
    :return: total sum of the completion syntax score
    """
    all_completion_scores = []
    for line in input_list:
        chunk_parts = list(line)
        left_side = deque()
        corrupt_line = False
        # Check for, and skip, corrupted lines:
        for character in chunk_parts:
            if character in COUNTERPART.keys():
                left_side.append(character)
            elif character in COUNTERPART.values():
                left_character = left_side.pop()
                if COUNTERPART[left_character] != character:
                    corrupt_line = True
                    break

        if not corrupt_line:
            line_completion_score = 0
            for _ in range(0, len(left_side)):
                left_character = left_side.pop()
                right_character = COUNTERPART[left_character]
                line_completion_score *= 5
                line_completion_score += COMPLETION_SCORE[right_character]
            all_completion_scores.append(line_completion_score)

    middle_index = floor(len(all_completion_scores) / 2)
    return sorted(all_completion_scores)[middle_index]


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
