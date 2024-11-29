import time
from struct import pack, unpack

import serial

# Se configura el puerto y el BAUD_Rate
PORT = "COM3"  # Esto depende del sistema operativo
BAUD_RATE = 115200  # Debe coincidir con la configuracion de la ESP32


# Se abre la conexion serial
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)


# Funciones
def send_message(bytes_format: str, message: bytes) -> None:
    """Funcion para enviar un mensaje a la ESP32."""
    ser.write(pack(bytes_format, message))


def receive_message() -> bytes:
    """Funcion para recibir un mensaje de la ESP32."""
    return ser.readline()


def receive_bytes(size: int) -> bytes:
    """Funcion para recibir un mensaje de la ESP32."""
    return ser.read(size)


def wait_message(message: bytes, timeout: int = 5) -> bool:
    """Funcion para esperar un mensaje especifico de la ESP32 en un tiempo maximo."""
    start_time = time.time()
    while True:
        timer = time.time() - start_time
        if timer > timeout:
            return False
        if ser.in_waiting > 0:
            try:
                response = receive_message()
                if message in response:
                    return True
            except: 
                continue


def test_conn() -> bool:
    """Funcion para testear la conexion a la ESP32."""
    # Se envia el mensaje de inicio de comunicacion
    send_message("5s", b"TEST\0")
    return wait_message(b"OK")

def receive_acc_data() -> tuple[float, float, float]:
    """Funcion para recibir los datos de la ESP32."""
    recv_bytes = receive_bytes(12)
    try:
        acc_x, acc_y, acc_z = unpack("fff", recv_bytes)
    except ValueError:
        return None
    else:
        return acc_x, acc_y, acc_z

if __name__ == "__main__":
    # Se inicia la conexion
    while True:
        if test_conn():
            print("Conexion exitosa")
            send_message("6s", b"START\0")
            if not wait_message(b"OK"):
                continue
            while True:
                acc_data = receive_acc_data()
                if acc_data:
                    print(f"Acelerometro: {acc_data}")
        else:
            print("Conexion fallida")
