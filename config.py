"""
Configuracion general del proyecto. Aqui se encuentran todas las variables de configuracion
del proyecto.
"""

import os
import logging.config

HOST = 'localhost'    #cual es la direccion del host que va a alojar el servidor. Por default es localhost
PORT = 6262         #cual es el puerto en el que el servidor va a estar escuchando

#la posicion absoluta en la que encuentra este archivo
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

#la posicion absoluta de la carpeta en la que se encuentran los archivos
#que el servidor sirve
STATIC_FILES_DIR = os.path.join(PROJECT_DIR, 'archivos_s')

#El tamano maximo en bytes que se va a leer de un archivo. Esto se usa en file_system.file
BYTES_LECTURA_ARCH = 1024 * 1024

#Tamano maximo de datos que el socket puede recibir (en bytes)
TAM_BUFFER_SOCKET = 4096

#Especifica la cantidad maxima de conexiones en fila que el socket puede
#sostener, este valor debe de ser siempre mayor que 0
MAX_SOCKET_QUEUE_SIZE = 10

#el tamano del thread pool (la cantidad de workers que este va a tener)
TAM_THREAD_POOL = 20

#este es un diccionario con las configuraciones necesarias
#para la herramienta de logging.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(module)s %(process)d %(thread)d %(levelname)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(message)s'
        },
    },
    'handlers': {
        #imprime el log de las cosas en un archivo
        'archivo-log': {
            'level': 'DEBUG',
            #cada dia (a la media noche) se rota el nombre del archivo
            #esto para no hacer una cantidad inecesaria de inputs en el archivo log
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'StarLord.log',
            #especificamos cuando queremos que ocurra la rotacion
            'when': 'midnight',
            },
        #muestra el log de las cosas en la consola
        'consola': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'StarLord': {
            'handlers': ['consola', 'archivo-log'], #especificamos los handlers que queremos usar
            'propagate': False,
            'level': 'DEBUG',
        },
    },
}


#metodo que se encarga de inicializar la herramienta de logging.
def setup_logging(verbose):
    if verbose:
        LOGGING['handlers']['consola']['formatter'] = 'verbose'
    logging.config.dictConfig(LOGGING)
