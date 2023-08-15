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
    grid = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
      cell_content, (x, y) = cell
      for obj in cell_content:
        if isinstance(obj, Car):
          grid[x][y] = 4
        elif isinstance(obj, TrafficLight):
          grid[x][y] = obj.state + 1
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
    
    def move(self):
        cellmates = self.model.grid.get_cell_list_contents((self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]))
        if len(cellmates) == 0:
            self.next_pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])

    def step(self):
        if   ((self.pos[0] == self.traffic_light.pos[0] or self.pos[0] == self.traffic_light.pos[0]+1)and(self.pos[1] < self.traffic_light.pos[1]-1) and self.traffic_light.unique_id == 1+50):
            if self.traffic_light.state == 2:
                pass
            else:
                self.move()
        elif ((self.pos[0] < self.traffic_light.pos[0]-1)and(self.pos[1] == self.traffic_light.pos[1] or self.pos[1] == self.traffic_light.pos[1]-1) and self.traffic_light.unique_id == 2+50):
            if self.traffic_light.state == 2:
                pass
            else:
                self.move()
        elif ((self.pos[0] == self.traffic_light.pos[0] or self.pos[0] == self.traffic_light.pos[0]-1)and(self.pos[1] > self.traffic_light.pos[1]+1) and self.traffic_light.unique_id == 3+50):
            if self.traffic_light.state == 2:
                pass
            else:
                self.move()
        elif ((self.pos[0] > self.traffic_light.pos[0]+1)and(self.pos[1] == self.traffic_light.pos[1] or self.pos[1] == self.traffic_light.pos[1]+1) and self.traffic_light.unique_id == 4+50):
            if self.traffic_light.state == 2:
                pass
            else:
                self.move()
        
        
    
    def advance(self):
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
        self.lights = []
        self.contador = 0

        contador = 1

        for test in tl:
            t = TrafficLight(contador+50, self, test, 0)
            contador += 1
            self.grid.place_agent(t, (test[0], test[1]))
            self.schedule.add(t)
            self.lights.append(t)

        u = [(12,0) ,(13,0) ,(0,10),(0,11) ,(10,23),(11,23),(23,12),(23,13)]
        d = [(12,23),(23,10),(10,0),(23,11),(0,13) ,(11,0) ,(0,12), (13,23)]
        m = [(0,1),(0,1),(1,0),(1,0),(0,-1),(0,-1),(-1,0),(-1,0)]
        o = [0,0,1,1,2,2,3,3]

        for k in range(len(u)):
            car = Car(k, self, u[k], d[k], m[k], self.lights[o[k]])
            self.grid.place_agent(car, u[k])
            self.schedule.add(car)
        
        self.datacollector = DataCollector(
                model_reporters={"Grid": get_grid},  # A function to call
                agent_reporters={"Type": "type"},  # An agent attribute
        )
            
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.contador += 1
        if contador % 10 == 0:
            u = [(12,0) ,(13,0) ,(0,10),(0,11) ,(10,23),(11,23),(23,12),(23,13)]
            d = [(12,23),(23,10),(10,0),(23,11),(0,13) ,(11,0) ,(0,12), (13,23)]
            m = [(0,1),(0,1),(1,0),(1,0),(0,-1),(0,-1),(-1,0),(-1,0)]
            o = [0,0,1,1,2,2,3,3]

            for k in range(len(u)):
                car = Car(100+k+self.contador, self, u[k], d[k], m[k], self.lights[o[k]])
                self.grid.place_agent(car, u[k])
                self.schedule.add(car)
    
if __name__ == "__main__":
    widht = 24
    height = 24  
    tiempo = 0.5

    cmp = matplotlib.colors.ListedColormap(['white','red', 'yellow', 'green', 'black',])

    tl = [(12,10),(10,11),(11,13),(13,12)]
    model = Cross(widht, height, tl)
    
    contador = 0
    while (contador < 100):
        model.step()
        contador += 1
    
    all_grid = model.datacollector.get_model_vars_dataframe()

    fig, axs = plt.subplots(figsize=(7,7))
    axs.set_xticks([])
    axs.set_yticks([])
    # show the grid with color
    patch = plt.imshow(all_grid.iloc[0][0], cmap=cmp)

    #patch = plt.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)

    def animate(i):
        patch.set_data(all_grid.iloc[i][0])

    anim = animation.FuncAnimation(fig, animate, frames=len(all_grid))

    # save animation using pillow writer

    writergif = animation.PillowWriter(fps=10)
    anim.save('animation.gif', writer=writergif)
