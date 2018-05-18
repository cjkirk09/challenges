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
    cursor_x = 10
    cursor_y = 10

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    items = {}
    # todo maybe add obstacles and maybe put the arena boundaries as obstacles
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

    # Loop where k is the last character pressed
    while True:
        if illegal_move or finished:
            # cheater cheater
            # Wait for next input
            k = stdscr.getch()
            if k == ord('q'):
                break
            continue

        if not cookies:
            finished = True
            continue
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        old_x = cursor_x
        old_y = cursor_y

        # give a copy of the items so that they can't cheat and change the locations
        items_copy = {}
        for key, value in items.iteritems():
            items_copy[key] = value

        cursor_x, cursor_y = performMovementLogic(cursor_x, cursor_y, items_copy)

        # check that they only tried to move square in x or y, but not both
        if old_x != cursor_x and old_y != cursor_y:
            illegal_move = True
        elif old_x != cursor_x:
            if abs(old_x - cursor_x) > 1:
                illegal_move = True
        elif old_y != cursor_y:
            if abs(old_y - cursor_y) > 1:
                illegal_move = True

        if illegal_move:
            # show the cheater message and refresh the screen
            continue

        # limit to within the arena
        cursor_x = max(arena_start_x, cursor_x)
        cursor_x = min(arena_start_x + arena_width - 1, cursor_x)

        cursor_y = max(arena_start_y, cursor_y)
        cursor_y = min(arena_start_y + arena_height - 1, cursor_y)

        # draw arena border
        stdscr.addstr(arena_start_y - 1, arena_start_x - 1, 'X'*(arena_width+2))
        for i in range(arena_height):
            stdscr.addstr(arena_start_y + i, arena_start_x - 1, 'X')
            stdscr.addstr(arena_start_y + i, arena_start_x + arena_width, 'X')
        stdscr.addstr(arena_start_y + arena_height, arena_start_x - 1, 'X' * (arena_width + 2))

        # draw cookies
        cookie_to_remove = None
        for cookie in cookies:
            if cursor_x == cookie['x'] and cursor_y == cookie['y']:
                stdscr.addstr(7, 7, 'You Found a Cookie!')
                cookie_to_remove = cookie
            else:
                stdscr.addstr(cookie['y'], cookie['x'], 'C')
        if cookie_to_remove:
            cookies.remove(cookie_to_remove)
            del items[(cookie_to_remove['x'], cookie_to_remove['x'])]

        # Declaration of strings
        title = "Curses example"[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_y = int((height // 2) - 2)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))
        stdscr.addstr(2, 0, 'Cookies Remaining: {}'.format(len(cookies)))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # # Turning on attributes for title
        # stdscr.attron(curses.color_pair(2))
        # stdscr.attron(curses.A_BOLD)
        #
        # # Rendering title
        # stdscr.addstr(start_y, start_x_title, title)
        #
        # # Turning off attributes for title
        # stdscr.attroff(curses.color_pair(2))
        # stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        time.sleep(0.5)

        # # Wait for next input
        # k = stdscr.getch()


def performMovementLogic(current_x, current_y, items):
    print(items)
    # if k == curses.KEY_DOWN:
    #     current_y = current_y + 1
    # elif k == curses.KEY_UP:
    #     current_y = current_y - 1
    # elif k == curses.KEY_RIGHT:
    #     current_x = current_x + 1
    # elif k == curses.KEY_LEFT:
    #     current_x = current_x - 1

    # find closest cookie
    closest_cookie = None
    for location_tuple, value in items.iteritems():
        if value != u'cookie':
            continue
        delta_x = abs(current_x - location_tuple[0])
        delta_y = abs(current_y - location_tuple[1])
    # head towards it, if there is an obstacle go around

    return current_x, current_y

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()