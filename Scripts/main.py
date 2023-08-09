from car import Car
from tl import TrafficLight

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid


class Cross(Model):
    def __init__(self, unique_id, model, width, height, tl):
        super().__init__(unique_id, model)
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.trafic_lights = tl
        
        car = Car(1, self, (0,0), (0,0), (0,1))
        self.grid.place_agent(car, (0,0))
        self.schedule.add(car)

        tl = TrafficLight(1, self, (0,1), 0)
        self.grid.place_agent(tl, (0,1))

        car = Car(2, self, (0,0), (0,0), (0,1))
        self.grid.place_agent(car, (0,0))
        self.schedule.add(car)

        self.grid.move_agent(car, (0,1))

        
            
    def step(self):
        self.schedule.step()

    
if __name__ == "__main__":
    widht = 10
    height = 10

    tl = [(0,1), (1,0), (2,1), (1,2)]
    model = Cross(1, None, widht, height, tl)
    model.step()

