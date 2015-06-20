# StarLord
Servicor HTTP hecho en Python 2.7. Pensado para facilitar el envio de archivos entre dispositivos conectados a una misma red local.

Para levantar el servidor simplemente hay que ejecutar desde la consola el siguiente comando:

`python star_lord.py`

Los archivos que se desean compartir hay que ponerlos en la carpeta de 'archivos_s'. Por el momento solo se pueden poner archivos que no tengan espacios en su nombre (si fuera el caso, nadamas hay que renombrarlos eliminando los espacios).

Para accesar el servidor desde cualquier dispositivo que este conectado a la misma red local nadamas hay que hacer un GET request al <ip_servidor>:<puerto>. Una manera de hacer esto es simplemente abriendo un navegador e ingresar en la barra de direccion (el ip local de la computadora que esta ejecutando el servidor:el puerto de la computadora).

#Cosas Que Hay Que Hacer
<ul>
  <li>Hacer que se pueden pasar archivos que contengan espacios en su nombre</li>
  <li>Que se pueda especificar por parametro, al ejecutar el servidor, el puerto en el que se quiere escuchar por peticiones</li>
  <li>Permitrle al usuario limitar el servidor a una interfaz de red especifica, y desplegarle la direccion IP local de esta</li>
</ul>
