#ifndef _UART_APP_H_
#define _UART_APP_H_

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "freertos/event_groups.h"

extern QueueHandle_t xQueueUartWriteBuffer;

typedef struct UART_data_s
{
    uint8_t data[64];        // Data value
    size_t len;            // Data lenght
}uart_data_t;


void vDataStream( void *pvParameters );


#endif //_UART_APP_
