from asciimatics.widgets import (
    Frame,
    ListBox,
    Layout,
    Divider,
    Text,
    Button,
    TextBox,
    Widget,
)
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.renderers import BarChart, StaticRenderer
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.paths import Path
from asciimatics.sprites import Sprite

import sys

from time import sleep
from random import randint
import math

# def fn():
#     return randint(0, 40)
# renderer = BarChart(10, 40, [fn, fn], char='=')


# def demo(screen):
#     screen.print_at('Hello world!', 0, 0)
#     # Draw a large with a smaller rectangle hole in the middle.
#     # screen.fill_polygon([[(60, 0), (70, 0), (70, 10), (60, 10)],
#                     #  [(63, 2), (67, 2), (67, 8), (63, 8)]])

#     screen.print_at(renderer , 10,10)
#     screen.refresh()
#     # sleep(10)

# Screen.wrapper(demo)




# frame = Frame(screen, 80, 20, has_border=False)
# layout = Layout([1, 1, 1, 1])
# frame.add_layout(layout)

# layout.add_widget(Button("OK", self._ok), 0)
# layout.add_widget(Button("Cancel", self._cancel), 3)




# # def demo(screen, scene):
# #     scenes = [
# #         Scene([ListView(screen, contacts)], -1, name="Main"),
# #         Scene([ContactView(screen, contacts)], -1, name="Edit Contact"),
# #     ]

# #     screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

# # last_scene = None
# # while True:
# #     try:
# #         Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
# #         sys.exit(0)
# #     except ResizeScreenError as e:
# #         last_scene = e.scene

# Sample Sprite that plots an "X" for each step along an elliptical path.



def demo(screen):

    centre = (screen.width // 2, screen.height // 2)
    curve_path = []
    for i in range(0, 11):
        curve_path.append(
            (centre[0] + (screen.width / 4 * math.sin(i * math.pi / 5)),
            centre[1] - (screen.height / 4 * math.cos(i * math.pi / 5))))
    path = Path()
    path.jump_to(centre[0], centre[1] - screen.height // 4),
    path.move_round_to(curve_path, 60)
    sprite = Sprite(
        screen,
        renderer_dict={
            "default": StaticRenderer(images=["X"])
        },
        path=path,
        colour=Screen.COLOUR_RED,
        clear=False)


Screen.wrapper(demo)

