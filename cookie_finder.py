import sys,os
import curses
import random
import time
arena_width = 20
arena_height = 20
arena_start_x = 10
arena_start_y = 10

def draw_menu(stdscr):
    k = 0
    position_x = 10
    position_y = 10

    stdscr.nodelay(1)
    stdscr.leaveok(1)
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    items = {}
    # TODO maybe add obstacles and maybe put the arena boundaries as obstacles
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

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    illegal_move = False
    finished = False
    stuck = False
    stuck_timeout = 10

    # Loop where k is the last character pressed
    while True:

        # Check for input
        k = stdscr.getch()
        if k == ord('q'):
            break

        if illegal_move or finished:
            # cheater cheater
            stdscr.addstr(4, 0, '{}'.format('You Cheated!' if illegal_move else 'You Won!'))
            stdscr.addstr(5, 0, 'Press "q" to exit')
            # Refresh the screen
            stdscr.refresh()
            continue

        # Clear the screen
        stdscr.clear()

        if not cookies:
            finished = True
            continue

        if stuck and not stuck_timeout:
            break
        elif stuck:
            if stuck_timeout < 6:
                stdscr.addstr(4, 0, 'You seem stuck. {}'.format('closing now' if stuck_timeout == 1 else ''))
            stuck_timeout -= 1
        else:
            stuck_timeout = 10

        height, width = stdscr.getmaxyx()

        old_x = position_x
        old_y = position_y

        # give a copy of the items so that they can't cheat and change the locations
        items_copy = {}
        for key, value in items.iteritems():
            items_copy[key] = value

        position_x, position_y = performMovementLogic(position_x, position_y, items_copy)

        # todo check that only 2 ints were returned

        # check that they only tried to move square in x or y, but not both
        if old_x != position_x and old_y != position_y:
            illegal_move = True
        elif old_x != position_x:
            if abs(old_x - position_x) > 1:
                illegal_move = True
        elif old_y != position_y:
            if abs(old_y - position_y) > 1:
                illegal_move = True

        if illegal_move:
            # show the cheater message and refresh the screen
            stdscr.clear()
            continue

        # limit to within the arena
        position_x = max(arena_start_x, position_x)
        position_x = min(arena_start_x + arena_width - 1, position_x)

        position_y = max(arena_start_y, position_y)
        position_y = min(arena_start_y + arena_height - 1, position_y)

        if old_x == position_x and old_y == position_y:
            stuck = True
        else:
            stuck = False

        # draw arena border
        stdscr.addstr(arena_start_y - 1, arena_start_x - 1, 'X'*(arena_width+2))
        for i in range(arena_height):
            stdscr.addstr(arena_start_y + i, arena_start_x - 1, 'X')
            stdscr.addstr(arena_start_y + i, arena_start_x + arena_width, 'X')
        stdscr.addstr(arena_start_y + arena_height, arena_start_x - 1, 'X' * (arena_width + 2))

        # draw cookies
        cookie_to_remove = None
        for cookie in cookies:
            if position_x == cookie['x'] and position_y == cookie['y']:
                stdscr.addstr(7, 7, 'You Found a Cookie!')
                cookie_to_remove = cookie
            else:
                stdscr.addstr(cookie['y'], cookie['x'], 'C')
        if cookie_to_remove:
            cookies.remove(cookie_to_remove)
            del items[(cookie_to_remove['x'], cookie_to_remove['y'])]

        # Draw you
        stdscr.addstr(position_y, position_x, 'U')

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))
        stdscr.addstr(2, 0, 'Cookies Remaining: {}'.format(len(cookies)))

        # Render status bar
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(position_x, position_y)
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Refresh the screen
        stdscr.refresh()

        time.sleep(0.2)


def performMovementLogic(current_x, current_y, items):

    # TODO find closest cookie
    closest_cookie = None
    for location_tuple, value in items.iteritems():
        if value != u'cookie':
            continue
        delta_x = abs(current_x - location_tuple[0])
        delta_y = abs(current_y - location_tuple[1])

    # TODO head towards it, if there is an obstacle go around

    # randomly wander the area
    if random.random() > 0.5:
        if random.random() > 0.5:
            current_x += 1
        else:
            current_x -= 12
    else:
        if random.random() > 0.5:
            current_y += 1
        else:
            current_y -= 1
    return current_x, current_y

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()