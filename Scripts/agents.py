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
        elif isinstance(obj, lightsController):
            grid[x][y] = 5
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
        
        print("move")

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

class lightsController(Agent):
    # NOT SMART CONTROLLER
    def __init__(self, unique_id, model, pos, tl):
        super().__init__(unique_id, model)
        self.pos = pos
        self.traffic_lights = tl
        self.type = "lightsController"
        self.contador = 0

        self.traffic_lights[0].next_state = 2
        self.traffic_lights[2].next_state = 2
    
    def step(self):
        if self.contador == 15:
            self.traffic_lights[0].next_state = 1
            self.traffic_lights[2].next_state = 1
        if self.contador == 20:
            self.traffic_lights[0].next_state = 0
            self.traffic_lights[2].next_state = 0
            self.traffic_lights[1].next_state = 2
            self.traffic_lights[3].next_state = 2
        if self.contador == 35:
            self.traffic_lights[1].next_state = 1
            self.traffic_lights[3].next_state = 1
        if self.contador == 40:
            self.traffic_lights[1].next_state = 0
            self.traffic_lights[3].next_state = 0
            self.traffic_lights[0].next_state = 2
            self.traffic_lights[2].next_state = 2
            self.contador = 0

    def advance(self):
        self.contador += 1

class Cross(Model):
    def __init__(self, width, height, tl):
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.trafic_lights = tl
        self.lights = []
        self.contador = 0
        self.origin = [(12,0) ,(13,0) ,(0,10),(0,11) ,(10,23),(11,23),(23,12),(23,13)]
        self.destination = [(12,23),(23,10),(10,0),(23,11),(0,13) ,(11,0) ,(0,12), (13,23)]
        self.directions = [(0,1),(0,1),(1,0),(1,0),(0,-1),(0,-1),(-1,0),(-1,0)]
        self.lightIndex = [0,0,1,1,2,2,3,3]

        for test in tl:
            t = TrafficLight(self.contador, self, test, 0)
            self.contador += 1
            self.grid.place_agent(t, (test[0], test[1]))
            self.schedule.add(t)
            self.lights.append(t)
        
        controller = lightsController(self.contador, self, (23,0), self.lights)
        self.contador += 1
        self.grid.place_agent(controller, (23,0))
        self.schedule.add(controller)

        car = Car(self.contador, self, (12,0), (12,23), (0,1), self.lights[0])
        self.contador += 1
        self.grid.place_agent(car, (12,0))
        self.schedule.add(car)

        self.datacollector = DataCollector(
                model_reporters={"Grid": get_grid},  # A function to call
        )
            
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
    
if __name__ == "__main__":
    widht = 24
    height = 24  
    tiempo = 0.5

    cmp = matplotlib.colors.ListedColormap(['white','red', 'yellow', 'green', 'black','blue'])

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
