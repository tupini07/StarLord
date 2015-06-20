"""
Este es el modulo del servidor como tal. Aqui se especifican los metodos para handle una coneccion
y el metodo general del 'run' el cual crea un socket, un ThreadPool y empieza a escuchar por conecciones
"""

import logging
import socket
from sistema_archivos.file import get_archivo
from protocolo_http.http_request import parse_http_request
from protocolo_http.http_response import HttpResponse
from thread_pool.pool import ThreadPool
import os
from config import TAM_BUFFER_SOCKET
from config import TAM_THREAD_POOL
from config import MAX_SOCKET_QUEUE_SIZE
from config import STATIC_FILES_DIR

Log = logging.getLogger('StarLord.servidor') #Cramos una instancia global del logger

#metodo ejecutado por los workers para 'handle' un request. Recibe como parametro
#el un objeto socket el cual permite enviar y recibir datos de la conexion (permite
#enviar datos al cliente y recibir datos de este)
def procesar_request(socket_cliente):

    #recibimos los datos del socket. El tamano maximo de datos que el socket puede
    #recibir es de TAM_BUFFER_SOCKET (especificado en config.py). El valor retornado por
    #'Socket.recv' es una representacion String de los datos recibidos.
    request_data = socket_cliente.recv(TAM_BUFFER_SOCKET)

    #creamos un nuevo objeto HttpRequest con los datos del request.
    request = parse_http_request(request_data)

    Log.debug('%s', request_data)

    #obtenemos el archivo se especifico en el 'request.request_uri'. Este metodo
    #devuelve una instancia de file.File [ver file_system.file para una mejor
    #definicion]
    archivo = get_archivo(request.request_uri)

    #si el archivo existe
    if archivo.existe:

        #creamos un nuevo HttpResponse con status code 200 (osea OK)
        #y el protocolo especificado en el reques
        response = HttpResponse(protocolo=request.protocolo, codigo_de_estado=200)

        #le ponemos el archivo al response
        response.file = archivo

    #si el archivo no existe o no fue especificado
    else:
        #creamos un nuevo HttpResponse con status code 404 (osea NOT-FOUND)
        #y el protocolo especificado en el request
        response = HttpResponse(protocolo=request.protocolo, codigo_de_estado=404)

        #el response header 'Content-type' va a ser 'text/plain' ya que no hay archivo
        response.headers['Content-type'] = 'text/html'

        #mostramos un menu con todas las entradas de la carpeta
        response.content = '<h1>StarLord</h1>'+"\n"
        for nombre_archivo in os.listdir(STATIC_FILES_DIR):
            if nombre_archivo != '_': response.content += '<a href="'+nombre_archivo+'">--> '+nombre_archivo+'</h1>'+"\n <br />"
        if len(os.listdir(STATIC_FILES_DIR)) is 0:
            response.content += '<h3> No se encontraron archivos en el directorio de archivos compartidos!! </h3>'


    #logueamos el request que se acaba de procesar y el estado correspondiente a dicho request
    Log.info('GET %s %s %s',
             request.request_uri, request.protocolo, response.codigo_de_estado)
    
    #escribimos el response al socket que nos conecta con el cliente
    response.write_to(socket_cliente)

    #una vez servido el request y mandado el response cerramos el socket
    socket_cliente.close()


def run(host, port):
    address = (host, port)

    #creamos un socket al cual es servidor va a escuchar. Este se va a
    #identificar mediante un Internet PRotocol Address (esto lo especifica socket.AF_INET) y
    #funciona mediante un protocolo basado en coneccion TCP (esto lo especifica
    #socket.SOCK_STREAM)
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #aqui especificamos las opciones del socket. Con 'socket.SOL_SOCKET' decimos que
    #las opciones que vamos a modificar son las que se encuentran al nivel del API
    #del socket. Con socket.SO_REUSEADDR le estamos diciendo al kernel que si el puerto
    #esta ocupado (con estado TIME_WAIT) entonces que igualmente lo use pero si esta
    #ocupado con cualquier otro estado entonces va a dar un error de que el puerto ya esta
    #en uso. Esto es util por si el servidor se apaga y se reinicia inmediatamente,
    #haciendo asi que los sockets aun esten activos en el puerto, pero en estado TIME_WAIT.
    socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #ligamos (bind) el socket al la direccion (address)
    socket_servidor.bind(address)

    #le decimos al socket que empiece la escucha, el parametro 'MAX_SOCKET_QUEUE_SIZE'
    #le especifica al socket la cantidad maxima de conexiones que puede tener en fila
    #(El maximum 'queue' de conexiones)
    socket_servidor.listen(MAX_SOCKET_QUEUE_SIZE)

    #creamos un uevo thread pool y sus trabajadores [ver ThreadPool.__init__]
    pool = ThreadPool(TAM_THREAD_POOL)

    #Esperamos a que alguien se conecte. Activamente esperamos que alguien se conecte y
    #si alguien lo hace entonces procesamos la conexion
    while True:
        
        #aqui es donde el socket intenta aceptar conexiones. El metodo 'socket.accept'
        #devuelve un tuple '(conn, address)' donde 'conn' es un nuevo objeto Socket
        #el cual puede ser usado para enviar y recibir datos a la conexion, y
        #'address' es la direccion conectada al socket del otro lado de la conexion.
        socket_cliente, addr = socket_servidor.accept()

        #si Socket.accept devolvio algo entonces procesamos el request, sino volvemos
        #a aceptar conexiones.
        if socket_cliente:
            Log.debug('-------> Coneccion aceptada de: %s', addr)

            #agregamos un nuevo task al queue de tasks. [ver ThreadPool.add_task para
            #ver como funciona]
            pool.add_task(procesar_request, socket_cliente)
