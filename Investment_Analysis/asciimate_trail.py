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

class DataModel(object):
    current_id = None

    def __init__(self):
        pass

    def get_summary(self):
        return ["a",'b'] , ["a", "b"]

    def delete_contact(self,name):
        pass







class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(
            screen,
            screen.height * 4// 5,
            screen.width * 4 // 5,
            on_load=self._reload_list,
            hover_focus=True,
            can_scroll=False,
            title="Contact List",
        )
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.get_summary(),
            name="trades",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._edit,
        )
        self._edit_button = Button("Edit", self._edit)
        self._delete_button = Button("Delete", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self._add), 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._edit_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Contact")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["trades"]
        raise NextScene("Edit Contact")

    def _delete(self):
        self.save()
        self._model.delete_contact(self.data["trades"])
        self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")






def demo(screen, scene):
    scenes = [
        Scene([ListView(screen,dataModel)], -1, name="Main")
        # Scene([ContactView(screen, contacts)], -1, name="Edit Contact"),
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


dataModel = DataModel()
last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
