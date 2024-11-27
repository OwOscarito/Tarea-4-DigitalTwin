#include <string.h>
#include "driver/uart.h"
#include "esp_log.h"

#define BUF_SIZE (128)      // buffer size
#define TXD_PIN 1           // UART TX pin
#define RXD_PIN 3           // UART RX pin
#define UART_NUM UART_NUM_0 // UART port number
#define REDIRECT_LOGS 1 // if redirect ESP log to another UART

// Function for sending things to UART1
static int uart1_printf(const char *str, va_list ap) {
  char *buf;
  vasprintf(&buf, str, ap);
  uart_write_bytes(UART_NUM_1, buf, strlen(buf));
  free(buf);
  return 0;
}

// Setup of UART connections 0 and 1, and try to redirect logs to UART1 if asked
static void uart_setup() {
  uart_config_t uart_config = {
      .baud_rate = 115200,
      .data_bits = UART_DATA_8_BITS,
      .parity = UART_PARITY_DISABLE,
      .stop_bits = UART_STOP_BITS_1,
      .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
  };

  uart_param_config(UART_NUM_0, &uart_config);
  uart_param_config(UART_NUM_1, &uart_config);
  uart_driver_install(UART_NUM_0, BUF_SIZE * 2, 0, 0, NULL, 0);
  uart_driver_install(UART_NUM_1, BUF_SIZE * 2, 0, 0, NULL, 0);

  // Redirect ESP log to UART1
  if (REDIRECT_LOGS) {
    esp_log_set_vprintf(uart1_printf);
  }
}

// Read UART_num for input with timeout of 1 sec
int serial_read(char *buffer, int size) {
  int len =
      uart_read_bytes(UART_NUM, (uint8_t *)buffer, size, pdMS_TO_TICKS(1000));
  return len;
}

// Write UART_num with data from buffer 
void serial_write(char *buffer, int size) {
    uart_write_bytes(UART_NUM, (uint8_t *)buffer, size);
}
