import sys
import curses
import random
import time
from cookie_move import performMovementLogic

def draw_menu(stdscr, demo):
    position_x = 10
    position_y = 10

    arena_width = 35
    arena_height = 10
    arena_start_x = 10
    arena_start_y = 10

    stdscr.nodelay(1)
    stdscr.leaveok(1)
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    items = {}
    # initialize cookies
    cookies = []
    while len(cookies) < 5:
        cookie_x = int(random.random() * arena_width + arena_start_x)
        cookie_y = int(random.random() * arena_height + arena_start_y)
        cookie = {'x': cookie_x, 'y': cookie_y}
        coordinates = (cookie_x, cookie_y)
        if coordinates not in items:
            items[coordinates] = 'cookie'
            cookies.append(cookie)

    veggies = []
    while len(veggies) < 5:
        veggie_x = int(random.random() * arena_width + arena_start_x)
        veggie_y = int(random.random() * arena_height + arena_start_y)
        veggie = {'x': veggie_x, 'y': veggie_y}
        coordinates = (veggie_x, veggie_y)
        if coordinates not in items:
            items[coordinates] = 'veggie'
            veggies.append(veggie)

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    illegal_move = False
    finished = False
    too_slow = False
    winning_time = None
    time_limit = 10
    cheater_message = u''

    start_time = time.time()

    # Loop where k is the last character pressed
    while True:

        # Check for input
        k = stdscr.getch()
        if k == ord('q'):
            break

        time_passed = time.time() - start_time

        if illegal_move or finished or too_slow:
            if illegal_move:
                message = 'You Cheated! {}'.format(cheater_message)
            elif too_slow:
                message = 'You took too long! Must do it in less than {} seconds'.format(time_limit)
            else:
                message = 'You Won in {} seconds!'.format(winning_time)
            stdscr.addstr(4, 0, '{}'.format(message))
            stdscr.addstr(5, 0, 'Press "q" to exit')
            # Refresh the screen
            stdscr.refresh()
            continue

        # Clear the screen
        stdscr.clear()

        if time_passed > time_limit:
            too_slow = True
            continue

        if not cookies:
            finished = True
            winning_time = time_passed
            continue

        height, width = stdscr.getmaxyx()

        old_x = position_x
        old_y = position_y

        # give a copy of the items so that they can't cheat and change the locations
        items_copy = {}
        for key, value in items.iteritems():
            items_copy[key] = value

        # TODO add debugging hook
        # TODO improve docstring
        if demo:
            position_x, position_y = myPerformMovementLogic(position_x, position_y, items_copy)
        else:
            position_x, position_y = performMovementLogic(position_x, position_y, items_copy)

        # todo check that only 2 ints were returned

        # check that they only tried to move square in x or y, but not both
        if old_x != position_x and old_y != position_y:
            illegal_move = True
            cheater_message = u"You can't move diagonally"
        elif old_x != position_x:
            if abs(old_x - position_x) > 1:
                illegal_move = True
                cheater_message = u"You can't move more than 1 space at a time"
        elif old_y != position_y:
            if abs(old_y - position_y) > 1:
                illegal_move = True
                cheater_message = u"You can't move more than 1 space at a time"

        if illegal_move:
            stdscr.clear()
            continue

        # limit to within the arena
        position_x = max(arena_start_x, position_x)
        position_x = min(arena_start_x + arena_width - 1, position_x)

        position_y = max(arena_start_y, position_y)
        position_y = min(arena_start_y + arena_height - 1, position_y)

        # draw arena border
        stdscr.addstr(arena_start_y - 1, arena_start_x - 1, 'X'*(arena_width+2))
        for i in range(arena_height):
            stdscr.addstr(arena_start_y + i, arena_start_x - 1, 'X')
            stdscr.addstr(arena_start_y + i, arena_start_x + arena_width, 'X')
        stdscr.addstr(arena_start_y + arena_height, arena_start_x - 1, 'X' * (arena_width + 2))

        # draw items
        item_to_remove = None
        for position, item_type in items.iteritems():
            if position_x == position[0] and position_y == position[1]:
                item_to_remove = position
                if item_type == 'cookie':
                    stdscr.addstr(7, 7, 'You Found a Cookie!')
                    cookies.pop()
                else:
                    stdscr.addstr(7, 7, 'You Found a Veggie!')
                    veggies.pop()
            else:
                stdscr.addstr(position[1], position[0], 'C' if item_type == 'cookie' else 'V')
        if item_to_remove:
            del items[item_to_remove]

        # Draw the robot
        stdscr.addstr(position_y, position_x, 'R')

        if not cookies:
            finished = True
            winning_time = time_passed
            stdscr.clear()
            continue

        # Rendering some text
        stdscr.addstr(2, 0, 'Cookies Remaining: {}'.format(len(cookies)))

        # Render status bar
        statusbarstr = "Press 'q' to exit | Time: {} | Pos: {}, {}".format(time_passed, position_x, position_y)
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(0, 0, statusbarstr)
        stdscr.addstr(0, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Refresh the screen
        stdscr.refresh()

        time.sleep(0.2)

my_destination = None
def myPerformMovementLogic(current_x, current_y, items):
    global my_destination

    if my_destination not in items:
        # Greedy find closest cookie
        cookie_x = None
        cookie_y = None
        best_delta_x = 100
        best_delta_y = 100
        for location_tuple, value in items.iteritems():
            if value != u'cookie':
                continue
            delta_x = abs(location_tuple[0] - current_x)
            delta_y = abs(location_tuple[1] - current_y)
            if delta_x + delta_y < best_delta_x + best_delta_y:
                cookie_x = location_tuple[0]
                cookie_y = location_tuple[1]
                best_delta_x = delta_x
                best_delta_y = delta_y
        my_destination = (cookie_x, cookie_y)
    else:
        cookie_x = my_destination[0]
        cookie_y = my_destination[1]

    # head towards it
    if cookie_x > current_x:
        current_x += 1
    elif cookie_x < current_x:
        current_x -= 1
    elif cookie_y > current_y:
        current_y += 1
    elif cookie_y < current_y:
        current_y -= 1

    return current_x, current_y

def main(demo):
    curses.wrapper(draw_menu, demo)

if __name__ == "__main__":
    demo = False
    if len(sys.argv) == 2:
        demo = sys.argv[1] == u'demo'
    main(demo)