#include <stdio.h>
#include <inttypes.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_chip_info.h"
#include "esp_flash.h"
#include "esp_system.h"

#include "bmi270.c"
#include "uart.c"

void start_reading(void) {
    char read_buffer[4];
    const char *uart_send_buffer;
    while (1) {
        int read_len = serial_read(read_buffer, 4);
        if (read_len > 0) {
            if strcmp(read_buffer, "STOP") == 0 {
                uart_write_bytes(UART_NUM, "OK\n", 3);
                break;
            }
        }
        get_acc(acc_array);
        uart_send_buffer = (const char *)acc_array;
        uart_write_bytes(UART_NUM, uart_send_buffer, 3 * sizeof(int16_t));
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

void start_conn(void) {
    char read_buffer[4];
    const char *uart_send_buffer;
    while (1) {
        int read_len = serial_read(read_buffer, 4);
        if (read_len > 0) {
            if strcmp(read_buffer, "TEST") == 0 {
                uart_write_bytes(UART_NUM, "OK\n", 3);
            }
            else if strcmp(read_buffer, "START") == 0 {
                uart_write_bytes(UART_NUM, "OK\n", 3);
                // Start reading
                start_reading();
            }
        }
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}

void app_main(void) {
    // Init UART
    uart_setup();

    // Init BME270
    ESP_ERROR_CHECK(bmi_init());
    softreset();
    chipid();
    initialization();
    check_initialization();
    bmipowermode();
    internal_status();

    // Start reading
    start_conn();
}