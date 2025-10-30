#!/usr/bin/python3

import os, sys
import random
import keras
import numpy as np
from pysimbotlib.Window import PySimbotApp
from pysimbotlib.Robot import Robot
from kivy.core.window import Window
from kivy.logger import Logger
import random
# Number of robot that will be run
ROBOT_NUM = 1

# Delay between update (default: 1/60 (or 60 frame per sec))
TIME_INTERVAL = 1/60 #10frame per second 

# Max tick
MAX_TICK = 5000

# START POINT
START_POINT = (10, 560)

# Map file
MAP_FILE = 'maps/default_map.kv'

load = keras.models.load_model('./model/irp_ANN.keras')
class FuzzyRobot(Robot):

    def __init__(self):
        super(FuzzyRobot, self).__init__()
        self.pos = START_POINT
        self.tg = 0
        self.b_pos = 0
        self.cnt = 0

    def update(self):
        self.ir_values = self.distance()
        #initial IR Sensor buffer
        if self.tg == 0:
             self.b_pos = self.ir_values
             self.tg = 1
        self.target = self.smell()

        x = list(np.array(self.distance())/100)
        x.append(self.smell()/360)
        x = np.array([x])
        next_move = load.predict(x,verbose=0)[0]
        print(f"Turn : {next_move[0]} Move : {next_move[1]}")
        ans_turn = float(next_move[0])*360
        ans_move = float(next_move[1])*100
        #check diff IR
        if sum(self.b_pos) == sum(self.ir_values):
            self.b_pos = self.ir_values
        else:
            self.cnt +=1
        #timer
        if self.cnt > 30:
            self.cnt = 0
            ans_turn = -random.randint(90, 130)
            ans_move = 20
        self.turn(ans_turn)
        self.move(ans_move)

if __name__ == '__main__':
    app = PySimbotApp(FuzzyRobot, ROBOT_NUM, mapPath=MAP_FILE, interval=TIME_INTERVAL, maxtick=MAX_TICK)
    app.run()
    