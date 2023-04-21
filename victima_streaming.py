import numpy as np
import cv2
import pyautogui
import socket

# Dimensiones de la pantalla
WIDTH, HEIGHT = 1920, 1080

# Iniciar servidor de socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.1.19', 8000))
server_socket.listen(0)

# Aceptar conexión de cliente
client_socket, _ = server_socket.accept()

# Iniciar captura de pantalla
while True:
    # Capturar pantalla
    screenshot = pyautogui.screenshot()

    # Convertir captura de pantalla a una imagen de OpenCV
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Redimensionar imagen a las dimensiones esperadas
    frame = cv2.resize(frame, (WIDTH, HEIGHT))

    # Enviar imagen al cliente
    try:
        client_socket.sendall(frame.tobytes())
    except:
        break

# Cerrar conexión
client_socket.close()
server_socket.close()
