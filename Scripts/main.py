import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128

from agents import Cross
    
if __name__ == "__main__":
    # Modificar todo el main (crear un servidor y que cada GET sea un step)
    widht = 24
    height = 24  
    tiempo = 0.5

    cmp = matplotlib.colors.ListedColormap(['white','red', 'yellow', 'green', 'black','blue'])

    tl = [(12,10),(10,11),(11,13),(13,12)]
    model = Cross(widht, height, tl)
    
    contador = 0
    while (contador < 200):
        model.step()
        contador += 1
    
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



