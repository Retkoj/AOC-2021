import fileinput
from collections import Counter
from copy import deepcopy
from typing import List


class CaveSystem:
    def __init__(self, connections_list):
        self.big_caves = []
        self.small_caves = []
        self.connections = {}
        self.make_connection_dict(connections_list)
        self.list_small_caves()
        self.all_paths = []

    def make_connection_dict(self, connection_list: List[str]):
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

    def list_small_caves(self):
        """
        Lowercase caves are considered small caves. Current function identifies those and lists them in self.small_caves
        """
        self.small_caves = [cave for cave in self.connections.keys() if cave == cave.lower()]

    def traverse_paths(self) -> int:
        """
        Starting from the 'start', loop through all possible paths and return the number of valid paths
        :return: Number of valid unique paths
        """
        current_cave = 'start'
        road_so_far = [current_cave]
        self.walk_through_caves(current_cave, road_so_far)
        return len(self.all_paths)

    def walk_through_caves(self, current_cave, road_so_far):
        """
        Walks through all caves connected to current_cave, if the cave entered is not 'end' and the path is still valid,
        then proceed to next iteration of caves by calling this function with next_cave.

        road_so_far is deepcopied per loop to collect individual paths.

        When an 'end' cave is reached, the path is saved to self.all_paths

        :param current_cave: Cave you're currently in
        :param road_so_far: Caves you've passed so far
        """
        for next_cave in self.connections[current_cave]:
            current_road = deepcopy(road_so_far)
            if next_cave != 'end':
                if self.is_path_still_valid(current_road, next_cave):
                    current_road.append(next_cave)
                    self.walk_through_caves(next_cave, current_road)

            elif next_cave == 'end':
                current_road.append(next_cave)
                self.all_paths.append(current_road)

    def is_path_still_valid(self, current_road: List[str], current_cave: str) -> bool:
        """
        Valid paths:
            - Large caves can be visited as many times as you want
            - A single small cave can be visited at most twice, the rest of the small caves can only be visited once
            - Start and End can always only be visited once

        :param current_road: Path through caves so far
        :param current_cave: Current cave
        :return: Whether the path is still valid
        """
        valid_path = True

        if current_cave in self.small_caves:
            n_cave_visits = Counter(current_road)
            double_visited_cave = None
            for visited_cave, count in n_cave_visits.items():
                if visited_cave in self.small_caves and count > 1:
                    double_visited_cave = visited_cave
            if (double_visited_cave and current_cave == double_visited_cave) or \
                    (double_visited_cave and (n_cave_visits[current_cave] > 0)):
                valid_path = False

        return valid_path


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
