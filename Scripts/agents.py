from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid


from mesa.datacollection import DataCollector
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128

import numpy as np
import pandas as pd

import time
import datetime
import random


def get_grid(model):
    '''
    descripcion...
    '''
    grid = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
      cell_content, (x, y) = cell
      for obj in cell_content:
        if isinstance(obj, RobotLimpieza):
          grid[x][y] = 2
        elif isinstance(obj, Cell):
          grid[x][y] = obj.estado
    return grid

class Car(Agent):
    def __init__(self, unique_id, model, pos, dest, dir, tl):
        super().__init__(unique_id, model)
        self.pos = pos
        self.next_pos = pos
        self.dest = dest
        self.dir = dir
        self.type = "Car"
        self.traffic_light = tl
        self.trigger = False
    
    def step(self):
        if (not self.trigger):
            if (self.traffic_light.state == 2):
                self.next_pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
            
            if (self.next_pos[0] == self.traffic_light[0] or self.next_pos[1] == self.traffic_light[1]):
                self.trigger = True
        else:
            # if we have arrived at the end of the grid remove the agent
            if (self.pos == self.dest):
                self.model.grid.remove_agent(self)
                return
            else:
                if (self.pos[0] == self.dest[0]):
                    if (self.pos[1] < self.dest[1]):
                        self.dir = (0,1)
                    else:
                        self.dir = (0,-1)
                else:
                    if (self.pos[0] < self.dest[0]):
                        self.dir = (1,0)
                    else:
                        self.dir = (-1,0)

                self.next_pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
        
    
    def advance(self):
        self.pos = self.next_pos
        self.model.grid.move_agent(self, self.pos)
            

class TrafficLight(Agent):
    def __init__(self, unique_id, model, pos, state):
        # state: 0 = red, 1 = yellow, 2 = green
        super().__init__(unique_id, model)
        self.pos = pos
        self.state = state
        self.next_state = state
        self.type = "TrafficLight"
    
    def step(self):
        if state != self.next_state:
            state = self.next_state
    
    def advance(self):
        pass

class Cross(Model):
    def __init__(self, width, height, tl):
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.trafic_lights = tl
        self.trafic_lights_list = []

        contador = 1


        for test in tl:

            t = TrafficLight(contador, self, test, 0)
            contador += 1
            self.grid.place_agent(t, (test[0], test[1]))
            self.schedule.add(t)
            self.trafic_lights_list.append(t)
            
    def step(self):
        self.schedule.step()


    
if __name__ == "__main__":
    widht =23
    height = 23

    tl = [(11,10),(13,11),(10,12),(12,13)]
    model = Cross(widht, height, tl)
    #model.step()

