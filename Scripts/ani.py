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

    # Size of the board:
    widht = 24
    height = 24  
    tiempo = 10
    smart = 1
    max_cars = 100

    probabilidad = (10,100) 

    tl = [(12,10),(10,11),(11,13),(13,12)]

    model = Cross(widht, height, probabilidad, smart)

    start_time = time.time()
    maxstep=0
    while (((time.time() - start_time) < tiempo) and model.numTotalCaros < max_cars):
        maxstep+=1
        model.step()


    cmp = matplotlib.colors.ListedColormap(['white','red', 'yellow', 'green', 'black','blue', 'gray'])
    
    execution_time = str(datetime.timedelta(seconds=(time.time() - start_time)))

    all_grid = model.datacollector.get_model_vars_dataframe()

    fig, axs = plt.subplots(figsize=(7,7))
    axs.set_xticks([])
    axs.set_yticks([])
    # show the grid with color
    patch = plt.imshow(all_grid.iloc[0][0], cmap=cmp)

    #patch = plt.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)

    def animate(i):
        patch.set_data(all_grid.iloc[i][0])

    if smart:
        print("Semaforo inteligente")
    else:
        print("Semaforo normal")
    
    print("Maximo de carros: " + str(max_cars))
    print("Numero de carros: " + str(model.numTotalCaros))
    print("Numero de pasos: " + str(len(all_grid)))
    print("Tiempo de ejecución: " + execution_time)

    anim = animation.FuncAnimation(fig, animate, frames=len(all_grid))

    # save animation using pillow writer

    writergif = animation.PillowWriter(fps=8)
    anim.save('Smartanimation.gif', writer=writergif)