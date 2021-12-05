import fileinput
from typing import List


class BingoBoard:
    def __init__(self):
        self.won = False
        self.board = []
        self.board_width = None
        self.crossed_off_board = []

    def build_board(self, line):
        self.board.append([int(n) for n in line.split()])
        if self.board_width is None:
            self.board_width = len(line.split())
        self.crossed_off_board.append([0] * len(line.split()))

    def print_board(self):
        for line in self.board:
            print(line)

    def print_crossed_off_board(self):
        for line in self.crossed_off_board:
            print(line)

    def cross_off_number(self, number):
        for i, line in enumerate(self.board):
            try:
                index_of_number = line.index(number)
                self.crossed_off_board[i][index_of_number] = 1
                self.check_win()
            except ValueError:
                pass

    def sum_unmarked(self):
        summed_unmarked = 0
        for i in range(0, self.board_width):
            for j in range(0, self.board_width):
                if self.crossed_off_board[i][j] == 0:
                    summed_unmarked += self.board[i][j]
        return summed_unmarked

    def check_win(self):
        self.check_horizontal_win()
        self.check_vertical_win()

    def check_horizontal_win(self):
        win = any([sum(line) == self.board_width for line in self.crossed_off_board])
        if win:
            self.won = True

    def check_vertical_win(self):
        win = False
        for i in range(0, self.board_width):
            if self.board_width == sum([line[i] for line in self.crossed_off_board]):
                win = True
        if win:
            self.won = True


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
    input_list.append('')
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
