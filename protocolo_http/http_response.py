"""
Este modulo contiene todo lo relevante a HttpResponse. El objeto HttpResponse que se usa para simbolizar
y el metodo render_http_response que sirve para transformar un objeto HttpResponse en un string que luego
se puede enviar al socket
"""

import logging
from codigos_de_estado import CODIGOS_ESTADO_HTTP

Log = logging.getLogger('StarLord.response')


class HttpResponse(object):

    def __init__(self, protocolo, codigo_de_estado):
        assert codigo_de_estado in CODIGOS_ESTADO_HTTP, '!!----Status Code Desconocido----!!'

        self.protocolo = protocolo        #la version del protocolo
        self.codigo_de_estado = codigo_de_estado  #el codigo de estado
        self.headers = {}               #los headers
        self.content = ''               #el contenido
        self.file = None                #el archivo

    def __str__(self):
        return 'HttpRequest (protocolo=%s, codigo_de_estado=%s)' % \
               (self.protocolo, self.codigo_de_estado)


    #mandamos el response al socket especificado en output. El response siempre es
    #un file que el cliente esta solicitando.
    def write_to(self, output):
        #si el file en el response ha sido especificado
        if self.file:
            #ponemos el response header 'Content-Type' al mime_type especificado
            self.headers['Content-type'] = self.file.mime_type

            #ponemos el response header 'Content-Length' al tamanno especificado
            self.headers['Content-Length'] = self.file.tamanno

            #ponemos el response header 'Accept-Ranges' a 'bytes'
            self.headers['Accept-Ranges'] = 'bytes'


        #creamos un string que contiene el HttpResponse
        mensaje_response = renderizar_http_response(self)

        #mandamos la respuesta al socket.
        output.sendall(mensaje_response)

        #si se ha especificado un archivo entonces..
        #esto lo hacemos despues de mandar el 'mensaje_response' porque
        #primero tenemos que decirle al cliente que es lo que le vamos a mandar
        #si le vamos a mandar algo, luego se lo mandamos. La parte en que le decimos
        #que le vamos a mandar es cuando le mandamos 'mensaje_response' mediante
        #   output.sendall(mensaje_response)
        if self.file:
            #mandamos el archivo [ver file_system.file.File]
            self.file.stream_to(output)


#metodo que recibe un HttpResponse como parametro y devuelve un String
#con el response
def renderizar_http_response(response):
    ret_val = []

    #seteamos la pimera linea del response, especifivamos los distintos elementos
    #separados por ' ' (version protocolo, codigo de estado y mensaje de estado).
    #el mensaje de estado se encuentra en un mapa en http_protocol.status_codes.HTTP_STATUS_CODES
    response_line = '%s %s %s' % (response.protocolo, response.codigo_de_estado,
                                  CODIGOS_ESTADO_HTTP[response.codigo_de_estado][0])


    #agregamos la primera linea al valor a retornar
    ret_val.append(response_line)

    #por cada pareja key, value, en el diccionario de headers
    #las agregamos al ret_val
    for key, value in response.headers.iteritems():
        header_line = '%s: %s' % (key, value)
        ret_val.append(header_line)

    ret_val.append('')

    if response.content:
        ret_val.append(response.content)
    else:
        ret_val.append('')

    #unimos los elementos del arreglo ret_val con '\n' entre ellos y retornamos
    #ese string
    return '\n'.join(ret_val)
