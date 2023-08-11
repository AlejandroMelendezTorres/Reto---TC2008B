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
        if isinstance(obj, Car):
          grid[x][y] = 0.4
        elif isinstance(obj, TrafficLight):
          grid[x][y] = 0.1 + obj.state * .1
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
            
            if (self.next_pos[0] == self.traffic_light.pos[0] or self.next_pos[1] == self.traffic_light.pos[1]):
                self.trigger = True
        else:
            # if we have arrived at the end of the grid remove the agent
            if (self.pos == self.dest):
                #self.model.grid.remove_agent(self)
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
        #self.pos = self.next_pos
        self.model.grid.move_agent(self, self.next_pos)
            

class TrafficLight(Agent):
    def __init__(self, unique_id, model, pos, state):
        # state: 0 = red, 1 = yellow, 2 = green
        super().__init__(unique_id, model)
        self.pos = pos
        self.state = state
        self.next_state = state
        self.type = "TrafficLight"
    
    def step(self):
        if self.state != self.next_state:
            self.state = self.next_state
    
    def advance(self):
        pass

class Cross(Model):
    def __init__(self, width, height, tl):
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.trafic_lights = tl
        self.yoyo = []

        contador = 1

        for test in tl:

            t = TrafficLight(contador, self, test, 2)
            contador += 1
            self.grid.place_agent(t, (test[0], test[1]))
            self.schedule.add(t)
            self.yoyo.append(t)

        car = Car(0, self, (12,0), (12,23), (0,1), self.yoyo[2])
        self.grid.place_agent(car, (12,4))
        self.schedule.add(car)
        
        self.datacollector = DataCollector(
                model_reporters={"Grid": get_grid},  # A function to call
                agent_reporters={"Type": "type"},  # An agent attribute
        )
            
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)


    
if __name__ == "__main__":
    widht =23
    height = 23  
    tiempo = 0.5

    tl = [(10,11),(11,13),(12,10),(13,12)]
    model = Cross(widht, height, tl)
    
    contador = 0
    while (contador < 100):
        model.step()
        contador += 1
    
    all_grid = model.datacollector.get_model_vars_dataframe()

    fig, axs = plt.subplots(figsize=(7,7))
    axs.set_xticks([])
    axs.set_yticks([])
    patch = plt.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)

    def animate(i):
        patch.set_data(all_grid.iloc[i][0])

    anim = animation.FuncAnimation(fig, animate, frames=len(all_grid))

    # save animation using pillow writer

    writergif = animation.PillowWriter(fps=10)
    anim.save('animation.gif', writer=writergif)

