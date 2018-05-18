import random

def performMovementLogic(current_x, current_y, items):
    """
    You are given the current position x and y and a dictionary of the items

    The items dictionary looks like {(x,y): item_type} so if there is only a cookie at 5, 7
    it would be {(5,7): 'cookie'}
    You are only allowed to move 1 space in the x or y direction.
    Note: There are boundaries of the arena (not provided to you) that you cannot move across

    :param current_x:
    :param current_y:
    :param items:
    :return: the x and y location that you should move to
    """

    # randomly wander the area
    if random.random() > 0.5:
        if random.random() > 0.5:
            current_x += 1
        else:
            current_x -= 1
    else:
        if random.random() > 0.5:
            current_y += 1
        else:
            current_y -= 1
    return current_x, current_y