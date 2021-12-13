import fileinput
from typing import List

from matplotlib import pyplot as plt


class Paper:
    def __init__(self, dots, folds):
        self.folds = [(f.split('=')[0], int(f.split('=')[1])) for f in folds]
        self.dots = dots
        self.max_length = max([y for x, y in self.dots]) + 1
        self.max_width = max([x for x, y in self.dots]) + 1
        self.paper_grid = [['.'] * self.max_width for _ in range(0, self.max_length)]
        self.plot_dots_on_paper()

    def plot_dots_on_paper(self):
        """
        Map the coordinates of the given dots on the paper_grid by putting a '#' sign in those coordinates
        """
        for x, y in self.dots:
            self.paper_grid[y][x] = '#'

    def print_grid(self):
        """
        Print the paper grid both to command line and to file
        :return:
        """
        for line in self.paper_grid:
            print(line)
        plot_paper = [[1 if point == '#' else 0 for point in line] for line in self.paper_grid]
        plt.matshow(plot_paper, cmap='inferno')
        plt.axis('off')
        plt.savefig('.\images\code\code', bbox_inches='tight')
        plt.close()

    def make_folds(self):
        """
        Loops through all fold commands. Determines the axis (x or y) over which the paper folds and calls the correct
        fold function with the index of the fold line
        """
        for axis, fold_index in self.folds:
            if axis == 'x':
                self.fold_paper_x(fold_index)
            else:
                self.fold_paper_y(fold_index)

    def fold_paper_x(self, fold_index: int):
        """
        Create a new grid that represents the folded paper. Map all dots from the right side of the fold line to the
        left:
            fold_index - (old_x_index - fold_index)
        The self.paper_grid is updated with the folded paper
        self.max_width is updated with the fold_index

        :param fold_index: x index on where to fold the paper
        """
        new_grid = [line[0:fold_index] for line in self.paper_grid]
        for y in range(0, self.max_length):
            for x in range(fold_index, self.max_width):
                if self.paper_grid[y][x] == '#':
                    inverse_x = fold_index - abs(x - fold_index)
                    new_grid[y][inverse_x] = '#'
        self.paper_grid = new_grid
        self.max_width = fold_index

    def fold_paper_y(self, fold_index: int):
        """
        Create a new grid that represents the folded paper. Map all dots from the lower side of the fold line to the
        top:
            fold_index - (old_y_index - fold_index)
        The self.paper_grid is updated with the folded paper
        self.max_length is updated with the fold_index

        :param fold_index: y index on where to fold the paper
        :return:
        """
        new_grid = self.paper_grid[0:fold_index]
        for y in range(fold_index, self.max_length):
            for x in range(0, self.max_width):
                if self.paper_grid[y][x] == '#':
                    inverse_y = fold_index - abs(y - fold_index)
                    new_grid[inverse_y][x] = '#'
        self.paper_grid = new_grid
        self.max_length = fold_index

    def count_dots(self):
        """
        Count all dots that are present on the (folded) paper
        :return: total count
        """
        total = 0
        for line in self.paper_grid:
            total += sum([1 if point == '#' else 0 for point in line])
        return total


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
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
    paper.make_folds()
    total = paper.count_dots()
    paper.print_grid()

    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
