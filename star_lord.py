"""
Aqui se cargan las configuraciones y se incia el servidor como tal.
"""
import socket
import logging
import sys
from servidor_http.servidor import run
from config import HOST
from config import PORT
from config import setup_logging

Log = logging.getLogger('StarLord.run')


if __name__ == '__main__':

    print(chr(27) + "[2J") #limpiamos la terminal

    #configuramos la herramienta de logging
    setup_logging(True);

    try:
        #ejecutamos el servidor con el HOST y el PORT especificados
        #en el archivo config.py. A menos de que se especifique que se quiere que
        #el host sea global (osea 0.0.0.0) acepta conexiones provenientes de cualquier IP
        print "Escuchando en todas las interfaces en el puerto: "+str(PORT)
        run(host='0.0.0.0', port=PORT)

    except KeyboardInterrupt:
        Log.info('terminando StarLord...')
