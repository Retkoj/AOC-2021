import fileinput
from typing import List

import numpy as np


class DiracDice:
    def __init__(self, start_position_one, start_position_two):
        self.position_p_one = start_position_one - 1  # get index
        self.score_p_one = 0
        self.position_p_two = start_position_two - 1  # get index
        self.score_p_two = 0
        self.current_dice_value = 1
        self.board_values = np.array(range(1, 11))

    def play(self):
        round = 0
        while self.score_p_one < 1000 and self.score_p_two < 1000:
            round += 1
            move = sum(range(self.current_dice_value, self.current_dice_value + 3))
            if round % 2 == 0:
                score = self.board_values.take(self.position_p_two + move, mode='wrap')
                self.position_p_two = np.where(self.board_values == score)[0][0]  # index of value
                self.score_p_two += score
            else:
                score = self.board_values.take(self.position_p_one + move, mode='wrap')
                self.position_p_one = np.where(self.board_values == score)[0][0]  # index of value
                self.score_p_one += score

            self.current_dice_value += 3
        end_score = self.score_p_two * (round * 3) if self.score_p_two < 1000 else self.score_p_one * (round * 3)
        return end_score


def process() -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    game = DiracDice(4, 2)
    total = game.play()
    return total


if __name__ == '__main__':
    # lines = [i.strip('\n') for i in fileinput.input()]
    # print(lines[0:10])
    output = process()
    print(f'Output: {output}')
