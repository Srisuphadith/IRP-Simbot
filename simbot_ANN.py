#!/usr/bin/python3
import keras
import numpy as np
import os, platform
if platform.system() == "Linux" or platform.system() == "Darwin":
    os.environ["KIVY_VIDEO"] = "ffpyplayer"

from pysimbotlib.core import PySimbotApp, Robot
from kivy.logger import Logger
from kivy.config import Config
load = keras.models.load_model('./model/irp_ANN.keras')

# Force the program to show user's log only for "info" level or more. The info log will be disabled.
Config.set('kivy', 'log_level', 'info')

# update robot every 0.5 seconds (2 frames per sec)
REFRESH_INTERVAL = 1/2

class MyRobot(Robot):
    
    def update(self):
        #create input of model
        x = list(self.distance())
        x.append(self.smell())
        x = np.array([x])

        #predict next move
        next_move = load.predict(x,verbose=0)[0]

        #log next move
        print(f"Turn : {next_move[0]} Move : {next_move[1]}")
        
        #send value to move
        self.turn(float(next_move[0]))
        self.move(float(next_move[1]))

if __name__ == '__main__':
    app = PySimbotApp(robot_cls=MyRobot, num_robots=1, interval=REFRESH_INTERVAL, enable_wasd_control=True)
    app.run()