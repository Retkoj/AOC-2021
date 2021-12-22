import fileinput
from collections import Counter
from copy import deepcopy
from itertools import permutations
from typing import List

import numpy as np


class DiracDice:
    def __init__(self, start_position_one, start_position_two):
        self.position_p_one = start_position_one - 1  # get index
        self.score_p_one = 0
        self.p_one_wins = 0
        self.position_p_two = start_position_two - 1  # get index
        self.score_p_two = 0
        self.p_two_wins = 0

        self.possible_scores = [sum(list(throws)) for throws in set(permutations([1, 1, 1, 2, 2, 2, 3, 3, 3], 3))]
        self.possible_scores_counts = Counter(self.possible_scores)

        self.board_values = np.array(range(1, 11))
        self.winning_score = 21

    def play_simple(self):
        for score, factor in self.possible_scores_counts.items():
            print(f"running {score} with factor {factor}")
            self.single_round_explicit(score, factor, 3, 1, 0, 0, 1)
    # def play_simple(self):
    #     for score, factor in self.possible_scores_counts.items():
    #         print(f"running {score} with factor {factor}")
    #         self.improve(score, factor, 3, 7, 0, 0, 1)

    def make_move(self, dice_value, pos, score):
        added_score = self.board_values.take(pos + dice_value, mode='wrap')
        new_pos = np.where(self.board_values == added_score)[0][0]  # index of score
        new_score = score + added_score
        return new_score, new_pos

    def single_round_explicit(self, added_dice_value, factor, pos_p_one, pos_p_two, score_p_one, score_p_two, n_rounds):
        winner = False
        if n_rounds % 2 == 0:
            new_score_p_two, new_pos_p_two = self.make_move(added_dice_value, pos_p_two, score_p_two)
            new_score_p_one, new_pos_p_one = score_p_one, pos_p_one
            if new_score_p_two >= self.winning_score:
                self.p_two_wins += factor
                winner = True
        else:
            new_score_p_one, new_pos_p_one = self.make_move(added_dice_value, pos_p_one, score_p_one)
            new_score_p_two, new_pos_p_two = score_p_two, pos_p_two
            if new_score_p_one >= self.winning_score:
                self.p_one_wins += factor
                winner = True

        if not winner:
            new_n_rounds = n_rounds + 1
            for score, next_factor in self.possible_scores_counts.items():
                new_factor = factor * next_factor
                self.single_round_explicit(score, new_factor, new_pos_p_one, new_pos_p_two, new_score_p_one,
                                           new_score_p_two, new_n_rounds)

    def improve(self, added_dice_value, factor, pos_p_one, pos_p_two, score_p_one, score_p_two, n_rounds):
        new_score_p_one, new_pos_p_one = self.make_move(added_dice_value, pos_p_one, score_p_one)
        if new_score_p_one >= self.winning_score:
            self.p_one_wins += factor
            return

        new_score_p_two, new_pos_p_two = self.make_move(added_dice_value, pos_p_two, score_p_two)
        if new_score_p_two >= self.winning_score:
            self.p_two_wins += factor
            return

        new_n_rounds = n_rounds + 2
        for score, next_factor in self.possible_scores_counts.items():
            new_factor = factor * next_factor
            self.improve(score, new_factor, new_pos_p_one, new_pos_p_two, new_score_p_one,
                                       new_score_p_two, new_n_rounds)

def process() -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    game = DiracDice(4, 8)
    total = game.play_simple()
    print(f"p one wins: {game.p_one_wins}")
    print(f"p two wins: {game.p_two_wins}")
    return total


if __name__ == '__main__':
    # lines = [i.strip('\n') for i in fileinput.input()]
    # print(lines[0:10])
    output = process()
    print(f'Output: {output}')
