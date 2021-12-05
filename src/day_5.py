import fileinput
from typing import List


class HydrothermalVentureMap:
    def __init__(self, allow_vertical=False):
        self.allow_vertical = allow_vertical
        self.field_grid = [[0] * 1000 for i in range(0, 1001)]

    def add_vector_to_grid(self, start, end):
        # high - low
        if start[0] == end[0]:
            low, high = (start[1], (end[1] + 1)) if start[1] < end[1] \
                else (end[1], (start[1] + 1))
            for y in range(low, high):
                self.field_grid[start[0]][y] = self.field_grid[start[0]][y] + 1
        if start[1] == end[1]:
            low, high = (start[0], (end[0] + 1)) if start[0] < end[0] \
                else (end[0], (start[0] + 1))
            for x in range(low, high):
                self.field_grid[x][start[1]] = self.field_grid[x][start[1]] + 1

    def count_more_than_two(self):
        total = 0
        for line in self.field_grid:
            for number in line:
                if number >= 2:
                    total += 1
        return total


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    venture_map = HydrothermalVentureMap()
    for vector in input_list:
        start_coordinates, end_coordinates = vector.split(' -> ')
        start_coordinates = int(start_coordinates.split(',')[0]), int(start_coordinates.split(',')[1])
        end_coordinates = int(end_coordinates.split(',')[0]), int(end_coordinates.split(',')[1])
        venture_map.add_vector_to_grid(start_coordinates, end_coordinates)
    total = venture_map.count_more_than_two()
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
