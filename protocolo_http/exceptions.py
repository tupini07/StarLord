"""
Una excepcion costumizada que es tirada por http_request_parser cuando
se encuentra con un error
"""

#Es la excepcion que tira el http_request_parser en caso de error
class HttpParseException(Exception):
    pass
