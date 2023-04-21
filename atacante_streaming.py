import numpy as np
import cv2
import socket

# Dimensiones de la pantalla
WIDTH, HEIGHT = 1920, 1080

# Iniciar cliente de socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.19', 8000))

# Iniciar ventana para mostrar el streaming
cv2.namedWindow('Remote', cv2.WINDOW_NORMAL)

while True:
    # Recibir imagen del servidor
    try:
        data = b''
        while len(data) < WIDTH * HEIGHT * 3:
            packet = client_socket.recv(WIDTH * HEIGHT * 3 - len(data))
            if not packet:
                break
            data += packet

        # Convertir datos a una imagen de OpenCV
        frame = np.frombuffer(data, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))
        
        # Mostrar imagen en ventana
        cv2.imshow('Remote', frame)

        # Esperar 1ms para permitir la actualización de la ventana
        if cv2.waitKey(1) == ord('q'):
            break
    except:
        break

# Cerrar conexión y ventana
client_socket.close()
cv2.destroyAllWindows()
