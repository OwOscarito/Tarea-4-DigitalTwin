import random
import logging

def receive_acc_data_fake() -> tuple[float, float, float]:
    """Funcion falsa para recibir los datos de la ESP32."""
    # recv_bytes = receive_bytes(struct.calcsize("fff"))
    # try:
    #     acc_x, acc_y, acc_z = struct.unpack("fff", recv_bytes)
    # except struct.error:
    #     logging.debug("Error unpacking data")
    #     return None
    # else:
    #     return acc_x, acc_y, acc_z

    acc_x = random.uniform(-1, 1)
    acc_y = random.uniform(-1, 1)
    acc_z = random.uniform(-1, 1)

    return acc_x, acc_y, acc_z

def start_receiving_fake():
    """Función para iniciar la conexión"""
    # while True:
    #     if test_conn():
    #         print("Conexion exitosa")
    #         send_message("6s", b"START\0")
    #         if not wait_message(b"OK"):
    #             continue
    #         while True:
    #             if ser.in_waiting > 0:
    #                 acc_data = receive_acc_data()
    #                 if acc_data:
    #                     print(f"Acelerometro: {acc_data}")
    #     else:
    #         print("Conexion fallida")

    while True:
        acc_data = receive_acc_data_fake()
        if acc_data:
            print(f"Acelerometro (fake): {acc_data}")
            return acc_data

if __name__ == "__main__":
    LOGGING_FORMAT = "%(levelname)s - <%(funcName)s>: %(message)s"
    logging.basicConfig(format=LOGGING_FORMAT,
                        style="%",
                        level=logging.DEBUG)
    
    start_receiving_fake()