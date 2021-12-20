import fileinput
from copy import deepcopy
from typing import List

import numpy as np
from matplotlib import pyplot as plt


class ImageField:
    def __init__(self, image, enhancement_algorithm):
        self.image_field = np.array([np.array(list(line)) for line in image])
        self.width_max = len(self.image_field[0])
        self.length_max = len(self.image_field)
        self.enhancement_algorithm = enhancement_algorithm
        self.current_field = (0, 0)
        self.expanded_field = []
        self.enhancement_round = 0
        self.expand_field(2)

    def expand_field(self, times):
        self.expanded_field = deepcopy(self.image_field)
        character = self.get_character()

        for _ in range(0, times):
            self.expanded_field = np.insert(self.expanded_field, 0, np.repeat([character], len(self.expanded_field)),
                                            axis=1)
            self.expanded_field = np.insert(self.expanded_field, 0, np.repeat([character], len(self.expanded_field[0])),
                                            axis=0)
            self.expanded_field = np.insert(self.expanded_field,
                                            len(self.expanded_field),
                                            np.repeat([character], len(self.expanded_field[0])),
                                            axis=0)
            self.expanded_field = np.insert(self.expanded_field,
                                            len(self.expanded_field[0]),
                                            np.repeat([character], len(self.expanded_field)),
                                            axis=1)

            self.width_max = len(self.expanded_field[0])
            self.length_max = len(self.expanded_field)

    def enhancements(self, rounds):
        for i in range(0, rounds):
            print(f"Enhancement round: {i}")
            self.enhancement_round += 1
            self.enhance_image()
            self.print_image(i)

    def print_image(self, index):
        binary_field = [[1 if p == '.' else 0 for p in line] for line in self.expanded_field]
        plt.matshow(binary_field, cmap='inferno')
        plt.axis('off')
        plt.savefig(f'.\images\image_enhancer\plot_{index}', bbox_inches='tight')
        plt.close()

    def enhance_image(self):
        self.expand_field(3)
        new_field = deepcopy(self.expanded_field)
        for y in range(0, len(self.expanded_field)):
            for x in range(0, len(self.expanded_field[0])):
                outcome = self.get_field_values((x, y))
                binary = ['0' if p == '.' else '1' for p in outcome]
                number = int(''.join(binary), 2)
                new_pixel = self.enhancement_algorithm[number]
                new_field[y][x] = new_pixel
        self.image_field = new_field
        print(new_field)

    def get_surrounding_fields(self, current_field):
        current_x, current_y = current_field
        return [(current_x - 1, current_y - 1),
                (current_x, current_y - 1),
                (current_x + 1, current_y - 1),

                (current_x - 1, current_y),
                (current_x, current_y),
                (current_x + 1, current_y),

                (current_x - 1, current_y + 1),
                (current_x, current_y + 1),
                (current_x + 1, current_y + 1)]

    def get_character(self):
        character = '.'
        if self.enhancement_round % 2 == 0:
            character = self.enhancement_algorithm[0]
        return character

    def get_field_values(self, current_field):
        surrounding_fields = self.get_surrounding_fields(current_field)

        character = self.get_character()

        characters_lined_up = []
        for x, y in surrounding_fields:
            if (x < 0) or (y < 0) or (x > (len(self.expanded_field[0]) - 1)) or (y > (len(self.expanded_field) - 1)):
                characters_lined_up.append(character)
            else:
                characters_lined_up.append(self.expanded_field[y][x])
        return characters_lined_up

    def count_lit_pixels(self):
        return sum([sum([1 if p == '#' else 0 for p in line]) for line in self.image_field])


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    image_enhancement_algorithm = input_list[0]
    image = input_list[2:]
    image_field = ImageField(image, image_enhancement_algorithm)

    # Change to 2 to get answer to first part
    image_field.enhancements(50)
    total = image_field.count_lit_pixels()

    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
