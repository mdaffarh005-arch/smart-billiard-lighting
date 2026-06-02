# 💡 Smart Billiard Lighting

## 📂 Folder Software
Berisi source code utama untuk mengontrol sistem pencahayaan meja biliar.

---

## 🔧 Hardware Setup (Wokwi Diagram)

### Komponen Utama
- **Arduino Mega 2560**
- **ESP32 Devkit V1**
- **Breadboard Half**
- **4 LED merah (L1–L4)** dengan resistor 220Ω
- **2 Push Button** (hijau = ON/OFF, biru = kontrol tambahan)
- **OLED SSD1306 (I2C, address 0x3C)** untuk monitor status

### 📑 Koneksi Penting
- LED1 → Pin 22 (via resistor 220Ω)  
- LED2 → Pin 23 (via resistor 220Ω)  
- LED3 → Pin 24 (via resistor 220Ω)  
- LED4 → Pin 25 (via resistor 220Ω)  
- OLED SCL → Pin 21 (Arduino Mega)  
- OLED SDA → Pin 20 (Arduino Mega)  
- ESP32 RX0 ↔ Arduino Mega Pin 18  
- ESP32 TX0 ↔ Arduino Mega Pin 19  
- Push Button hijau → Pin 7 (Mega)  
- Push Button biru → Pin 6 (Mega)  
- Semua GND terhubung ke rail negatif breadboard  
- VCC OLED terhubung ke 5V rail breadboard  

---

## 📊 Fungsi Sistem
- Tombol **hijau**: start sistem.  
- Tombol **biru**: stop sistem.  
- **OLED**: menampilkan status sistem meja yang aktif (lampu aktif, mode, dll).  
- **ESP32**: komunikasi serial dengan Arduino Mega untuk integrasi IoT.  

---
## 🚀 Fitur Sistem

✅ Kontrol 4 meja biliar independen

✅ Monitoring OLED real-time

✅ Tombol Start dan Emergency

✅ Komunikasi Serial Mega ↔ ESP32

✅ Integrasi GUI Desktop

✅ Dukungan IoT dan MQTT

✅ Status meja real-time

✅ Update otomatis setiap detik

---

## 📌 Catatan
- File `diagram.json` adalah blueprint rangkaian di Wokwi.  
- Pastikan library **Adafruit SSD1306** dan **Wire** sudah terpasang di Arduino IDE.  
- ESP32 bisa digunakan untuk koneksi WiFi/MQTT agar sistem bisa dikontrol jarak jauh.  
