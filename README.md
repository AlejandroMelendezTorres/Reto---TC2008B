# Smart Lights
- Alejandro Melendez Torres - A00832494
  
        Durante el transucrso en mi carrera profesional he desarrollado un interes con el
        desarrollo de videojuegos, gracias a esto me siento muy agusto con unity. Por lo
        cual durante esta unidad de formacion me gustaria conocer mas sobre las librerias
        de python. Algunas experiencias que me gustaria desarrollar serian las siguientes:

          - Utilizar Mesa
          - Crear Agentes inteligentes
          - Empezar a conocer las aplicaciones del AI.
  
- Francisco Nicolas Jervis Hidalgo - A00835131
  
        Personalmente mi interes se encuentra en el area de la inteligencia artificial y
        machine learning, por lo que me gustaria aprender en el bloque a utilizar las
        librerias de python como mesa para poder crear agentes y poder aplicarlos en
        el futuro a proyectos. Para lograr esto, me comprometo a dedicarle
        el tiempo necesario a la materia y a las actividades que se nos asignen.

- Jesús Alonso Galaz Reyes - A00832930
        
        Como parte de mis fortalezas, podría mencionar mi habilidad para analizar problemas complejos y
        descomponerlos en pasos más sencillos para su solución. Sin embargo, veo una oportunidad de
        mejorar en la parte de organización y distribución de tareas. En este proyecto espero aprender
        a aplicar mis habilidades de análisis en un proyecto práctico y  colaborar efectivamente con
        mi equipo. Mi objetivo es hacer una solución innovadora para este problema de movilidad urbana,
        utilizando simulaciones gráficas y coordinación de semáforos para reducir la congestión vehicular
        en intersecciones. Además, estoy comprometido a trabajar de manera dedicada, comunicarme
        abiertamente con mi equipo y buscar oportunidades de crecimiento.

- Mariano Barberi Garza - A01571226
  
        Mientras más estudio y me adentro en la programación he seguido buscando quedarme con un área
        de interés, pero no me puedo decidir entre la ciberseguridad o creación de páginas web. Siento
        que soy competente en resolver problemas sobre nuevas tecnologías para mi, ya sea leyendo o
        buscando información, me gustaría adentrarme más en la creación de agentes inteligentes durante
        este semestre. Me comprometo en este proyecto y materia a dedicarle las horas necesarias para
        entender al completo los temas.
 
## Descripcion
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; El proyecto consiste en la simulación de un cruce de calles, en el cual se implementarán agentes que permitan la coordinación de los semáforos. El objetivo de esto es reducir la congestión de los cruces y, así, mejorar la movilidad de los vehículos. Para esto, se utilizará la librería de Mesa para crear los agentes y simular el cruce.

<img alt="Grafica representando la posicion de los agentes" src = "https://i.imgur.com/XyjuOQk.png">

### Librerias
> Mesa\
> Matplotlib

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Se utilizara pip para instalar las librerias  `pip install mesa`

### Agentes
- Car
    
        Este agente representa a los carros que se encuentran en el cruce, estos agentes
        se mueven hacia un destino predeterminado respetando las convenciones de tránsito
        por el cruce y se detienen cuando se encuentran con un semáforo en rojo.

- Traffic Light
  
        Este agente representa a los semaforos que se encuentran en el cruce, estos agentes
        se encuentran en cada esquina del cruce y cambian de color dependiendo de como el
        controlador lo indique. A parte de esto, este agente enviara la información de la
        cantidad de carros que se encuentran en su calle.

- Controller
  
        Este agente representa al controlador del cruce, este agente se encarga de cambiar
        el color de los semáforos de tal manera que se evite la congestión del cruce tomando
        decisiones con base a la información proporcionada por los semáforos.

<img alt="UML de los agentes" src="https://i.imgur.com/FquJCZw.jpg">

### Protocolos de interacción entre los agentes:

- Car -> Traffic Light
   
        El agente de carro le pregunta al semaforo si puede pasar, si el semáforo esta en
        verde el carro puede pasar, si el semáforo está en rojo el carro se detiene.

- Traffic Light -> Car
       
        El agente de semáforo le indica al carro si puede pasar o no, si el semaforo
        esta en verde el carro puede pasar, si el semaforo esta en rojo el carro
        se detiene.

- Controller -> Traffic Light
           
        El agente de controlador le indica al semaforo si debe cambiar de color o no, si el controlador
        le indica que debe cambiar de color el semaforo cambia de color, si el controlador le indica que
        no debe cambiar de color el semaforo no cambia de color.

- Traffic Light -> Controller
               
        El agente de semaforo le indica al controlador la cantidad de carros que estan presentes
        en su calle para en base a esto el controlador decida si debe cambiar de color o no.     

### Plan de Trabajo
- Actividades realizadas:
  - Descripción de cada miembro del equipo
  - Propuesta formal del reto
  - Identificación de los agentes involucrados
  - Diagrama de clase de los agentes involucrados
  - Diagrama de protocolos de interacción


- Actividades pendientes:
  - Programar los autos
  - Programar el controlador de semáforos
  - Crear los agentes
  - Crear conexión entre unity y python
  - Conseguir modelos para el render
  - Ver la posibilidad de añadir peatones
