import fileinput
import re
from typing import List


class ProbeSender:
    def __init__(self, target_area):
        self.x_range = range(0, 0)
        self.y_range = range(0, 0)
        self.get_range(target_area)
        self.highest_y = 0
        self.highest_points = {}

    def get_relevant_x_range(self):
        def get_steps(x):
            i = 0
            tmp = 0
            while tmp < x:
                i += 1
                tmp += i
            return i
        return range(get_steps(min(self.x_range)) -1 , get_steps(max(self.x_range)) + 2)

    def get_range(self, target_area):
        digits = [int(n) for n in re.findall('-?\d+', target_area)]
        self.x_range = range(digits[0], digits[1] + 1)
        self.y_range = range(digits[2], digits[3] + 1)

    def loop_velocities(self):
        all_cross_points = []
        for x_vel in range(0, 117):
            for y_vel in range(-200, 500):
                highest_point, y_steps, cross_points = self.both_cross(x_vel, y_vel)
                all_cross_points += cross_points
                if highest_point:
                    self.highest_points[(x_vel, y_vel)] = highest_point
                    if highest_point > self.highest_y:
                        self.highest_y = highest_point
        return self.highest_points, self.highest_y, all_cross_points

    def both_cross(self, x_velocity, y_velocity):
        x_steps = self.crossing_x(x_velocity)
        y_steps = self.crossing_y(y_velocity)
        cross_points = []
        highest_point = None
        for step, y_coordinate in y_steps.items():
            x_coordinate = x_steps.get(step, None)
            if x_coordinate is None:
                infinite_coordinate = x_steps.get('inf', None)
                if infinite_coordinate and step >= infinite_coordinate:
                    x_coordinate = x_steps.get(infinite_coordinate, None)
            if x_coordinate:
                cross_points.append((x_velocity, y_velocity))
                highest_point = self.get_highest_y(y_velocity, step)

        return highest_point, y_steps, cross_points

    def crossing_x(self, x_velocity):
        x = 0
        steps_in_range = {}
        step = 0
        while x < max(self.x_range):
            step += 1
            x, x_velocity = self.calculate_x(x, x_velocity)
            if x in self.x_range:
                steps_in_range[step] = x
            if x_velocity == 0:
                if x in self.x_range:
                    steps_in_range['inf'] = step
                break
        return steps_in_range

    def calculate_x(self, x, x_velocity):
        next_x = x + x_velocity
        decrease_velocity = 0
        if next_x < 0:
            decrease_velocity = 1
        elif next_x > 1:
            decrease_velocity = -1
        next_x_velocity = x_velocity + decrease_velocity
        return next_x, next_x_velocity

    def get_highest_y(self, y_velocity, max_step):
        y = 0
        highest = 0
        step = 0
        while y > min(self.y_range):  # since negative target
            step += 1
            y, y_velocity = self.calculate_y(y, y_velocity)
            if y > highest:
                highest = y
            if step >= max_step:
                break
        return highest

    def crossing_y(self, y_velocity):
        y = 0
        steps_in_range = {}
        step = 0
        while y > min(self.y_range):  # since negative target
            step += 1
            y, y_velocity = self.calculate_y(y, y_velocity)
            if y in self.y_range:
                steps_in_range[step] = y
        return steps_in_range

    def calculate_y(self, y, y_velocity):
        next_y = y + y_velocity
        next_y_velocity = y_velocity - 1
        return next_y, next_y_velocity


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    probe_sender = ProbeSender(input_list[0])
    # probe_sender.both_cross(13, -2)
    highest_points, total, cross_points = probe_sender.loop_velocities()
    print(highest_points)
    print(set(cross_points))
    total = len(set(cross_points))
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
