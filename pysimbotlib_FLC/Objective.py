#!/usr/bin/python3
from kivy.uix.widget import Widget
from kivy.logger import Logger

class ObjectiveItem(Widget):
    pass

class Objective(Widget):
    def get_objectives(self):
        obj = []
        for objective in self.children:
            if isinstance(objective, ObjectiveItem):
                obj.append(objective)
        return obj