"""
Este mapa contiene todos los estados de http que nos puedan servir en la aplicacion. Estos errores
estan definidos en el RFC 2616 (o porlomenos este fue el que usamos de referencia)
"""
CODIGOS_ESTADO_HTTP = {
    200: ('OK', 'Request fulfilled, document follows'),
    404: ('Not Found', 'Nothing matches the given URI'),
}
