#!/usr/bin/python3
from kivy.uix.widget import Widget
from kivy.logger import Logger


class ObstacleItem(Widget):
    pass

class Obstacle(Widget):
    def get_obstacles(self):
        obs = []
        for obstacle in self.children:
            if isinstance(obstacle, ObstacleItem):
                obs.append(obstacle)
        return obs