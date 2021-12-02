from typing import List


class Submarine:
    def __init__(self):
        self.horizontal = 0
        self.depth = 0
        self.aim = 0

    def move(self, direction: str, steps: int) -> None:
        """
        Move the submarine along the aim, horizontal en depth axis.

        - down X increases your aim by X units.
        - up X decreases your aim by X units.
        - forward X does two things:
            - It increases your horizontal position by X units.
            - It increases your depth by your aim multiplied by X.

        :param direction: 'forward', 'down', 'up'
        :param steps: number of steps in the move
        """
        if direction == 'forward':
            self.horizontal += steps
            self.depth += (steps * self.aim)
        elif direction == 'up':
            self.aim -= steps
        elif direction == 'down':
            self.aim += steps

    def multiple_moves(self, moves: List):
        """
        Process multiple moves specified in a list of strings containing the direction and X/steps,
        e.g. 'forward 5', 'down 3'

        :param moves: list of strings
        """
        for move in moves:
            direction, steps = move.split(' ')
            self.move(direction, int(steps))

    def get_position(self):
        """
        Return the current position of the submarine

        :return: horizontal, depth, aim
        """
        return self.horizontal, self.depth, self.aim
