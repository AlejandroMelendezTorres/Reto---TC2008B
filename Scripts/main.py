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

    writergif = animation.PillowWriter(fps=30)
    anim.save('animation.gif', writer=writergif)

    # open and show the animation
    os.system("animation.gif")