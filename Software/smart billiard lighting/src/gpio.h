#ifndef GPIO_H
#define GPIO_H

#include <avr/io.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

void GPIO_Init(void);

void Relay_On(uint8_t relay);
void Relay_Off(uint8_t relay);

uint8_t StartButtonPressed(void);
uint8_t EmergencyButtonPressed(void);

#ifdef __cplusplus
}
#endif

#endif