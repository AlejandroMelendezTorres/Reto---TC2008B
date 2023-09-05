from mesa import Model, Agent
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid


from mesa.datacollection import DataCollector


import numpy as np
import pandas as pd

import random

#from agents import Car, TrafficLight, lightsController

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
        
        if len(cell_content) == 0:
            if (x >= 10 and x <= 13) or (y >= 10 and y <= 13):
                grid[x][y] = 6

    return grid

class Cross(Model):
    # Agregar un metodo para que obtenga la informacion de los agentes (solamante de los carros y los semaforos)
    def __init__(self, width, height, prob, smart):
        self.grid = MultiGrid(width, height, False)
        self.width = width
        self.height = height
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.trafic_lights = [(12,10),(10,11),(11,13),(13,12)]
        self.lights = []
        self.contador = 0
        self.origin = [(12,0) ,(13,0) ,(0,10),(0,11) ,(10,23),(11,23),(23,12),(23,13)]
        self.destination = [(12,23),(23,10),(10,0),(23,11),(0,13) ,(11,0) ,(0,12), (13,23)]
        self.middle = [(13, 10), (13, 10), (10, 10), (10, 10), (10, 13), (10, 13), (13, 13), (13,13)]
        self.next_dir = [(1,0), (1,0), (0, -1), (0,-1), (-1, 0), (-1, 0), (0, 1), (0,1)]
        self.directions = [(0,1),(0,1),(1,0),(1,0),(0,-1),(0,-1),(-1,0),(-1,0)]
        self.lightIndex = [0,0,1,1,2,2,3,3]
        self.density = prob
        self.numTotalCaros = 0

        tempx = [(12, 13),(0, 9), (10, 11), (14, 23)]
        tempy = [(0,9), (10, 11), (14, 23), (12, 13)]

        for test in self.trafic_lights:
            lista = []
            for i in range(tempx[self.contador][0], tempx[self.contador][1]+1):
                for j in range(tempy[self.contador][0], tempy[self.contador][1]+1):
                    #print(i,j)
                    lista.append((i,j))
            t = TrafficLight(self.contador, self, test, 0, lista)
            self.contador += 1
            self.grid.place_agent(t, (test[0], test[1]))
            self.schedule.add(t)
            self.lights.append(t)
        
        controller = lightsController(self.contador, self, (23,0), self.lights, smart)
        self.contador += 1
        self.grid.place_agent(controller, (23,0))
        self.schedule.add(controller)

        self.datacollector = DataCollector(
                model_reporters={"Grid": get_grid},
                agent_reporters={"Position": "pos","Type": "type","State": "state"} 
        )
            
    def step(self):
        for i in range(len(self.origin)):
            cell = self.grid.get_cell_list_contents(self.origin[i])
            if len(cell) == 0:
                temp = random.randint(1, self.density[1])
                if temp <= self.density[0] or self.density[0] == self.density[1]:
                    car = Car(self.contador, self, self.origin[i], self.destination[i], self.directions[i], self.lights[self.lightIndex[i]], self.next_dir[i], self.middle[i])
                    self.contador += 1
                    self.grid.place_agent(car, self.origin[i])
                    self.schedule.add(car)

        self.schedule.step()
        self.datacollector.collect(self)

class Car(Agent):
    def __init__(self, unique_id, model, pos, dest, dir, tl, next_dir, middle):
        super().__init__(unique_id, model)
        self.pos = pos
        self.next_pos = pos
        self.dest = dest
        self.dir = dir
        self.type = "Car"
        self.traffic_light = tl
        self.next_dir = next_dir
        self.middle = middle
        self.first = False
        self.state=None
    
    def move(self):
        next = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
        if next[0] >= 0 and next[0] < self.model.width and next[1] >= 0 and next[1] < self.model.height:
            cellmates = self.model.grid.get_cell_list_contents(next)
            trigger = False
            for agent in cellmates:
                if isinstance(agent, Car):
                    trigger = True
            if not trigger:
                if next in self.traffic_light.area:
                    self.next_pos = next
                else:
                    if not self.first:
                        if self.traffic_light.state == 2:
                            self.next_pos = next
                            self.first = True
                    else:
                        self.next_pos = next
                    
    def step(self):
        self.move()

    def advance(self):
        if self.pos == self.dest:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.numTotalCaros += 1
        elif self.pos != self.next_pos:
            if self.next_pos == self.middle:
                self.dir = self.next_dir
            self.model.grid.move_agent(self, self.next_pos)
            self.pos = self.next_pos
        
class TrafficLight(Agent):
    def __init__(self, unique_id, model, pos, state, area):
        # state: 0 = red, 1 = yellow, 2 = green
        super().__init__(unique_id, model)
        self.pos = pos
        self.state = state
        self.next_state = state
        self.type = "TrafficLight"
        self.area = area
        self.num_carros = 0
    
    def step(self):
        self.num_carros = 0
        for cord in self.area:
            cellmates = self.model.grid.get_cell_list_contents(cord)
            for agent in cellmates:
                if isinstance(agent, Car):
                    self.num_carros += 1

    def advance(self):
        if self.state != self.next_state:
            self.state = self.next_state

class lightsController(Agent):
    # NOT SMART CONTROLLER
    def __init__(self, unique_id, model, pos, tl, smart):
        super().__init__(unique_id, model)
        self.pos = pos
        self.traffic_lights = tl
        self.type = "lightsController"
        self.contador = 0
        self.state = None
        self.smart = smart

        if self.smart:
            self.yellows = False
            self.area1 = [] # Para los semaforos 0 y 2
            self.trigger1 = False
            self.area2 = [] # Para los semaforos 1 y 3
            self.trigger2 = False
            num_cariles = 3
            for i in range(10-num_cariles, 10):
                self.area1.append((12, i))
                self.area1.append((13, i))

            for i in range(14, 14+num_cariles):
                self.area1.append((10, i))
                self.area1.append((11, i))

            for i in range(10-num_cariles, 10):
                self.area2.append((i, 10))
                self.area2.append((i, 11))
            
            for i in range(14, 14+num_cariles):
                self.area2.append((i, 12))
                self.area2.append((i, 13))

        for light in self.traffic_lights:
            light.next_state = 0
    
    def step(self):
        if self.smart:
            num_carros12 = 0
            num_carros34 = 0
            for pos in self.area1:
                cellmates = self.model.grid.get_cell_list_contents(pos)
                if len(cellmates) > 0:
                    num_carros12 += 1
            
            for pos in self.area2:
                cellmates = self.model.grid.get_cell_list_contents(pos)
                if len(cellmates) > 0:
                    num_carros34 += 1

            if num_carros12 != 0 and num_carros34 ==0 and not self.trigger2 and not self.yellows:
                self.contador = 0
                self.trigger2 = True
            elif num_carros12 == 0 and num_carros34 != 0 and not self.trigger1 and not self.yellows:
                self.contador == 28
                self.trigger1 = True
            
            if self.trigger1 and self.traffic_lights[1].num_carros + self.traffic_lights[3].num_carros == 0:
                self.contador = 48
                self.trigger1 = False
            elif self.trigger2 and self.traffic_lights[0].num_carros + self.traffic_lights[2].num_carros == 0:
                self.contador = 20
                self.trigger2 = False
        

        if self.contador == 0:
            self.traffic_lights[0].next_state = 2
            self.traffic_lights[1].next_state = 0
            self.traffic_lights[2].next_state = 2
            self.traffic_lights[3].next_state = 0
            self.yellows = False
        if self.contador == 20:
            self.traffic_lights[0].next_state = 1
            self.traffic_lights[1].next_state = 0
            self.traffic_lights[2].next_state = 1
            self.traffic_lights[3].next_state = 0
            self.trigger2 = False
            self.yellows = True
        if self.contador == 28:
            self.traffic_lights[0].next_state = 0
            self.traffic_lights[1].next_state = 2
            self.traffic_lights[2].next_state = 0
            self.traffic_lights[3].next_state = 2
            self.yellows = False
        if self.contador == 48:
            self.traffic_lights[0].next_state = 0
            self.traffic_lights[1].next_state = 1
            self.traffic_lights[2].next_state = 0
            self.traffic_lights[3].next_state = 1
            self.trigger1 = False
            self.yellows = True
        if self.contador == 56:
            self.contador = -1


    def advance(self):
        self.contador += 1