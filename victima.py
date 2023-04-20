import socket
import pyautogui

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
direccion_servidor = ('192.168.1.19', 7373)
sock.bind(direccion_servidor)
sock.listen(1)
print('Esperando una conexión entrante...')
conexion, direccion_cliente = sock.accept()
print('Conexión aceptada desde', direccion_cliente)
while True:
    datos = conexion.recv(1024)
    if not datos:
        break
    coordenadas = datos.decode().strip().split(',')
    x = int(coordenadas[0])
    y = int(coordenadas[1])
    screen_size = pyautogui.size()
    x = max(0, min(x, screen_size.width))
    y = max(0, min(y, screen_size.height))
    pyautogui.moveTo(x, y)
conexion.close()
sock.close()
