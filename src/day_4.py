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
        """
        Calculate te sum of all numbers that haven't been crossed off
        :return: int
        """
        summed_unmarked = 0
        for i in range(0, self.board_width):
            for j in range(0, self.board_width):
                if self.crossed_off_board[i][j] == 0:
                    summed_unmarked += self.board[i][j]
        return summed_unmarked

    def check_win(self):
        """
        Check whether there is a horizontal or vertical winning line
        Sets the 'won' parameter to True
        """
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
    """
    The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It
    automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input).
    """
    def __init__(self, called_numbers):
        self.winning_number = None
        self.boards: dict[int: BingoBoard] = {}
        self.n_boards = 0
        self.called_numbers = [int(n) for n in called_numbers]
        self.winning_board = None

    def add_board(self, board: BingoBoard):
        self.boards[self.n_boards] = board
        self.n_boards += 1

    def play_game(self):
        """
        Goes trough all boards, crossing off the called numbers per board. After one board wins, the score of the
        winning board can be calculated. Start by finding the sum of all unmarked numbers on that
        board. Then, multiply that sum by the number that was just called when the board
        won to get the final score.

        The board id number, the winning number (last called), the unmarked sum and the product of the unmarked sum
        and last called number are printed to the commandline.
        :return:
        """
        for number in self.called_numbers:
            for i, board in self.boards.items():
                board.cross_off_number(number)
                if board.won:
                    self.winning_board = i
                    self.winning_number = number
                    print(f"Winning board is {i}, with number {number}")
                    print(f"sum unmarked: {board.sum_unmarked()}, output: {board.sum_unmarked() * number}")
                    break
            if self.winning_board is not None:
                break

    def print_boards(self):
        """
        Print all boards in the system
        """
        for i, board in self.boards.items():
            print(f"Board {i}:")
            board.print_board()


def process(input_list: List) -> int:
    """
    Parses the list of called numbers and the boards into a BingoSubsystem and calls print_boards and play_game
    on the subsystem.
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
