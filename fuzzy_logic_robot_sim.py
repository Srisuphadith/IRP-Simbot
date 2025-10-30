#!/usr/bin/python3

import os, sys
import random
import pandas as pd
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
MAX_TICK = 15000

# START POINT
START_POINT = (10, 560)

# Map file
MAP_FILE = 'maps/default_map.kv'

data = []
class FuzzyRobot(Robot):

    def __init__(self):
        super(FuzzyRobot, self).__init__()
        self.pos = START_POINT
        self.turn(90)
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
        rules = []

        # Rule innitial
        rules.append(self.N_target()*(1-self.N_0()))
        rules.append(1-self.N_0())
        rules.append(self.N_7())
        rules.append(self.N_1())
        rules.append(self.N_3())
        rules.append(self.N_6())
        rules.append(self.N_4())
        turns = [0.3,0,45,-45,-45,45,0]
        moves = [0,10,2,2,2,2,20]

        ans_turn = 0.0
        ans_move = 0.0
        # Defuzzy logic
        for r, t, m in zip(rules, turns, moves):
            ans_turn += t * r
            ans_move += m * r
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
        #Action
        x.append(ans_turn)
        x.append(ans_move)
        data.append(x)
        self.turn(ans_turn)
        self.move(ans_move)

    #Membership Function
    def N_target(self):
        return self.target
    def N_0(self):
        return self.de_triangle_fn(self.ir_values[0],10,15)
    def N_1(self):
        return self.de_triangle_fn(self.ir_values[1],10,15)
    def N_2(self):
        return self.de_triangle_fn(self.ir_values[2],10,15)
    def N_3(self):
        return self.de_triangle_fn(self.ir_values[3],10,15)
    def N_4(self):
        return self.de_triangle_fn(self.ir_values[4],10,15)
    def N_5(self):
        return self.de_triangle_fn(self.ir_values[5],10,15)
    def N_6(self):
        return self.de_triangle_fn(self.ir_values[6],10,15)
    def N_7(self):
        return self.de_triangle_fn(self.ir_values[7],10,15)
    def de_triangle_fn(self,dis,lower,upper):
        return 1 if dis <lower else (-(1/(upper-lower))*(dis-upper) if dis < upper else 0)
    def in_triangle_fn(self,dis,lower,upper):
        return 0 if dis <lower else ((1/(upper-lower))*(dis-lower) if dis < upper else 1)
if __name__ == '__main__':
    app = PySimbotApp(FuzzyRobot, ROBOT_NUM, mapPath=MAP_FILE, interval=TIME_INTERVAL, maxtick=MAX_TICK)
    app.run()
    df = pd.DataFrame(data=data,columns=['IR0','IR1','IR2','IR3','IR4','IR5','IR6','IR7','Smell','Turn','Move'])
    df.to_csv('./csv/irp_ann.csv')