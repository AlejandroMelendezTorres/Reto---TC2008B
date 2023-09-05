import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128

import time
import datetime

from agents import Cross

import os
    
if __name__ == "__main__":
    # Modificar todo el main (crear un servidor y que cada GET sea un step)
    widht = 24
    height = 24  
    tiempo = 10
    smart = True
    max_cars = 500
    # Probabilidad de que un carro aparezca en cada carril
    # 1% - Trafico ligero (1,100)
    # 10% - Trafico mediano (10,100)
    # 20% - Trafico pesado (20,100)
    probabilidad = (10,100) 

    cmp = matplotlib.colors.ListedColormap(['white','red', 'yellow', 'green', 'black','blue', 'gray'])
    
    model = Cross(widht, height, probabilidad, smart)
    
    start_time = time.time()

    while (((time.time() - start_time) < tiempo) and model.numTotalCaros < max_cars):
        model.step()
    
    execution_time = str(datetime.timedelta(seconds=(time.time() - start_time)))

AgentsDF= model.datacollector.get_agent_vars_dataframe()
print(AgentsDF.head())
#acces agents ids separated by step


    #print(positions.loc[1])#get everything from one step
    #print(positions.loc[1]["Position"].tolist())#get a list of all positions in one step

positions=[]

for i in range (1,201):
    tempPos=[] 
    pos=AgentsDF.loc[i]["Position"].tolist()
    type=AgentsDF.loc[i]["Type"].tolist()
    state=AgentsDF.loc[i]["State"].tolist()
    for j in range(len(pos)):
        x,y=pos[j]
        if type[j]=="Car":
            tempPos.append((float(x),float(y),0.0,0,5))
        elif type[j]=="TrafficLight":
            if state[j]==0:
                tempPos.append((float(x),float(y),0.0,1,0))
            elif state[j]==1:
                tempPos.append((float(x),float(y),0.0,1,1))
            elif state[j]==2:
                tempPos.append((float(x),float(y),0.0,1,2))
        #elif type[j]=="lightsController":
            #tempPos.append((float(x),float(y),0.0,2,5))
    positions.append(tempPos)

    if smart:
        print("Semaforo inteligente")
    else:
        print("Semaforo normal")
    
    print("Maximo de carros: " + str(max_cars))
    print("Numero de carros: " + str(model.numTotalCaros))
    print("Numero de pasos: " + str(len(all_grid)))
    print("Tiempo de ejecución: " + execution_time)

    anim = animation.FuncAnimation(fig, animate, frames=len(all_grid))


    writergif = animation.PillowWriter(fps=30)
    anim.save('animation.gif', writer=writergif)