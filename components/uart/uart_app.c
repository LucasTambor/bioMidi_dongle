#include "uart_app.h"
#include "uart_driver.h"
#include "esp_log.h"
#include <string.h>

static const char *TAG = "UART_App";

QueueHandle_t xQueueUartWriteBuffer;

void vDataStream( void *pvParameters ) {
    uart_data_t lReceivedValue;

    // Init Queue
    xQueueUartWriteBuffer = xQueueCreate(16, sizeof(uart_data_t));

    // Init UART
    ESP_ERROR_CHECK(uart_init());

	// Signalize task successfully creation
    ESP_LOGI(TAG, "Data Stream Initialized");

    while(1) {
        if( xQueueReceive( xQueueUartWriteBuffer, (void *)&lReceivedValue, portMAX_DELAY ) == pdPASS ) {
            esp_log_buffer_hex(TAG, lReceivedValue.data, lReceivedValue.len);
            if(!uart_write((char *)lReceivedValue.data, lReceivedValue.len)) {
                ESP_LOGE(TAG, "ERROR WRITING DATA");
            }else{
                ESP_LOGI(TAG, "Sent %d bytes", lReceivedValue.len);
            }
        }

        // vTaskDelay( 20 / portTICK_RATE_MS );
    }
}
