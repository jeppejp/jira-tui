from . import Jira
import sys
import curses
import time
import configparser
import os
import subprocess

NOCOL = -1
BLACK = curses.COLOR_BLACK
RED = curses.COLOR_RED
GREEN = curses.COLOR_GREEN
YELLOW = curses.COLOR_YELLOW
BLUE = curses.COLOR_BLUE
MAGENTA = curses.COLOR_MAGENTA
CYAN = curses.COLOR_CYAN
WHITE = curses.COLOR_WHITE


def main_view(stdscr):
    cf = configparser.ConfigParser()
    cf.read(os.path.expanduser('~/.config/jira-cli.conf'))
    url = cf['jira-cli']['url']
    username = cf['jira-cli']['user']
    password = cf['jira-cli']['password']
    myjira = Jira.Jira(url, username, password)
    stdscr.timeout(100)
    curses.start_color()
    curses.use_default_colors()

    query = ''
    last_query = query
    (maxy, maxx) = stdscr.getmaxyx()
    do_search = False
    results = []
    idx = 0
    view_help = False
    only_me = False
    only_open = False

    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    curses.init_pair(4, curses.COLOR_YELLOW, -1)

    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_WHITE)
    s = 0
    force_query = False
    while True:
        query_print = "Query: " + query
        stdscr.addstr(0, 0, "{0:{1}}".format(query_print, maxx))
        control_menu = curses.newwin(3, 17, 3, 3)
        if ((time.time() - do_search) > 1.0 and query != last_query) or force_query:
            force_query = False
            last_query = query
            control_menu.box()
            control_menu.addstr(1, 1, "LOADING RESULTS")
            stdscr.refresh()
            control_menu.refresh()
            results = myjira.search_by_summary(query, only_me, only_open)
            results = results[:maxy - 4]
        else:
            control_menu.clear()

        if not view_help:
            for i in range(0, maxy - 4):

                if i >= len(results):
                    stdscr.addstr(i + 2, 0, " " * (maxx))
                else:
                    issue_print = "[{0}] {1}".format(results[i]['key'], results[i]['summary'])
                    issue_print = issue_print[:maxx]
                    if i == idx:
                        stdscr.addstr(i + 2, 0, "{0:{1}}".format(issue_print, 10), curses.color_pair(1))
                    else:
                        stdscr.addstr(i + 2, 0, "{0:{1}}".format(issue_print, 10), curses.color_pair(2))

        if view_help:
            control_menu = curses.newwin(10, 40, 10, 10)
            control_menu.box()
            control_menu.addstr(1, 1, "HELP:")
            control_menu.addstr(2, 1, "F1 show help")
            control_menu.addstr(3, 1, "F2 only assigned to me")
            control_menu.addstr(4, 1, "F3 only unresolved")
            stdscr.refresh()
            control_menu.refresh()

        options_str = ''
        if only_me:
            options_str += "[only me] "
        if only_open:
            options_str += "[only unres]"
        options_print = "{0:{1}}".format(options_str, maxx - 1)
        stdscr.addstr(maxy - 1, 0, options_print)

        try:
            s = stdscr.getch()
        except KeyboardInterrupt:
            return
        if s == 27:  # ESC
            return
        elif s == curses.KEY_DOWN:
            idx += 1
            idx = min(idx, len(results) - 1)
        elif s == curses.KEY_UP:
            idx -= 1
            idx = max(idx, 0)
        elif s == curses.KEY_BACKSPACE:  # Backspace
            query = query[:-1]
            do_search = time.time()
            idx = 0
        elif s == 265:  # F1
            view_help = not view_help
        elif s == 266:  # F2
            only_me = not only_me
            force_query = True
        elif s == 267:
            only_open = not only_open
            force_query = True
        elif s == 10:  # return
            if idx < len(results):
                return results[idx]['url']
            else:
                return ''
        elif s < 256:  # perhaps a valid char...
            try:
                query += chr(s)
                do_search = time.time()
                idx = 0
            except ValueError:
                pass


def main():
    try:
        url = curses.wrapper(main_view)
    except KeyError as e:
        print("Failed to extract config. Have you filled ~/.config/jira-cli.conf ??")
        print("Exception {}".format(e))
        sys.exit(-1)
    if url:
        try:
            subprocess.Popen(['xdg-open', url])
        except Exception:
            print("Failed xdg-open")
            print(url)


if __name__ == '__main__':
    main()
