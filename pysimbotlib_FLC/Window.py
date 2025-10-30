#!/usr/bin/python3
import os, sys

from kivy.config import Config
Config.set('graphics', 'resizable', '0') #0 being off 1 being on as in true/false
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.lang import Builder
import platform
from kivy.properties import NumericProperty,\
                            ReferenceListProperty,\
                            ObjectProperty

from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.logger import Logger
from .scaler import Scaler

import random

from . import Obstacle
from . import Objective

DEFAULT_INTERVAL = 1.0/60.0
MAP_DIRECTORY = '/maps'
DEFAULT_MAP_NAME = 'default_map.kv'

class PySimbotMap(Widget):
    playground = ObjectProperty(None)
    obstacles = ObjectProperty(None)
    objectives = ObjectProperty(None)
    iteration = NumericProperty(0)
    max_iter = NumericProperty(0)
    eat_count = NumericProperty(0)
    food_move_count = NumericProperty(0)
    score = NumericProperty(0)

    def __init__(self, mapPath, **kwargs):
        super(PySimbotMap, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.mapPath = mapPath
        self.robots = list()
    
    def before_update(self):
        # Update robots index 0 to UI
        if len(self.robots) > 0:
            distances = self.robots[0].distance()
            smell = self.robots[0].smell()

        Logger.info('Map: Iteration: {}'.format(self.iteration))
    
    def after_update(self):
        Logger.info('Map: End Iteration')

    def update(self, dt):
        if self.max_iter > 0 and self.iteration >= self.max_iter:
            return
        self.iteration += 1
        self.before_update()
        for robot in self.robots:
            robot.update()
        self.after_update()
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            for r in self.robots:
                r.move(5)
        elif keycode[1] == 'a':
            for r in self.robots:
                r.turn(-5)
        elif keycode[1] == 'd':
            for r in self.robots:
                r.turn(5)
        elif keycode[1] == 's':
            for r in self.robots:
                r.move(-5)
        elif keycode[1] == 'n':
            for obj in self.objectives.get_objectives():
                self.change_objective_pos(obj)
                self.food_move_count += 1
                self.score = int(self.eat_count * 100 / self.food_move_count)

    def on_robot_eat(self, robot, obj):
        self.change_objective_pos(obj)
        self.eat_count += 1
        self.food_move_count += 1
        self.score = int(self.eat_count * 100 / self.food_move_count)

    def change_objective_pos(self, obj, pos=None):
        if pos is None:
            new_pos = Vector(random.randrange(self.playground.size[0]), random.randrange(self.playground.size[1]))
            while not self.is_obj_pos_valid(obj, new_pos):
                new_pos = Vector(random.randrange(self.playground.size[0]), random.randrange(self.playground.size[1]))
            obj.pos = new_pos
        else:        
            obj.pos = pos

    def is_obj_pos_valid(self, obj, pos):
        # check wall
        if pos.x < 10 or pos.x > self.size[0] - 210 - obj.size[0]:
            return False
        if pos.y < 10 or pos.y > self.size[1] -  10 - obj.size[1]:
            return False

        # check obstracles
        for obs in self.obstacles.get_obstacles():
            if (obs.pos[0] < pos.x < obs.pos[0] + obs.size[0] or obs.pos[0] < pos.x + obj.size[0] < obs.pos[0] + obs.size[0])\
                and (obs.pos[1] < pos.y < obs.pos[1] + obs.size[1] or obs.pos[1] < pos.y + obj.size[1] < obs.pos[1] + obs.size[1]):
                return False
        return True

class PySimbotApp(App):
    title = 'PySimbot (Created by Saran(Bird) Khotsathian CPE25)'

    def __init__(self, robotCls, numRobot=1, mapPath=os.path.join(MAP_DIRECTORY, DEFAULT_MAP_NAME), interval=DEFAULT_INTERVAL, maxtick=5000, **kwargs):
        super(PySimbotApp, self).__init__(**kwargs)
        Logger.info('Map Path: %s' % mapPath)
        self.numRobot = numRobot
        self.robotCls = robotCls
        self.mapPath = mapPath
        self.interval = interval
        self.maxtick = maxtick
        self.simbotMap = None
    
    def build(self):
        Window.size = (900, 600)
        obmap = Builder.load_file(self.mapPath)
        robot = Builder.load_file('pysimbotlib/widget/robot.kv')
        sbmap = Builder.load_file('pysimbotlib/widget/simbotmap.kv')

        self.simbotMap = PySimbotMap(self.mapPath)
        self.simbotMap.robots = []
        self.simbotMap.max_iter = self.maxtick

        obs = Obstacle.Obstacle()
        self.simbotMap.obstacles = obs
        obj = Objective.Objective()
        self.simbotMap.objectives = obj

        if(self.simbotMap.playground):
            self.simbotMap.playground.add_widget(obs)
            self.simbotMap.playground.add_widget(obj)
        else:
            self.simbotMap.add_widget(obs)
            self.simbotMap.add_widget(obj)

        for i in range(self.numRobot):
            r = self.robotCls()
            r._sm = self.simbotMap
            if(self.simbotMap.playground):
                self.simbotMap.playground.add_widget(r)
            else:
                self.simbotMap.add_widget(r)
            self.simbotMap.robots.append(r)

        Clock.schedule_interval(self.simbotMap.update, self.interval)

        if platform.system() == 'Darwin':
            self._scaler = Scaler(size=Window.size, scale=2)
            Window.add_widget(self._scaler)
            parent = self._scaler or Window
            parent.add_widget(self.simbotMap)
        else:
            return self.simbotMap
