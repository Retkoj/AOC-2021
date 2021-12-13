import fileinput
from typing import List


class Paper:
    def __init__(self, dots, folds):
        self.folds = folds
        self.dots = dots
        self.max_length = max([y for x, y in self.dots]) + 1
        self.max_width = max([x for x, y in self.dots]) + 1
        self.paper_grid = [['.'] * self.max_width for _ in range(0, self.max_length)]
        self.plot_dots_on_paper()

    def plot_dots_on_paper(self):
        for x, y in self.dots:
            print(f'y: {y}, x: {x}')
            self.paper_grid[y][x] = '#'

    def print_grid(self):
        for line in self.dots:
            print(line)

    def make_folds(self):
        for fold in self.folds:
            axis = fold.split('=')[0]
            fold_line = int(fold.split('=')[1])
            if axis == 'x':
                self.fold_paper_x(fold_line)
            else:
                self.fold_paper_y(fold_line)

    def fold_paper_x(self, fold_line: int):
        new_grid = [line[0:fold_line] for line in self.paper_grid]
        for y in range(0, self.max_length):
            for x in range(fold_line, self.max_width):
                if self.paper_grid[y][x] == '#':
                    inverse_x = fold_line - abs(x - fold_line)
                    new_grid[y][inverse_x] = '#'
        self.paper_grid = new_grid
        self.max_width = fold_line

    def fold_paper_y(self, fold_line: int):
        new_grid = self.paper_grid[0:fold_line]
        for y in range(fold_line, self.max_length):
            for x in range(0, self.max_width):
                if self.paper_grid[y][x] == '#':
                    inverse_y = fold_line - abs(y - fold_line)
                    new_grid[inverse_y][x] = '#'
        self.paper_grid = new_grid
        self.max_length = fold_line

    def count_dots(self):
        total = 0
        for line in self.paper_grid:
            total += sum([1 if point == '#' else 0 for point in line])
        return total


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    index = 0
    line = input_list[index]
    dots = []
    while line != '':
        dots.append((int(line.split(',')[0]), int(line.split(',')[1])))
        index += 1
        line = input_list[index]

    index += 1
    folds = []
    while index < len(input_list):
        line = input_list[index]
        line = line.lstrip('fold along ')
        folds.append(line)
        index += 1

    paper = Paper(dots, folds)
    axis = folds[0].split('=')[0]
    fold_line = int(folds[0].split('=')[1])
    if axis == 'x':
        paper.fold_paper_x(fold_line)
    else:
        paper.fold_paper_y(fold_line)
    total = paper.count_dots()

    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
