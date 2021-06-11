from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText

from time import sleep

COLOUR_BLACK = 0
COLOUR_RED = 1
COLOUR_GREEN = 2
COLOUR_YELLOW = 3
COLOUR_BLUE = 4
COLOUR_MAGENTA = 5
COLOUR_CYAN = 6
COLOUR_WHITE = 7

A_BOLD = 1
A_NORMAL = 2
A_REVERSE = 3
A_UNDERLINE = 4


def demo(screen):
    screen.print_at("hello world", 10, 50, COLOUR_GREEN, A_BOLD)
    screen.print_at("hello world", 10, 45, COLOUR_GREEN, A_NORMAL)
    screen.move(0, 0)
    screen.draw(50, 20, thin=True)

    # Draw a large with a smaller rectangle hole in the middle.
    screen.fill_polygon(
        [[(60, 0), (70, 0), (70, 10), (60, 10)], [(63, 2), (67, 2), (67, 8), (63, 8)]]
    )

    # Clear the line
    # screen.move(0, 0)
    # screen.draw(10, 10, char=' ')

    screen.refresh()
    sleep(10)


Screen.wrapper(demo)
