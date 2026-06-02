#include "gpio.h"

void GPIO_Init(void)
{
    DDRA |= (1 << PA0);
    DDRA |= (1 << PA1);
    DDRA |= (1 << PA2);
    DDRA |= (1 << PA3);

    DDRH &= ~(1 << PH4);
    DDRH &= ~(1 << PH3);

    PORTH |= (1 << PH4);
    PORTH |= (1 << PH3);
}

void Relay_On(uint8_t relay)
{
    PORTA |= (1 << relay);
}

void Relay_Off(uint8_t relay)
{
    PORTA &= ~(1 << relay);
}

uint8_t StartButtonPressed(void)
{
    return !(PINH & (1 << PH4));
}

uint8_t EmergencyButtonPressed(void)
{
    return !(PINH & (1 << PH3));
}