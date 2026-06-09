#include "oled.h"

#include <Arduino.h>
#include <Wire.h>

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

extern "C"
{
#include "billiard.h"
}

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    &Wire,
    -1);

void OLED_Init(void)
{
    Wire.begin();

    display.begin(
        SSD1306_SWITCHCAPVCC,
        0x3C);

    display.clearDisplay();
    display.display();
}

void drawOLED(void)
{
    display.clearDisplay();

    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);

    if(!systemEnabled)
    {
        display.setCursor(15, 10);
        display.println("SMART BILLIARD");

        display.setCursor(20, 30);
        display.println("PRESS START");
    }
    else
    {
        display.setCursor(0, 0);
        display.println("SYSTEM READY");

        for(int i = 0; i < 4; i++)
        {
            display.setCursor(0, 16 + (i * 12));

            display.print("M");
            display.print(i + 1);
            display.print(": ");

            if(tables[i].active)
            {
                uint32_t totalSec = tables[i].remainSec;

                uint16_t hour = totalSec / 3600;
                uint16_t min = (totalSec % 3600) / 60;
                uint16_t sec = totalSec % 60;

                if(hour < 10)
                    display.print("0");
                display.print(hour);

                display.print(":");

                if(min < 10)
                    display.print("0");
                display.print(min);

                display.print(":");

                if(sec < 10)
                    display.print("0");
                display.print(sec);
            }
            else
            {
                display.print("OFF");
            }
        }
    }

    display.display();
}