#ifndef BILLIARD_H
#define BILLIARD_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct
{
    bool active;
    uint32_t endTime;
    uint32_t remainSec;
} TableData;

extern TableData tables[4];
extern bool systemEnabled;

void Billiard_Init(void);

void startTable(uint8_t index, uint16_t minutes);
void stopTable(uint8_t index);
void stopAllTables(void);

void processCommand(char *cmd);

void updateTables(void);

void sendStatusToGUI(void);

#ifdef __cplusplus
}
#endif

#endif