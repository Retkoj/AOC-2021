import fileinput
from dataclasses import dataclass
from typing import List

import numpy as np

rotations = [
    [1, 1, 1],
    [1, -1, 1],
    [1, -1, -1],
    [1, 1, -1],

    [-1, 1, 1],
    [-1, -1, 1],
    [-1, -1, -1],
    [-1, 1, -1],

    [1, 1, 1],
    [1, -1, 1],
    [1, -1, -1],
    [1, 1, -1],

    [-1, 1, 1],
    [-1, -1, 1],
    [-1, -1, -1],
    [-1, 1, -1],

    [1, 1, 1],
    [1, -1, 1],
    [1, -1, -1],
    [1, 1, -1],

    [-1, 1, 1],
    [-1, -1, 1],
    [-1, -1, -1],
    [-1, 1, -1]
]


@dataclass
class Beacon:
    original_sensor: str
    current_relative_location: tuple
    original_relative_location: tuple
    relative_distance_to_others: dict
    actual_location: tuple = None

    def add_distance_to_other(self, other_relative_location: tuple):
        relative_distance = []
        for c_own, c_other in zip(self.current_relative_location, other_relative_location):
            relative_distance.append(c_own - c_other)
        self.relative_distance_to_others[other_relative_location] = tuple(relative_distance)

    def rotate_beacon(self, rotation_index):
        tmp_relative_location = self.original_relative_location
        if rotation_index >= 8:
            # Rotate next axis to top
            tmp_relative_location = tuple(np.roll(np.array(tmp_relative_location), -1))
        if rotation_index >= 16:
            # Rotate next axis to top
            tmp_relative_location = tuple(np.roll(np.array(tmp_relative_location), -1))
        if rotation_index in list(range(4, 8)) + list(range(12, 16)) + list(range(20, 24)):
            # Switch 2nd and 3rd axis when turning upside down
            tmp = tmp_relative_location
            tmp_relative_location = (tmp[0], tmp[2], tmp[1])

        self.current_relative_location = tuple(np.multiply(tmp_relative_location, rotations[rotation_index]))
        self.relative_distance_to_others = {}

    def reset_beacon(self):
        self.current_relative_location = self.original_relative_location
        self.relative_distance_to_others = {}


@dataclass
class Sensor:
    sensor_name: str
    beacons: list
    actual_location: tuple = None
    rotation_index: int = 0

    def add_beacon(self, relative_location):
        self.beacons.append(Beacon(original_sensor=self.sensor_name, original_relative_location=relative_location,
                                   current_relative_location=relative_location, relative_distance_to_others={}))

    def add_distances_to_others(self):
        for index, beacon in enumerate(self.beacons):
            for index_other, other_beacon in enumerate(self.beacons):
                if index != index_other:
                    beacon.add_distance_to_other(other_beacon.current_relative_location)

    def rotate_beacons(self):
        if self.rotation_index < 24:
            [beacon.rotate_beacon(self.rotation_index) for beacon in self.beacons]
            self.add_distances_to_others()
            self.rotation_index += 1

    def reset_beacons(self):
        self.rotation_index = 0
        [beacon.reset_beacon() for beacon in self.beacons]
        self.add_distances_to_others()

    def update_actual_distance(self):
        pass

    def get_unique_distances(self):
        distances = set()
        for beacon in self.beacons:
            distances.update(set(beacon.relative_distance_to_others.values()))
        return distances

    def get_distances_per_beacon(self):
        distances = {}
        for beacon in self.beacons:
            distances[beacon.current_relative_location] = beacon.relative_distance_to_others.values()
        return distances


class SensorGrid:
    def __init__(self):
        self.sensors = []
        self.min_overlap = 12
        self.pairs = {}

    def add_sensor(self, sensor_name, beacons):
        new_sensor = Sensor(sensor_name=sensor_name, beacons=[])
        for beacon in beacons:
            new_sensor.add_beacon(beacon)
        self.sensors.append(new_sensor)
        self.pairs[sensor_name] = None

    def overlap_sensors(self):
        first_sensor = self.sensors[0]
        while not all(self.pairs.values()):
            for s in range(0, len(self.sensors)):
                sensor = self.sensors[s]
                if self.pairs.get(sensor.sensor_name, None) is None and first_sensor.sensor_name != sensor.sensor_name:
                    sensor.rotate_beacons()  # first 'rotation' is 1,1,1 = no rotation
                    first_distances = first_sensor.get_distances_per_beacon()
                    sensor_distances = sensor.get_distances_per_beacon()
                    overlap = False
                    overlap_count = 0
                    intersecting_coordinates = []
                    for key, distances in first_distances.items():
                        for other_key, other_distances in sensor_distances.items():
                            if len(set(distances).intersection(set(other_distances))) > 0:
                                overlap_count += 1
                                intersecting_coordinates.append(other_key)
                    if overlap_count / 2 == ((self.min_overlap * (self.min_overlap - 1)) / 2):
                        overlap = True
                    # intersecting_distances = first_sensor.get_unique_distances().intersection(sensor.get_unique_distances())
                    # if len(intersecting_distances) >= ((self.min_overlap * (self.min_overlap - 1)) / 2):
                    if overlap:
                        print(sensor.rotation_index)
                        self.pairs[first_sensor.sensor_name] = sensor.sensor_name
                        first_sensor = sensor
                        for reset_sensor in self.sensors:
                            if self.pairs.get(reset_sensor.sensor_name, None) is None and \
                                    reset_sensor.sensor_name != sensor.sensor_name:
                                reset_sensor.reset_beacons()

                        break
            if len([s for s in self.pairs.values() if s is None]) <= 1:
                break
        print(self.sensors[0].get_unique_distances().intersection(self.sensors[1].get_unique_distances()))


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    sensor_grid = SensorGrid()
    sensor_name = ''
    beacons = []
    for line in input_list:
        if 'scanner' in line:
            sensor_name = line
        elif line == '':
            sensor_grid.add_sensor(sensor_name, beacons)
            sensor_name = ''
            beacons = []
        else:
            beacon = tuple([int(n) for n in line.split(',')])
            beacons.append(beacon)
    for sensor in sensor_grid.sensors:
        sensor.add_distances_to_others()
    sensor_grid.overlap_sensors()
    print(sensor_grid)
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    lines.append('')
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
