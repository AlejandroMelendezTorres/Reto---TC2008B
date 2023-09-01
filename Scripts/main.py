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
    tiempo = 0.5

    cmp = matplotlib.colors.ListedColormap(['white','red', 'yellow', 'green', 'black','blue', 'gray'])
    
    model = Cross(widht, height, (1,100))
    
    start_time = time.time()

    while ((time.time() - start_time) < tiempo):
        model.step()
    
    execution_time = str(datetime.timedelta(seconds=(time.time() - start_time)))
    print("Tiempo de ejecución: " + execution_time)

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

    # open and show the animation
    os.system("animation.gif")