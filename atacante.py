import socket
import pyautogui

direccion_servidor = ('192.168.1.19', 7373)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(direccion_servidor)
while True:
    x, y = pyautogui.position()
    coordenadas = f"{x},{y}\n"
    sock.sendall(coordenadas.encode())
    pyautogui.sleep(0.1)
