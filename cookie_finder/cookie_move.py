import random

def performMovementLogic(current_x, current_y, items):
    """
    Cookie Monster is working on a cookie-collecting robot.
    He has built the robot and its sensor but he needs you to program the navigation system of his robot.
    It can only move in one direction at a time along the x or the y axis. It cannot go diagonally.
    And Cookie Monster is impatient to get his cookies, so it has to be able to collect them all in under 10 seconds.

    You are given the current position x and y and a dictionary of the items found by the robot sensor.

    The items dictionary looks like {(x,y): item_type} so if there is only a cookie at 5, 7
    it would be {(5,7): 'cookie'}. There are cookies and veggies in the item dictionary. Collecting the
    veggies does not hurt you, but the goal is to collect all the cookies.
    As you collect an item, it will be removed from the item dictionary.
    Note: There are boundaries of the arena (not provided to you) that you cannot move across.

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