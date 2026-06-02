#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 oled(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// =======================
// PIN SETUP
// =======================
#define BTN_ON       6
#define BTN_OFF      7

#define LAMP_1      22
#define LAMP_2      23
#define LAMP_3      24
#define LAMP_4      25

bool lampState = false;
bool autoMode = true;

unsigned long lastButtonTime = 0;
const unsigned long debounceDelay = 250;

// =======================
// OLED DISPLAY
// =======================
void updateOLED() {
  oled.clearDisplay();

  oled.setTextSize(1);
  oled.setTextColor(SSD1306_WHITE);

  oled.setCursor(0, 0);
  oled.println("SMART BILLIARD");

  oled.setCursor(0, 14);
  oled.print("Lampu : ");
  oled.println(lampState ? "ON" : "OFF");

  oled.setCursor(0, 28);
  oled.print("Mode  : ");
  oled.println(autoMode ? "AUTO" : "MANUAL");

  oled.setCursor(0, 42);
  oled.println("Meja  : 1");

  oled.setCursor(0, 54);
  oled.println("Serial Ready");

  oled.display();
}

// =======================
// OUTPUT
// =======================
void updateOutput() {
  digitalWrite(LAMP_1, lampState ? HIGH : LOW);
  digitalWrite(LAMP_2, lampState ? HIGH : LOW);
  digitalWrite(LAMP_3, lampState ? HIGH : LOW);
  digitalWrite(LAMP_4, lampState ? HIGH : LOW);

  updateOLED();
}

void sendStatus() {
  Serial.print("STATUS;");
  Serial.print("LAMP=");
  Serial.print(lampState ? "ON" : "OFF");
  Serial.print(";MODE=");
  Serial.println(autoMode ? "AUTO" : "MANUAL");
}

// =======================
// SERIAL COMMAND
// =======================
void processCommand(String cmd) {
  cmd.trim();
  cmd.toUpperCase();

  if (cmd == "PING") {
    Serial.println("READY");
    return;
  }

  else if (cmd == "ON") {
    lampState = true;
    Serial.println("LAMP_ON");
  }

  else if (cmd == "OFF") {
    lampState = false;
    Serial.println("LAMP_OFF");
  }

  else if (cmd == "AUTO") {
    autoMode = true;
    Serial.println("MODE_AUTO");
  }

  else if (cmd == "MANUAL") {
    autoMode = false;
    Serial.println("MODE_MANUAL");
  }

  else if (cmd == "STATUS") {
    sendStatus();
    return;
  }

  else {
    Serial.print("UNKNOWN_CMD:");
    Serial.println(cmd);
    return;
  }

  updateOutput();
  sendStatus();
}

// =======================
// SETUP
// =======================
void setup() {
  Serial.begin(9600);

  pinMode(BTN_ON, INPUT_PULLUP);
  pinMode(BTN_OFF, INPUT_PULLUP);

  pinMode(LAMP_1, OUTPUT);
  pinMode(LAMP_2, OUTPUT);
  pinMode(LAMP_3, OUTPUT);
  pinMode(LAMP_4, OUTPUT);

  if (!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED gagal");
    while (true);
  }

  oled.clearDisplay();
  oled.setTextSize(1);
  oled.setTextColor(SSD1306_WHITE);
  oled.setCursor(0, 0);
  oled.println("Smart Billiard");
  oled.setCursor(0, 16);
  oled.println("System Ready");
  oled.display();

  delay(1500);

  updateOutput();

  Serial.println("READY");
  sendStatus();
}

// =======================
// LOOP
// =======================
void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    processCommand(cmd);
  }

  if (digitalRead(BTN_ON) == LOW) {
    if (millis() - lastButtonTime > debounceDelay) {
      lampState = true;
      updateOutput();
      Serial.println("BUTTON_ON");
      sendStatus();
      lastButtonTime = millis();
    }
  }

  if (digitalRead(BTN_OFF) == LOW) {
    if (millis() - lastButtonTime > debounceDelay) {
      lampState = false;
      updateOutput();
      Serial.println("BUTTON_OFF");
      sendStatus();
      lastButtonTime = millis();
    }
  }
}