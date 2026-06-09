#include "billiard.h"
#include "gpio.h"
#include "uart.h"
#include "timer.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

TableData tables[4];

bool systemEnabled = false;

void stopTable(uint8_t index)
{
    tables[index].active = false;
    tables[index].remainSec = 0;
    tables[index].endTime = 0;

    Relay_Off(index);

    char buffer[32];
    sprintf(buffer, "TIMEUP:%d\r\n", index + 1);
    UART_SendString(buffer);
}

void stopAllTables(void)
{
    for(uint8_t i = 0; i < 4; i++)
    {
        Relay_Off(i);

        tables[i].active = false;
        tables[i].remainSec = 0;
        tables[i].endTime = 0;
    }
}

void startTable(uint8_t index, uint16_t minutes)
{
    if(index > 3)
        return;

    tables[index].active = true;
    tables[index].remainSec = (uint32_t)minutes * 60UL;
    tables[index].endTime = millis() + ((uint32_t)minutes * 60000UL);

    Relay_On(index);
}

void Billiard_Init(void)
{
    stopAllTables();
}

void processCommand(char *cmd)
{
    if(cmd == NULL)
        return;

    if(strncmp(cmd, "ON:", 3) == 0)
    {
        int meja = atoi(cmd + 3);

        if(meja >= 1 && meja <= 4)
        {
            uint8_t index = meja - 1;

            Relay_On(index);

            tables[index].active = true;
            tables[index].remainSec = 0;
            tables[index].endTime = 0;

            char buffer[32];
            sprintf(buffer, "LAMP_ON:%d\r\n", meja);
            UART_SendString(buffer);
        }
    }

    else if(strncmp(cmd, "OFF:", 4) == 0)
    {
        int meja = atoi(cmd + 4);

        if(meja >= 1 && meja <= 4)
        {
            uint8_t index = meja - 1;

            Relay_Off(index);

            tables[index].active = false;
            tables[index].remainSec = 0;
            tables[index].endTime = 0;

            char buffer[32];
            sprintf(buffer, "LAMP_OFF:%d\r\n", meja);
            UART_SendString(buffer);
        }
    }

    else if(cmd[0] == 'M')
    {
        char *comma = strchr(cmd, ',');

        if(comma)
        {
            int meja = atoi(cmd + 1);
            int menit = atoi(comma + 1);

            if(meja >= 1 && meja <= 4)
            {
                startTable(meja - 1, menit);

                char buffer[32];
                sprintf(buffer, "START:%d:%d\r\n", meja, menit);
                UART_SendString(buffer);
            }
        }
    }

    else if(strncmp(cmd, "STOP", 4) == 0)
    {
        char *comma = strchr(cmd, ',');

        if(comma)
        {
            int meja = atoi(comma + 1);

            if(meja >= 1 && meja <= 4)
            {
                stopTable(meja - 1);
            }
        }
    }

    else if(strcmp(cmd, "RESET") == 0)
    {
        stopAllTables();
    }

    else
    {
        char buffer[64];
        sprintf(buffer, "UNKNOWN_CMD:%s\r\n", cmd);
        UART_SendString(buffer);
    }
}

void updateTables(void)
{
    uint32_t now = millis();

    for(uint8_t i = 0; i < 4; i++)
    {
        if(tables[i].active && tables[i].endTime > 0)
        {
            if(now >= tables[i].endTime)
            {
                stopTable(i);
            }
            else
            {
                tables[i].remainSec = (tables[i].endTime - now) / 1000UL;
            }
        }
    }
}

void sendStatusToGUI(void)
{
    char buffer[64];

    for(uint8_t i = 0; i < 4; i++)
    {
        sprintf(
            buffer,
            "T%d:%s:%lu\r\n",
            i + 1,
            tables[i].active ? "ON" : "OFF",
            (unsigned long)tables[i].remainSec
        );

        UART_SendString(buffer);
    }

    sprintf(
        buffer,
        "SYSTEM:%s\r\n",
        systemEnabled ? "READY" : "OFF"
    );

    UART_SendString(buffer);
    UART_SendString("---\r\n");
}