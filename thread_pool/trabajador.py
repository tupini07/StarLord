"""
Clase que se encarga de completar tasks. Cada worker corre sobre un thread
diferente y yiene una lista de taska, las cuales completa.
"""

from threading import Thread

class Trabajador(Thread):

    #Thread que ejecuta 'tasks' de una cierta cierta queue de tasks
    def __init__(self, tasks):

        #inicializamos un nuevo Thread el cual va a ser representado por
        #este worker (inicializamos la superclase)
        Thread.__init__(self)

        #declaramos los tasks para el worker (estos son los tasks locales que el worker)
        #posee al ser inicializado
        self.tasks = tasks

        #le decimos que su ejecucion sea NON-BLOCKING
        self.daemon = True

        #Como el Trabajador es una sub-clase de Thread entonces tenemos que inicializarlo
        #para que empieze a ejecutarse (ejecute el metodo 'run')
        self.start()


    #metodo de ejecucion propio del Thread. Este se ejecuta cuando en Thread empieza
    #a ejecutarse
    def run(self):
        while True:

            #Con tasks.get (Queue.get) lo que hacemos es eliminar y retornar un elemento del
            #queue (una especie de 'pop'). Cada elemento del queue (Cada task) es un Tuple
            #el cual contiene 3 elementos (func, *args y **kwargs) [Ver ThreadPool.add_task
            #para una mejor explicacion]
            func, args, kargs = self.tasks.get()

            try:
                #se ejecuta la funcion que estaba especificada en el task
                func(*args, **kargs)

            except Exception, e:
                print e

            #le decimos al queue que el task que acabamos de '.get' ya fue procesado.
            self.tasks.task_done()
