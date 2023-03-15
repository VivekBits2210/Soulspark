import math


def calculate_level(num_chars):
    if num_chars == 0:
        level = 1.0
    else:
        level = 1.0 + math.log(num_chars, 50) ** 3.5
    return level
