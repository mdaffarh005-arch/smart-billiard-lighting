#ifndef UART_H
#define UART_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

void UART_Init(uint32_t baud);

void UART_SendChar(char c);
void UART_SendString(const char *str);

uint8_t UART_Available(void);
char UART_ReadChar(void);

#ifdef __cplusplus
}
#endif

#endif