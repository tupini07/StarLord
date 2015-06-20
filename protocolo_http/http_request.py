"""
En este modulo se encuentran todas las cosas relevantes al HTTP Request. El objeto HttpRequest que
lo simboliza y el metodo que se encarga de parse_http_request.
"""

import re   #expreciones regulares
import logging
from exceptions import HttpParseException

Log = logging.getLogger('StarLord.servidor')

#objeto que simboliza el HttpRequest
class HttpRequest(object):

    def __init__(self, metodo, request_uri, protocolo, headers):
        self.metodo = metodo    #el metodo mediante el cual se realizo el request (GET,POST,etc)
        self.request_uri = request_uri #el URI que se solicito en el request
        self.protocolo = protocolo #la version de HTTP con la que se solicito el request
        self.headers = headers #diccionario con los distintos headers que se pasaron en el request


    def __str__(self):
        return 'HttpRequest (metodo=%s, request_uri=%s, protocolo=%s)' % \
               (self.metodo, self.request_uri, self.protocolo)


#el parametro que recibe es una representacion string de un HttpRequest, este metodo
#se encarga de 'parsearlo' y convertirlo en una instancia de HttpRequest
def parse_http_request(data_request):

    #Se fija si el request (data_request) esta vacio
    if not data_request:
        error = 'Debe proveerse algun dato para que este pueda ser procesado en data_request'
        Log.error(error)
        raise HttpParseException(error)

    #separamos los datos en lineas. Lo que hace el metodo '.splitlines' es separar
    #el string en un arreglo y separa el string donde halla '\n' (newline), el parametro
    #que le estamos pasando es para que no meta el '\n' en el arreglo. Por ejemplo
    # "hola \n\n pop".splitlines(False) va a devolver ['hola ', '', ' pop']
    data_lines = data_request.splitlines(False)

    #esta es la linea que suponemos que especifica el request (esta es el initial request linea).
    request_line = data_lines[0]

    #Un request_line tiene 3 partes separadas por espacios. El nombre del metodo, el path del
    #recurso solicitado y la version del protocolo HTTP que se esta utilizando
    #   por ejemplo:
    #       GET /path/al/archivo/index.html HTTP/1.0
    componentes_request = request_line.split(' ')

    #Si la cantidad de elementos en componentes_request es diferente de 3 entonces sabemos que
    #no es un HTTP request valido
    if len(componentes_request) != 3:
        error = 'No se pudo procesar la linea de request: %s' % request_line
        Log.error(error)
        raise HttpParseException(error)

    #Separamos los elementos de componentes_request en el metodo, el URI del request y la
    #version del protocolo
    metodo, request_uri, protocolo = componentes_request[0], componentes_request[1], componentes_request[2]

    #diccionario de headers. Aqui se contiene los componentes de las lineas del header
    #del HTTP request. Por ejemplo uno de sus elementos puede ser:
    #                   {'From':'usuario@blabla.com'}
    headers = {}

    #ahora procesamos el resto de los data_lines que recibimos en el request..
    for linea in data_lines[1:]:

        if not linea:
            break

        #separamos los componentes de una linea. Las lineas que le siguen a la primera linea
        #siempre tienen sus componentes separados por ': ' y siempre son 2, por ejemplo
        #               From: usuario@blabla.com
        componentes_linea = linea.split(': ')

        #si los componentes de la linea no son 2 entonces no es una linea valida
        if len(componentes_linea) != 2:
            raise HttpParseException('No se puede procesar la linea del HTTP header: %s' % linea)

        #separamos los elementos de componentes_linea en key y value
        key, value = componentes_linea[0], componentes_linea[1]
        headers[key] = value    #guardamos el key y el value en el diccionario

    #retornamos un nuevo objeto HttpRequest el cual contiene el metodo de request (GET,POST,etc),
    #el URI solicitado, la version de HTTP y los headers
    return HttpRequest(metodo, request_uri, protocolo, headers)
