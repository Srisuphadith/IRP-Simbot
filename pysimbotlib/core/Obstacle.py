#!/usr/bin/python3
from kivy.uix.widget import Widget
from typing import Generator

class Obstacle(Widget):
    pass

class ObstacleWrapper(Widget):

    def get_obstacles(self) -> Generator[Obstacle, None, None]:
        return (obstacle for obstacle in self.children if isinstance(obstacle, Obstacle))