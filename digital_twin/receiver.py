import struct
import time

import serial
import logging
# Se configura el puerto y el BAUD_Rate
PORT = "COM3"  # Esto depende del sistema operativo
BAUD_RATE = 115200  # Debe coincidir con la configuracion de la ESP32


# Se abre la conexion serial
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)


# Funciones
def send_message(bytes_format: str, message: bytes) -> None:
    """Funcion para enviar un mensaje a la ESP32."""
    logging.debug("[%s]", message)
    ser.write(struct.pack(bytes_format, message))


def receive_message() -> bytes:
    """Funcion para recibir un mensaje de la ESP32."""
    recv_message = ser.readline()
    logging.debug("[%s]", recv_message)
    return recv_message

def receive_bytes(size: int) -> bytes:
    """Funcion para recibir un mensaje de la ESP32."""
    recv_bytes = ser.read(size)
    logging.debug("(req=%s, size=%s) [%s]", size, len(recv_bytes), recv_bytes)
    return recv_bytes


def wait_message(message: bytes, timeout: int = 5) -> bool:
    """Funcion para esperar un mensaje especifico de la ESP32 en un tiempo maximo."""
    logging.info("Waiting for %s", message)
    start_time = time.time()
    while True:
        timer = time.time() - start_time
        if timer > timeout:
            logging.info("NOT received")
            return False
        if ser.in_waiting > 0:
            try:
                response = receive_message()
                if response.startswith(message):
                    logging.info("Received")
                    return True
            except:
                continue


def test_conn() -> bool:
    """Funcion para testear la conexion a la ESP32."""
    # Se envia el mensaje de inicio de comunicacion
    send_message("6s", b"TEST\0\0")
    return wait_message(b"OK")

def receive_acc_data() -> tuple[float, float, float]:
    """Funcion para recibir los datos de la ESP32."""
    recv_bytes = receive_bytes(struct.calcsize("fff"))
    try:
        acc_x, acc_y, acc_z = struct.unpack("fff", recv_bytes)
    except struct.error:
        logging.debug("Error unpacking data")
        return None
    else:
        return acc_x, acc_y, acc_z

if __name__ == "__main__":
    LOGGING_FORMAT = "%(levelname)s - <%(funcName)s>: %(message)s"
    logging.basicConfig(format=LOGGING_FORMAT,
                        style="%",
                        level=logging.DEBUG)
    # Se inicia la conexion
    while True:
        if test_conn():
            print("Conexion exitosa")
            send_message("6s", b"START\0")
            if not wait_message(b"OK"):
                continue
            while True:
                if ser.in_waiting > 0:
                    acc_data = receive_acc_data()
                    if acc_data:
                        print(f"Acelerometro: {acc_data}")
        else:
            print("Conexion fallida")
