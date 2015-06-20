"""
'File' es una representacion de un archivo y contiene varios metodos importantes. Incluyendo el
stream_to que manda el archivo al socket especificado. El metodo get_file permite crear una
instancia de 'File' que represente al archivo que se encuentra en la carpeta de archivos
estaticos.
"""
import os
import logging
import mimetypes
import socket
from config import STATIC_FILES_DIR
from config import BYTES_LECTURA_ARCH

Log = logging.getLogger('StarLord.file')


class File(object):
    def __init__(self, request_uri=None, file_name=None, tamanno=None, existe=False, mime_type=None):
        self.request_uri = request_uri  #el URI con el que busco el archivo
        self.file_name = file_name      #el path absoluto al archivo
        self.tamanno = tamanno      #el tamano del archivo
        self.existe = existe            #si el archivo existe o no
        self.mime_type = mime_type      #el mime_type del archivo

    def __str__(self):
        return 'File (request_uri=%s, file_name=%s, existe=%s, mime_type=%s)' % \
               (self.request_uri, self.file_name, self.existe, self.mime_type)


    #abrimos el archivo (devuelve un nuevo objeto de tipo file[ Este es el tipo definido por Python
    #y no el que definimos nosotros])
    def open(self):
        #abrimos el archivo en modo de luctura y binario('r' para read y 'b' para binary). Devuelve
        #un nuevo archivo de tipo file.
        return open(self.file_name, 'rb')


    def stream_to(self, output, file_chunk_size=None):
        #si no se especifica el parametro file_chunk_size entonces usamos el valor definido
        #en config.py
        if not file_chunk_size:
            file_chunk_size = BYTES_LECTURA_ARCH

        range_start, range_end = 0, self.tamanno - 1

        #abrimos el archivo y lo denominamos 'archivo'
        with self.open() as archivo:

            #seteamos la posicion del archivo (en este caso desde el inicio)
            archivo.seek(range_start)

            #la cantiadad de bytes que hay entre range_start y range_end
            bytes_faltantes = range_end - range_start + 1

            # mientras ya no halla bytes_faltantes que mandar
            while bytes_faltantes > 0:

                #lee un bloque de bytes de archivo. El numero de bytes que le es igual al
                #especificado como parametro o menos si se encuentra EOF.
                #Los bytes son retornados como un objeto String.
                #El numero de bytes a leer es el numero que es mas pequeno entre
                #bytes_faltantes y file_chunk_size
                bytes_leidos = archivo.read(min(bytes_faltantes, file_chunk_size))

                try:
                    #output es de tipo Socket. El metodo '.sendall' manda los datos al socket, el cual
                    #debe de estar conectado a un socket remoto. Este metodo manda todo el string especificado
                    #(no termina hasta que todo se halla enviado o un error ocurre).
                    output.sendall(bytes_leidos)

                #si hay un error entonces se lanza la excepcion socket.error la cual viene acompanada
                #de un Tuple (val,msg) donde val es el codigo del error y msg es el mensaje
                except socket.error, (val, msg):

                    # Si la conexion fue cerrada por el cliente
                    if val == 104:
                        Log.debug('El error va a ser ignorado: %s %s', val, msg)
                    else:
                        Log.error('Ocurrio un error: %s %s', val, msg)
                        raise

                #le restamos el file_chunk_size a los bytes_faltantes y volvemos a empezar.
                bytes_faltantes -= file_chunk_size


#devuelve el archivo que se encuentra en el path=(path archivos estaticos + request_uri)
def get_archivo(request_uri):

    #el path absoluto del archivo requerido es el path absoluto a la carpeta
    #de archivos estaticos + el path especificado en el request_uri
    path_archivo = STATIC_FILES_DIR + request_uri

    tamanno_archivo = None    #tamano del archivo
    existe = False  #flag de si existe el archivo o no
    mime_type = ''  #el tipo de archivo

    try:
        #si el archivo apunta a una carpeta entonces lanzamos una excepcion
        if os.path.isdir(path_archivo):
            raise Exception()

        tamanno_archivo = os.path.getsize(path_archivo) #obtenemos el tamano del archivo (en bytes)
        existe = True   #si la instruccion anterior no dio error entonces el archo existe

        #adivina el tipo del archivo basandose en su terminacion o en el url. Devuleve un Tuple
        #(tipo, encoding) donde tipo es un string 'tipo/subtipo' del archivo y el encoding
        #es None si no esta 'encoded' o sino es el nombre el programa usado para 'encode' el archivo
        tipo, encoding = mimetypes.guess_type(request_uri)
        if tipo:
            mime_type = tipo
    except:
        pass

    #retornamos un nuevo objeto File
    return File(request_uri, path_archivo, tamanno_archivo, existe, mime_type)
