import datetime
import fileinput
from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from typing import List


class EscapeCavern:
    def __init__(self, cave_grid):
        self.current_field = (0, 0)
        self.cave_grid = cave_grid
        self.length_max = len(cave_grid)
        self.width_max = len(cave_grid[0])

        self.start_point = (0, 0)
        self.end_point = (self.width_max - 1, self.length_max - 1)
        self.distance_to_source = {}
        self.previous_node = {}
        self.queue = []

        self.make_node_graph()

    def make_node_graph(self):
        for y in range(0, self.length_max):
            for x in range(0, self.width_max):
                self.distance_to_source[(x, y)] = float('inf')
                self.previous_node[(x, y)] = None
                self.queue.append((x, y))

        self.distance_to_source[self.start_point] = 0
        self.previous_node[self.start_point] = self.start_point

    def dijkstra_algorithm(self):
        while len(self.queue) > 0:
            distances = [self.distance_to_source[n] for n in self.queue]
            current_node = self.queue.pop(distances.index(min(distances)))
            neighbours = self.fields_in_sight(current_node)

            for node in neighbours:
                if node in self.queue:
                    path_length = self.distance_to_source[current_node] + self.get_weight(node)
                    if path_length < self.distance_to_source[node]:
                        self.distance_to_source[node] = path_length
                        self.previous_node[node] = current_node
        print(self.distance_to_source[self.end_point])
        return self.distance_to_source[self.end_point]

    def get_weight(self, node):
        return self.cave_grid[node[1]][node[0]]

    def fields_in_sight(self, current_field):
        """get all 8 seats in line of sight, if any"""
        self.current_field = current_field
        indices = self.horizontal_fields_in_sigth()
        indices += self.vertical_fields_in_sight()
        # indices += self.diagonal_fields_in_sight()
        return indices

    def check_valid_LOS_coordinate(self, x, y):
        """A valid Line of Sight coordinate is a seat (state.ALIVE or state.EMPTY) and is not the current seat"""
        if (x, y) != self.current_field:
            return True
        return False

    def vertical_fields_in_sight(self):
        """Gets the coordinates of any seats in the vertical line of sight"""
        current_x, current_y = self.current_field

        def get_valid_vertical_coords(x_range) -> tuple or None:
            """Returns the first valid coordinate it comes across"""
            for tmp_x in x_range:
                if self.check_valid_LOS_coordinate(tmp_x, current_y):
                    return tmp_x, current_y
            return None

        # Vertical line:
        x_lower = get_valid_vertical_coords(reversed(range(0, current_x)))
        x_upper = get_valid_vertical_coords(range(current_x + 1, self.length_max))
        return [coords for coords in [x_lower, x_upper] if coords is not None]  # None = no seats in that line of sight

    def horizontal_fields_in_sigth(self):
        """Gets the coordinates of any seats in the horizontal line of sight"""
        current_x, current_y = self.current_field

        def get_valid_horizontal_coords(y_range) -> tuple or None:
            """Returns the first valid coordinate it comes across"""
            for tmp_y in y_range:
                if self.check_valid_LOS_coordinate(current_x, tmp_y):
                    return current_x, tmp_y
            return None

        # Horizontal line:
        y_lower = get_valid_horizontal_coords(reversed(range(0, current_y)))
        y_upper = get_valid_horizontal_coords(range(current_y + 1, self.width_max))
        return [coords for coords in [y_lower, y_upper] if coords is not None]  # None = no seats in that line of sight

    def diagonal_fields_in_sight(self):
        """Gets the coordinates of any seats in the diagonal line of sight"""
        current_x, current_y = self.current_field

        def get_valid_diagonal_coords(x_lst, y_lst) -> tuple or None:
            """Cast to list due to range iterator object by reversed.
            Returns the first valid coordinate it comes across"""
            x_lst, y_lst = list(x_lst), list(y_lst)
            max_index = min(len(x_lst), len(y_lst))
            for i in range(0, max_index):
                cur_x, cur_y = x_lst[i], y_lst[i]
                if self.check_valid_LOS_coordinate(cur_x, cur_y):
                    return cur_x, cur_y
            return None
            # diagonals, go through the range quadrants:

        lower_y = list(reversed(range(0, current_y)))  # cast generator to list to preserve values
        upper_y = range(current_y + 1, self.width_max)
        lower_x = list(reversed(range(0, current_x)))  # cast generator to list to preserve values
        upper_x = range(current_x + 1, self.length_max)
        diags = [get_valid_diagonal_coords(x_l, y_l) for x_l, y_l
                 in [(lower_x, lower_y),  # To upper left corner
                     (upper_x, lower_y),  # To lower left corner
                     (upper_x, upper_y),  # To lower right corner
                     (lower_x, upper_y)]]  # To upper right corner

        return [coords for coords in diags if coords is not None]  # None = no seats in that line of sight


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    cave = EscapeCavern(input_list)
    total = cave.dijkstra_algorithm()
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    lines = [[int(n) for n in list(line)] for line in lines]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
