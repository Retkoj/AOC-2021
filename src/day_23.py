import fileinput
from typing import List
import turtle


class AmphipodGame:
    """
    Rules:
    - Amphipods will never stop on the space immediately outside any room. They can move into that space so long as they
    immediately continue moving. (Specifically, this refers to the four open spaces in the hallway that are directly
    above an amphipod starting position.)
    - Amphipods will never move from the hallway into a room unless that room is their destination room and that room
    contains no amphipods which do not also have that room as their own destination. If an amphipod's starting room is
    not its destination room, it can stay in that room until it leaves the room. (For example, an Amber amphipod will
    not move from the hallway into the right three rooms, and will only move into the leftmost room if that room is
    empty or if it only contains other Amber amphipods.)
    - Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room. (That is,
    once any amphipod starts moving, any other amphipods currently in the hallway are locked in place and will not move
    again until they can move fully into a room.)
    - When moving directly from one room to another: Click the pod, then a place in the hallway, then the room
    to move to
    """
    def __init__(self, field):
        self.field = field
        self.screen = turtle.Screen()
        self.colors = {
            'A': "red",
            'B': "green",
            'C': "blue",
            'D': "yellow"
        }

        self.step_prizes = {
            'A': 1,
            'B': 10,
            'C': 100,
            'D': 1000
        }
        self.cursor_size = 20
        self.reshape_y = -20
        self.reshape_x = 20

        self.amphipods = {}
        self.empty_spaces = {}
        self.total_cost = 0
        self.current_cost_label = None
        self.selected_empty_space = None
        self.selected_amphipod = None
        self.reset_button = None
        self.make_screen()

    def play(self):
        self.screen.onscreenclick(self.select_screen)

    def draw_wall(self, x, y):
        pen = turtle.Turtle()
        pen.hideturtle()
        pen.speed('fastest')
        pen.shape("square")
        pen.penup()
        pen.goto(x, y)
        pen.showturtle()
        pen.color("black")

    def make_amphipod(self, color, x, y):
        amphipod_pen = turtle.Turtle()
        # amphipod_pen.onclick(self.select)
        amphipod_pen.hideturtle()
        amphipod_pen.penup()
        amphipod_pen.goto(x, y)
        amphipod_pen.showturtle()
        amphipod_pen.speed('fastest')
        amphipod_pen.shape("circle")
        amphipod_pen.color(color)
        return amphipod_pen

    def make_empty_space(self, x, y):
        empty_space_pen = turtle.Turtle()
        empty_space_pen.hideturtle()
        empty_space_pen.penup()
        empty_space_pen.goto(x, y)
        empty_space_pen.color("white")
        empty_space_pen.shape("square")
        empty_space_pen.speed('fastest')
        empty_space_pen.showturtle()
        return empty_space_pen

    def make_screen(self):
        self.screen.bgcolor("white")
        self.screen.title("Help the amphipods!")

        for i, line in enumerate(self.field):
            for j, block in enumerate(line):
                x, y = (float(j * self.reshape_x), float(i * self.reshape_y))
                if block == '#':
                    self.draw_wall(x, y)
                if block in ['A', 'B', 'C', 'D']:
                    self.amphipods[(x, y)] = {'type': block,
                                              'pen': self.make_amphipod(self.colors[block], x, y),
                                              'step_prize': self.step_prizes[block]}
                if block == '.':
                    self.empty_spaces[(x, y)] = None
                    self.make_empty_space(x, y)

        self.make_reset_button()

        labels = turtle.Turtle()
        labels.hideturtle()
        labels.penup()
        labels.goto(len(self.field[0]) * -1 * self.reshape_x, 80)
        index_text = ""
        for key, color in self.colors.items():
            index_text += f"{key}: {color} - {self.step_prizes[key]}\n"
        labels.write(index_text, font={"courier new", 28})

        self.current_cost_label = turtle.Turtle()
        self.current_cost_label.hideturtle()
        self.current_cost_label.penup()
        self.current_cost_label.goto(0, 100)
        self.current_cost_label.write(f"current cost: {self.total_cost}", font={"courier new", 32})

    def select_screen(self, x, y):
        turtles = self.screen.turtles()
        for t in turtles:
            if t.distance(x, y) <= self.cursor_size / 2:
                turtle_location = t.pos()
                if turtle_location in self.amphipods.keys():
                    self.selected_amphipod = turtle_location
                elif turtle_location in self.empty_spaces.keys():
                    new_x, new_y = turtle_location
                    if self.selected_amphipod is not None:
                        old_x, old_y = self.selected_amphipod
                        if new_y != (1 * self.reshape_y) and old_y != (1 * self.reshape_y):  # if both not in hallway
                            self.current_cost_label.clear()
                            self.current_cost_label.color("red")
                            self.current_cost_label.write("Move through hallway first",  font={"courier new", 32})
                        else:
                            tmp_amphipod = self.amphipods[self.selected_amphipod]
                            self.amphipods.pop(self.selected_amphipod)
                            tmp_amphipod['pen'].goto(new_x, new_y)
                            self.amphipods[(new_x, new_y)] = tmp_amphipod
                            self.calculate_steps(tmp_amphipod, (old_x, old_y), (new_x, new_y))
                            self.selected_amphipod = None

                            empty_space = t.getturtle()
                            empty_space.goto(old_x, old_y)  # move empty space
                            self.empty_spaces.pop((new_x, new_y))
                            self.empty_spaces[(old_x, old_y)] = None

                            self.current_cost_label.clear()
                            self.current_cost_label.color("black")
                            self.current_cost_label.write(f"current cost: {int(self.total_cost)}",
                                                          font={"courier new", 32})

    def calculate_steps(self, amphipod, start, destination):
        step_prize = amphipod['step_prize']
        x, y = zip(start, destination)
        x_1, x_2 = x
        y_1, y_2 = y
        x_1 = x_1 / self.reshape_x
        x_2 = x_2 / self.reshape_x
        difference_x = abs(x_1 - x_2)

        y_1 = y_1 / self.reshape_y
        y_2 = y_2 / self.reshape_y
        difference_y = abs(y_1 - y_2)
        self.total_cost += step_prize * (difference_x + difference_y)

    def make_reset_button(self):
        button = turtle.Turtle()
        button.hideturtle()
        button.penup()
        button.goto(40, 40)
        button.showturtle()
        button.shape("turtle")
        button.color("red")
        button.write("Click the turtle\n"
                     "to reset the game", font={"courier new", 32})
        button.onclick(self.reset_game)
        self.reset_button = button

    def reset_game(self, x, y):
        self.screen.clear()
        self.amphipods = {}
        self.empty_spaces = {}
        self.total_cost = 0
        self.selected_empty_space = None
        self.selected_amphipod = None
        self.current_cost_label = None
        self.reset_button = None

        self.make_screen()
        self.play()


def process(input_list: List) -> int:
    """

    :param input_list:
    :return:
    """
    total = 0
    field = [list(line) for line in input_list]
    pod_game = AmphipodGame(field)
    pod_game.play()

    turtle.done()
    return total


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    print(lines[0:10])
    output = process(lines)
    print(f'Output: {output}')
