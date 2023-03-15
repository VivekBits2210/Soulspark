import math

#TODO: Fill Logic for levels and progress to next level calculation
def calculate_level_and_progress(input_chars):
    return 1

def calculate_level(num_chars):
    if num_chars == 0:
        level = 1
    else:
        level = 1 + int(math.log(num_chars, 50) ** 3.5)
    return level
