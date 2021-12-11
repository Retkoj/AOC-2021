import fileinput
from collections import deque
from itertools import chain

from matplotlib import pyplot as plt


class OctopusGrid:
    def __init__(self, grid, steps: int):
        self.grid = grid
        self.length_max = len(grid)
        self.width_max = len(grid[0])
        self.current_field = (0, 0)
        self.flash_points = deque()
        self.flash_count = 0
        self.steps = steps

    def find_simultanious_point(self):
        all_flashed = False
        steps = 0
        while not all_flashed:
            steps += 1
            self.all_plus_one()
            self.flash()
            all_flashed = all([True if n == 0 else False for n in chain(*self.grid)])
            if all_flashed:
                print(f'Steps: {steps}')
            self.print_flashes(steps)
        return steps

    def run_steps(self):
        for step in range(0, self.steps):
            self.all_plus_one()
            self.flash()
        return self.flash_count

    def print_flashes(self, index):
        print_map = [[20 if n == 0 else n for n in line] for line in self.grid]
        plt.matshow(print_map, cmap='inferno')
        plt.axis('off')
        plt.savefig(f'.\images\octopus_flash\plot_{index}', bbox_inches='tight')
        plt.close()

    def all_plus_one(self):
        for x, line in enumerate(self.grid):
            for y, energy in enumerate(line):
                self.set_new_energy(x, y)

    def flash(self):
        while len(self.flash_points) > 0:
            self.current_field = self.flash_points.popleft()
            adjecent_points = self.fields_in_sight()
            for x, y in adjecent_points:
                if self.grid[x][y] > 0:  # if not already flashed in this step
                    self.set_new_energy(x, y)

    def set_new_energy(self, x, y):
        """
        current energy + 1
        if 9, reset to 0 in self.grid and add coordinates to flash points list
        else, set new energy in self.grid
        :param x:
        :param y:
        :return:
        """
        energy = self.grid[x][y] + 1
        if energy == 10:
            self.flash_count += 1
            self.flash_points.append((x, y))
            self.grid[x][y] = 0
        else:
            self.grid[x][y] = energy

    def fields_in_sight(self):
        """get all 8 seats in line of sight, if any"""
        indices = self.horizontal_fields_in_sigth()
        indices += self.vertical_fields_in_sight()
        indices += self.diagonal_fields_in_sight()
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


def process(input_matrix) -> int:
    """

    :param input_matrix:
    :return:
    """
    octopus_grid = OctopusGrid(input_matrix, steps=100)
    total = octopus_grid.find_simultanious_point()
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    lines = [[int(n) for n in list(line)] for line in lines]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
