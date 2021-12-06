import fileinput
from collections import Counter


def single_cycle(current_cycle: dict, reset_cycle_length: int = 6, new_cycle_length: int = 8):
    """
    Each lanternfish creates a new lanternfish once every 7 days.

    A new lanternfish would surely need slightly longer before it's capable of producing more
    lanternfish: two more days for its first cycle.

    Each day, a 0 (n_days_current_cycle) becomes a 6 and adds a new 8 to the end of the list, while each other number
    decreases by 1 if it was present at the start of the day.

    :param current_cycle: Dictionary containing the number of fish per cycle phase (e.g. {1: 12} signifies 12 fish that
        have 1 day left in their cycle)
    :param reset_cycle_length: Number to reset adult fish to when they procreated, default 6 (= 7 day cycle)
    :param new_cycle_length: Number to set new fish to before they create fish themselves the first time, default 8 days
    :return: Dictionary containing the number of fish per cycle phase after a single cycle of current_cycle
    """
    next_cycle = {}
    for n_days_current_cycle, n_fish in current_cycle.items():
        if n_days_current_cycle == 0:
            next_cycle[reset_cycle_length] = n_fish + next_cycle.get(reset_cycle_length, 0)
            next_cycle[new_cycle_length] = n_fish
        elif n_days_current_cycle > 0:
            next_cycle[n_days_current_cycle - 1] = n_fish + next_cycle.get((n_days_current_cycle - 1), 0)
    return next_cycle


def process(fish_dict: dict) -> int:
    """

    :param fish_dict:
    :return:
    """
    for r in range(0, 256):
        fish_dict = single_cycle(current_cycle=fish_dict)
    return sum(fish_dict.values())


if __name__ == '__main__':
    lines = [i.strip('\n') for i in fileinput.input()]
    lines = [int(n) for n in lines[0].split(',')]
    print(lines[0:10])
    lines = Counter(lines)  # maps the counts of unique values into a dict where the unique values are keys
    output = process(lines)
