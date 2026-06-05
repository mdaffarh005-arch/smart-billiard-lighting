# Hardware

# Isi Folder
- File Schematic (EasyEDA)
- File PCB Layout
- 3D PCB View
- Wiring Diagram (Fritzing)


# Arduino Mega 2560
Berfungsi sebagai pengendali utama sistem:
Mengelola logika program billing
Mengontrol relay lampu meja biliar
Membaca input tombol ON/OFF
Mengirim dan menerima data dengan ESP32
Mengendalikan tampilan OLED

# ESP32 DevKitC
Digunakan sebagai modul komunikasi:
Koneksi Wi-Fi ke aplikasi atau server
Monitoring status sistem secara real-time
Pertukaran data dengan Arduino Mega melalui UART

# Logic Level Converter
Digunakan untuk menyesuaikan level tegangan komunikasi:
Konversi sinyal 5V ↔ 3.3V
Melindungi ESP32 dari level tegangan Arduino Mega

# Relay Module 1 Channel
Digunakan untuk mengendalikan lampu meja biliar:
Relay 1 → Lampu Meja 1
Relay 2 → Lampu Meja 2
Relay 3 → Lampu Meja 3
Relay 4 → Lampu Meja 4
Isolasi antara rangkaian kontrol dan beban lampu

# OLED Display SSD1306
Berfungsi sebagai tampilan informasi sistem:
Status koneksi
Informasi billing
Waktu bermain
Status lampu meja

# Push Button
Digunakan sebagai kontrol manual:
Tombol ON untuk mengaktifkan sistem atau fungsi tertentu
Tombol OFF untuk menghentikan atau membatalkan proses

# Power Supply
Rangkaian catu daya terdiri dari:
Input tegangan 12V DC

# Modul step-down LM2596
Output 5V untuk Arduino, relay, dan periferal
Output 3.3V untuk ESP32 dan rangkaian logika

# Koneksi Sistem
Komunikasi Arduino Mega ↔ ESP32
TX2 Arduino (D16) → RX2 ESP32 melalui Level Converter
RX2 Arduino (D17) → TX2 ESP32 melalui Level Converter
Komunikasi menggunakan protokol UART Serial
OLED Display
SDA → D20 (SDA)
SCL → D21 (SCL)
Menggunakan komunikasi I2C
Input Push Button
Tombol ON → D7
Tombol OFF → D8
Output Relay
Relay 1 → D22
Relay 2 → D23
Relay 3 → D24
Relay 4 → D25


# Desain PCB
PCB dirancang untuk:
Mengintegrasikan seluruh komponen dalam satu board
Mempermudah instalasi dan perawatan sistem
Mengurangi penggunaan kabel eksternal
Menyediakan konektor terminal untuk beban lampu dan catu daya

# 3D View
Visualisasi 3D digunakan untuk:
Memverifikasi posisi komponen
Memastikan tidak terjadi benturan antar komponen
Membantu proses fabrikasi dan perakitan PCB

# Wiring Diagram (Fritzing)
Diagram wiring digunakan sebagai panduan:
Penyambungan antar modul
Identifikasi pin koneksi
Referensi perakitan prototipe sebelum PCB diproduksi

# Tools
- EasyEDA
- Fritzing

## Designer
Imam Syaifudin
