"""
Esta clase contiene una coleccion de threads los cuales se van a dedicar a cumplir
tasks conforme se estas sean agregadas al task(Queue). Gracias a esta implementacion
el servidor va a poder servir varias conexiones al mismo tiempo.
"""

from Queue import Queue
from trabajador import Trabajador

class ThreadPool:
    def __init__(self, num_hilos):

        #los tasks a realizar son representados por un Queue. En este caso estamos
        #inicializando un FIFO Queue. El parametro que recibe es el maximo de elementos
        #que pueden estar en este Queue.
        self.tasks = Queue(num_hilos)

        #Inicializamos un Trabajador por cada uno de los num_hilos especificados.
        #(un worker por hilo). Y los ponemos a trabajar en los tasks que se encuentran
        #en el queue. Como Queue es un objeto entonces todos los workers van a referenciar
        #a la misma instancia de Queue, osea que todos pueden ver cuando un nuevo task se
        #agrega, pero solo uno puede trabajar en el nuevo task (aqui es donde el objeto Queue
        #implementa el control de acceso por nosotros)
        for i in range(num_hilos):
            Trabajador(self.tasks)


    #este metodo permite agregar un task al queue. Los tasks vienen representados por una funcion
    #(metodo) y sus argumentos ('*args' y '**kwargs') asi los workers lo unico que tienen que hacer
    #es ejecutar la funcion y pasarle los metodos.
    def add_task(self, function, *args, **kwargs):
        self.tasks.put((function, args, kwargs)) #agregamos el task al queue

    def __str__(self):
        return 'Tasks del Thread Pool: %s' % self.tasks
