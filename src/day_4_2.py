import fileinput
from typing import List

from src.day_4 import BingoBoard


class BingoSubsystem:
    def __init__(self, called_numbers):
        self.winning_number = None
        self.boards: dict[int: BingoBoard] = {}
        self.n_boards = 0
        self.called_numbers = [int(n) for n in called_numbers]
        self.winning_boards = {}

    def add_board(self, board: BingoBoard):
        self.boards[self.n_boards] = board
        self.n_boards += 1

    def play_game(self):
        """

        Second part challenge: Figure out which board will win last. Once it wins, what would its final score be?
        :return:
        """
        n_winning_boards = 0
        for number in self.called_numbers:
            for i, board in self.boards.items():
                board.cross_off_number(number)
                if board.won and (i not in self.winning_boards.keys()):
                    self.winning_boards[i] = n_winning_boards
                    self.winning_number = number
                    n_winning_boards += 1
                    if n_winning_boards == self.n_boards:
                        print(f"Last winning board is {i}, with number {number}")
                        print(f"sum unmarked: {board.sum_unmarked()}, output: {board.sum_unmarked() * number}")

    def print_boards(self):
        for i, board in self.boards.items():
            print(f"Board {i}:")
            board.print_board()


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    called_numbers = input_list[0].split(',')
    bingo_subsystem = BingoSubsystem(called_numbers)
    input_list.append('')  # Hack-y way to parse the final board
    board = BingoBoard()
    for line in input_list[2:]:
        if line != '':
            board.build_board(line)
        elif line == '':
            bingo_subsystem.add_board(board)
            board = BingoBoard()
    bingo_subsystem.print_boards()
    bingo_subsystem.play_game()
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
