from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

class Car(Agent):
    def __init__(self, unique_id, model, pos, dest, dir):
        super().__init__(unique_id, model)
        self.pos = pos
        self.next_pos = pos
        self.dest = dest
        self.dir = dir
        self.type = "Car"
    
    def step(self):
        # get agents in front of me
        cells = self.model.grid.get_cell_list_contents([(self.pos[0]+self.dir[0], self.pos[1]+self.dir[1])])
        tl = None
        for obj in cells:
            if isinstance(obj, Car):
                tl = obj
            elif isinstance(obj, TrafficLight):
                tl = obj
                break
        
        if isinstance(tl, TrafficLight):
            if tl.state == 0:
                pass
            elif tl.state == 1:
                pass
            elif tl.state == 2:
                self.next_pos = (self.pos[0]+self.dir[0], self.pos[1]+self.dir[1])
        elif not isinstance(tl, Car):
            self.next_pos = (self.pos[0]+self.dir[0], self.pos[1]+self.dir[1])
    
    def advance(self):
        self.pos = self.next_pos
            

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

    tl = [(4,3), (6,4), (3,5), (5,6)]
    model = Cross(1, None, widht, height, tl)
    model.step()

