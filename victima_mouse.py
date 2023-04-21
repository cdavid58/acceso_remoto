import socket
import mss
import mss.tools
from PIL import ImageGrab
import pyautogui

# Configuración del servidor
host = '192.168.1.19'
port = 7373

# Crea un socket y lo vincula al host y puerto especificados
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

# Espera a que un cliente se conecte y acepta la conexión
s.listen(1)
conn, addr = s.accept()
print('Conectado por', addr)

# Configuración de captura de pantalla
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
sct = mss.mss()

# Loop principal del servidor
while True:
    # Captura la pantalla y conviértela a un objeto de imagen
    sct_img = sct.grab(monitor)
    img = ImageGrab.grab()
    
    # Envía la imagen capturada al cliente
    with open("screenshot.png", "wb") as f:
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=f)
    with open("screenshot.png", "rb") as f:
        data = f.read()
        conn.sendall(data)

    # Recibe y procesa los datos del cliente
    try:
        data = conn.recv(1024).decode()
        if not data:
            break
        if data == "left_click":
            pyautogui.click(button="left")
        elif data == "right_click":
            pyautogui.click(button="right")
        elif data == "scroll_up":
            pyautogui.scroll(1)
        elif data == "scroll_down":
            pyautogui.scroll(-1)
        elif data.startswith("move"):
            _, x, y = data.split(":")
            x, y = int(x), int(y)
            pyautogui.moveTo(x, y)
    except ConnectionResetError:
        break

# Cierra la conexión y finaliza el programa
conn.close()
s.close()
