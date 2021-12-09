import fileinput
from typing import List

from matplotlib import pyplot as plt


class HeightMap:
    def __init__(self, heightmap):
        self.heightmap = heightmap
        self.length_max = len(heightmap)
        self.current_field = (0, 0)
        self.width_max = len(heightmap[0])
        self.low_points = []
        self.all_low_points = []
        self.all_low_points_in_single_basin = []
        self.basins = []
        self.print_map = [[-1 * ((n + 1) * 10) if n == 9 else 0 for n in line] for line in self.heightmap]

    def find_basins(self):
        for basin_idx, point in enumerate(self.low_points):
            figure_number = str(basin_idx)
            low_points = [point]
            self.all_low_points_in_single_basin = low_points
            self.all_low_points.append(point)
            still_running = True
            counting = 0
            while still_running:
                next_low_points = []
                # self.print_basins(f'{figure_number}_{counting}')
                for low_point in low_points:
                    points = self.loop_through_basin(low_point)
                    next_low_points += points
                if len(next_low_points) == 0:
                    still_running = False
                else:
                    low_points = next_low_points
                counting += 1
            self.basins.append(len(self.all_low_points_in_single_basin))

    def loop_through_basin(self, current_low_point):
        next_low_points = []
        self.current_field = current_low_point
        neighbours = [point for point in self.fields_in_sight()
                      if point not in self.all_low_points_in_single_basin
                      and self.get_value_on_heightmap(point) != 9]
        for neighbour in neighbours:
            self.current_field = neighbour
            current_value = self.get_value_on_heightmap(self.current_field)

            next_neighbours = [point for point in self.fields_in_sight()
                               if point not in self.all_low_points_in_single_basin]
            if all([True if int(self.get_value_on_heightmap(point)) >= int(current_value)
                    else False
                    for point in next_neighbours]):
                next_low_points.append(self.current_field)
                self.all_low_points_in_single_basin.append(self.current_field)
                self.all_low_points.append(self.current_field)
        return next_low_points

    def print_basins(self):
        index = 0
        basin_points = {}
        for idx, basin in enumerate(self.basins):
            # fig_num = f'{idx}'
            basin_points[idx] = self.all_low_points[index:index+basin]
            index += basin

        d = dict(sorted(basin_points.items(), key=lambda item: len(item[1])))
        for idx, items in enumerate(d.items()):
            key, coordinates = items
            for x, y in coordinates:
                self.print_map[x][y] = -10 * (self.heightmap[x][y] + 1)
            plt.matshow(self.print_map, cmap='inferno')
            plt.savefig(f'.\images\plot_{idx}')
            plt.close()
            index += basin

    def find_low_points(self):
        for x in range(0, self.length_max):
            for y in range(0, self.width_max):
                self.current_field = (x, y)
                current_value = self.get_value_on_heightmap(self.current_field)
                neighbours = self.fields_in_sight()
                if all([True if int(self.get_value_on_heightmap(point)) > int(current_value) else False for point in
                        neighbours]):
                    self.low_points.append(self.current_field)

    def get_value_on_heightmap(self, coordinates: tuple):
        return self.heightmap[coordinates[0]][coordinates[1]]

    def fields_in_sight(self):
        """get all 8 seats in line of sight, if any"""
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
                    return (tmp_x, current_y)
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
                    return (current_x, tmp_y)
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
                    return (cur_x, cur_y)
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


def process(input_list: List):
    """

    :param input_list:
    :return:
    """
    heightmap = HeightMap([[int(n) for n in list(line)] for line in input_list])
    heightmap.find_low_points()
    heightmap.find_basins()
    basins = sorted(heightmap.basins)
    basins.reverse()

    heightmap.print_basins()
    prod = 1
    for n in basins[0:3]:
        prod *= n
    return prod


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])

    output = process(lines)
    print(f'Output: {output}')
