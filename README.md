# 🎱 Smart Billiard Lighting & Billing System

![GitHub Header Banner](https://capsule-render.vercel.app/render?type=waving&color=auto&height=220&section=header&text=Smart%20Billiard%20Lighting%20%26%20Billing%20System&fontSize=32&animation=fadeIn&theme=dark)

<p align="center">
  <img src="https://img.shields.io/badge/Status-Complete-green?style=for-the-badge&logo=github" alt="Status">
  <img src="https://img.shields.io/badge/Microcontroller-ATmega2560-blue?style=for-the-badge&logo=arduino" alt="MCU">
  <img src="https://img.shields.io/badge/Embedded_System-IoT_Project-orange?style=for-the-badge" alt="Project">
</p>

---

### 📖 Overview
**Smart Billiard Lighting & Billing System** merupakan solusi otomatisasi berbasis mikrokontroler **ATmega2560** untuk membantu pengelolaan arena biliar. Sistem ini menghubungkan aplikasi kasir dengan perangkat keras melalui komunikasi serial UART sehingga status penggunaan meja dapat dipantau dan dikendalikan secara *real-time*.

Selain mengontrol sakelar lampu meja secara otomatis melalui modul relay, sistem ini juga mampu mencatat durasi bermain pelanggan, menghitung biaya sewa berdasarkan tarif per menit fleksibel, serta meminimalkan risiko celah kebocoran keuangan (*revenue leakage*).

---

### 🎯 Objectives
* 💡 **Mengurangi pemborosan energi listrik** pada meja biliar lewat otomasi relay.
* ⏱️ **Mengotomatisasi pencatatan durasi bermain** pelanggan secara presisi.
* 🧮 **Menghitung biaya sewa otomatis** berdasarkan akumulasi waktu penggunaan.
* 🛡️ **Mengurangi human error** dan kebocoran pendapatan dalam operasional bisnis.
* 📈 **Meningkatkan efisiensi** tata kelola meja dan rekapitulasi transaksi kasir.

---

### ✨ Features

* **⏱️ Real-Time Timer:** Menampilkan durasi bermain setiap meja secara *real-time*.
* **💰 Flexible Pricing:** Harga sewa per jam dapat diatur fleksibel sesuai kebutuhan operasional.
* **🧮 Automatic Billing:** Akumulasi total biaya dihitung otomatis berdasarkan durasi penggunaan meja.
* **💡 Smart Lighting Control:** Lampu meja menyala dan mati secara otomatis mengikuti status billing meja.
* **🎛️ Manual & Automatic Mode:** Mendukung pengoperasian sakelar secara otomatis maupun kontrol manual.
* **📊 Monitoring Dashboard:** Menampilkan status meja, durasi bermain, dan total biaya dalam satu tampilan GUI.
* **💲 Income Automatic Monitoring:** Menghitung otomatis total akumulasi pendapatan yang diperoleh kasir.

---

### 🗺️ System Architecture & Workflow

```mermaid
flowchart TD
    A[Kasir Dashboard] --> B[Serial Communication]
    B --> C[ATmega2560]
    C --> D[Timer]
    C --> E[Billing]
    C --> F[Relay]
    D --> G[Durasi Bermain]
    E --> H[Total Biaya]
    F --> I[Lampu Meja]
    
    style C fill:#1f6feb,stroke:#fff,stroke-width:2px,color:#fff
    style A fill:#238636,stroke:#fff,stroke-width:1px,color:#fff
    style I fill:#d29922,stroke:#fff,stroke-width:1px,color:#black