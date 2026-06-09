#include <Arduino.h>

extern "C"
{
    #include "gpio.h"
    #include "uart.h"
    #include "timer.h"
    #include "billiard.h"
}

#include "oled.h"

char serialBuffer[64];
uint8_t serialIndex = 0;

uint32_t oledUpdateTimer = 0;
uint32_t serialUpdateTimer = 0;

void setup()
{
    GPIO_Init();

    UART_Init(9600);

    Timer_Init();

    OLED_Init();

    Billiard_Init();

    UART_SendString("SMART_BILLIARD_READY\r\n");
}

void loop()
{
    if(!systemEnabled)
    {
        if(StartButtonPressed())
        {
            delay(50);

            if(StartButtonPressed())
            {
                systemEnabled = true;

                UART_SendString("SYSTEM_ON\r\n");

                while(StartButtonPressed());
            }
        }
    }

    if(EmergencyButtonPressed())
    {
        stopAllTables();

        systemEnabled = false;

        UART_SendString("EMERGENCY\r\n");

        delay(300);

        while(EmergencyButtonPressed());
    }

    while(UART_Available())
    {
        char c = UART_ReadChar();

        if(c == '\r')
            continue;

        if(c == '\n')
        {
            serialBuffer[serialIndex] = '\0';

            processCommand(serialBuffer);

            serialIndex = 0;
        }
        else
        {
            if(serialIndex < sizeof(serialBuffer) - 1)
            {
                serialBuffer[serialIndex++] = c;
            }
        }
    }

    updateTables();

    if(millis() - oledUpdateTimer >= 500)
    {
        oledUpdateTimer = millis();

        drawOLED();
    }

    if(millis() - serialUpdateTimer >= 1000)
    {
        serialUpdateTimer = millis();

        sendStatusToGUI();
    }
}