#include "uart.h"
#include <avr/io.h>

void UART_Init(uint32_t baud)
{
    uint16_t ubrr = (F_CPU / 16 / baud) - 1;

    UBRR0H = ubrr >> 8;
    UBRR0L = ubrr;

    UCSR0B =
        (1 << RXEN0) |
        (1 << TXEN0);

    UCSR0C =
        (1 << UCSZ01) |
        (1 << UCSZ00);
}

void UART_SendChar(char c)
{
    while (!(UCSR0A & (1 << UDRE0)));

    UDR0 = c;
}

void UART_SendString(const char *str)
{
    while (*str)
    {
        UART_SendChar(*str++);
    }
}

uint8_t UART_Available(void)
{
    return (UCSR0A & (1 << RXC0));
}

char UART_ReadChar(void)
{
    return UDR0;
}