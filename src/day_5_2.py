import fileinput
from typing import List


class HydrothermalVentureMap:
    def __init__(self, allow_vertical=False):
        self.allow_vertical = allow_vertical
        self.field_grid = [[0] * 1000 for i in range(0, 1001)]

    def add_vector_to_grid(self, start_point: tuple, end_point: tuple):
        if start_point[0] == end_point[0]:
            low, high = sorted([start_point[1], end_point[1]])
            for y in range(low, high + 1):
                self.field_grid[start_point[0]][y] += 1
        if start_point[1] == end_point[1]:
            low, high = sorted([start_point[0], end_point[0]])
            for x in range(low, high + 1):
                self.field_grid[x][start_point[1]] += 1
        if (start_point[0] != end_point[0]) and (start_point[1] != end_point[1]):
            x_direction_up = start_point[0] < end_point[0]
            y_direction_up = start_point[1] < end_point[1]

            length = abs(start_point[0] - end_point[0])
            steps = 0
            diagonal_x = start_point[0]
            diagonal_y = start_point[1]
            while steps != (length + 1):
                self.field_grid[diagonal_x][diagonal_y] += 1
                diagonal_x = diagonal_x + 1 if x_direction_up else diagonal_x - 1
                diagonal_y = diagonal_y + 1 if y_direction_up else diagonal_y - 1
                steps += 1

    def count_more_than_two(self):
        """
        Count the number of points/coordinates that more than one vector crosses
        """
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
    print(f'Output still correct: {int(output) == 21305}')
