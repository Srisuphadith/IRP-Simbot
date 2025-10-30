#!/usr/bin/python3

from pysimbotlib.core import PySimbotApp, Robot
from kivy.logger import Logger
from kivy.config import Config
import random
import keras
import numpy as np
# Force the program to show user's log only for "info" level or more. The info log will be disabled.
Config.set('kivy', 'log_level', 'info')

# update robot every 0.5 seconds (2 frames per sec)
load = keras.models.load_model('./model/irp_ANN.keras')
MAX_TICK = 5000
REFRESH_INTERVAL = 1/120
START_POINT = (10, 560)
class ann(Robot):

    def __init__(self):
        super(ann, self).__init__()
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
        ans_move = float(next_move[1])*100*1.3
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
    app = PySimbotApp(robot_cls=ann, num_robots=1, interval=REFRESH_INTERVAL,max_tick=MAX_TICK, enable_wasd_control=False)
    app.run()