import fileinput
from copy import deepcopy
from typing import List


class CaveSystem:
    def __init__(self, connections_list):
        self.big_caves = []
        self.small_caves = []
        self.connections = {}
        self.make_connection_dict(connections_list)
        self.make_cave_size_lists()
        self.all_paths = []

    def make_connection_dict(self, connection_list):
        """
        Per cave, list every other cave it connects to.
        The start cave cannot be reached by any other cave,
        The end cave cannot reach other caves

        :param connection_list: list of connections, (two way if not 'end' or 'start'), e.g. ['UM-kb', 'start-kb', ...]
        """
        for connection in connection_list:
            left, right = connection.split('-')
            self.connections[left] = self.connections.get(left, [])
            self.connections[right] = self.connections.get(right, [])

            if 'start' not in [left, right] and 'end' not in [left, right]:
                self.connections[left].append(right)
                self.connections[right].append(left)
            elif left in ['start', 'end']:
                if left == 'end':
                    self.connections[right].append(left)
                else:
                    self.connections[left].append(right)
            elif right in ['start', 'end']:
                if right == 'end':
                    self.connections[left].append(right)
                else:
                    self.connections[right].append(left)

    def make_cave_size_lists(self):
        for cave in self.connections.keys():
            if cave == cave.upper():
                self.big_caves.append(cave)
            elif cave == cave.lower():
                self.small_caves.append(cave)
        self.big_caves = list(set(self.big_caves))
        self.small_caves = list(set(self.small_caves))

    def traverse_paths(self):
        """
        Starting from the 'start', loop through all possible paths and return the number of valid paths
        :return: Number of valid unique paths
        """
        current_cave = 'start'
        road_so_far = [current_cave]
        self.loop_through_caves(current_cave, road_so_far)
        return len(self.all_paths)

    def loop_through_caves(self, current_cave, road_so_far):
        """
        Walks through all caves connected to current_cave, if the cave entered is not 'end' and the path is still valid,
        then proceed to next iteration of caves by calling this function with next_cave.
        valid paths:
            - Small caves can all only be visited once
            - Big caves can be visited multiple times

        road_so_far is deepcopied per loop to collect individual paths.

        When an 'end' cave is reached, the path is saved to self.all_paths

        :param current_cave: Cave you're currently in
        :param road_so_far: Caves you've passed so far
        """
        for cave in self.connections[current_cave]:
            current_road = deepcopy(road_so_far)
            if cave != 'end':
                if cave in self.big_caves or \
                        (cave in self.small_caves and cave not in current_road):  # or (len(current_road) > 1 and current_road[-2] != cave)
                    current_road.append(cave)
                    self.loop_through_caves(cave, current_road)

            elif cave == 'end':
                current_road.append(cave)
                self.all_paths.append(current_road)


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    cave_system = CaveSystem(input_list)
    total = cave_system.traverse_paths()
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
