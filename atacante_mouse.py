import socket
import time
from PIL import Image
import pyautogui

# Tamaño de la pantalla
screenWidth, screenHeight = pyautogui.size()

# Crea el socket y espera la conexión del cliente
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.1.19', 7373))
server_socket.listen(1)
client_socket, client_address = server_socket.accept()

# Función para enviar los comandos de movimiento del cursor al servidor
def send_commands():
    while True:
        # Obtiene las coordenadas del cursor
        x, y = pyautogui.position()
        
        # Envía el comando de movimiento al servidor
        client_socket.send(f"move {x/screenWidth} {y/screenHeight}".encode('utf-8'))
        time.sleep(0.05)

# Función para recibir la transmisión de la pantalla del servidor
def receive_screen():
    with mss.mss() as sct:
        while True:
            # Captura la pantalla del servidor
            img = sct.grab(sct.monitors[1])
            # Convierte la imagen a formato RGB
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            # Envía la imagen al cliente
            img_bytes = img.tobytes()
            client_socket.send(img_bytes)

# Inicia las funciones para enviar los comandos de movimiento del cursor y recibir la transmisión de la pantalla del servidor
send_commands_thread = threading.Thread(target=send_commands)
receive_screen_thread = threading.Thread(target=receive_screen)
send_commands_thread.start()
receive_screen_thread.start()
