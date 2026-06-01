import customtkinter as ctk
from datetime import datetime

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Billiard Lighting")
app.geometry("1350x760")
app.configure(fg_color="#f5f7fb")

BLUE = "#3f55f6"
BLUE_DARK = "#2636d9"
TEXT = "#111827"
MUTED = "#64748b"
GREEN = "#22c55e"
RED = "#ef4444"
YELLOW = "#f5b400"
WHITE = "#ffffff"
DARK = "#111827"
BORDER = "#eef1f6"
GRAY = "#cbd5e1"

arduino_connected = False


def add_log(message):
    time_now = datetime.now().strftime("%H:%M:%S")
    log_box.insert("end", f"[{time_now}]  {message}\n")
    log_box.see("end")


def update_clock():
    clock_label.configure(text=datetime.now().strftime("%d/%m/%Y\n%H:%M:%S"))
    app.after(1000, update_clock)


def connect_arduino():
    global arduino_connected
    arduino_connected = True

    arduino_status.configure(text="● Arduino\nConnected", text_color=GREEN)
    connect_button.configure(text="ARDUINO CONNECTED", fg_color=GREEN)
    connection_info.configure(
        text="Arduino Mega      ● Connected\n"
             "Billing App       ● Connected\n"
             "Relay Lampu       ● Standby\n"
             "Database          ● Connected"
    )
    add_log("Arduino Mega terhubung pada COM3")


def set_auto():
    mode_value.configure(text="AUTO", text_color=BLUE)
    add_log("Mode sistem diubah ke AUTO")


def set_manual():
    mode_value.configure(text="MANUAL", text_color=YELLOW)
    add_log("Mode sistem diubah ke MANUAL")


def lamp_on():
    lamp_value.configure(text="ON", text_color=GREEN)
    add_log("Lampu meja 1 dinyalakan")


def lamp_off():
    lamp_value.configure(text="OFF", text_color=RED)
    add_log("Lampu meja 1 dimatikan")


sidebar = ctk.CTkFrame(app, width=150, corner_radius=0, fg_color=WHITE)
sidebar.pack(side="left", fill="y")

main = ctk.CTkFrame(app, fg_color="#f5f7fb", corner_radius=0)
main.pack(side="left", fill="both", expand=True, padx=25, pady=25)

ctk.CTkLabel(
    sidebar,
    text="SBL",
    text_color=BLUE,
    font=("Segoe UI", 30, "bold")
).pack(anchor="w", padx=18, pady=(35, 0))

ctk.CTkLabel(
    sidebar,
    text="Smart Billiard\nLighting",
    text_color=TEXT,
    font=("Segoe UI", 10, "bold"),
    justify="left"
).pack(anchor="w", padx=18, pady=(0, 25))

menus = [
    ("⌂  Dashboard", True),
    ("▣  Monitoring", False),
    ("◉  Kontrol", False),
    ("▤  Billing", False),
    ("▦  Meja", False),
    ("◷  Riwayat", False),
    ("⚙  Setting", False),
]

for text, active in menus:
    ctk.CTkButton(
        sidebar,
        text=text,
        height=36,
        corner_radius=12,
        fg_color=BLUE if active else WHITE,
        hover_color="#e8edff",
        text_color=WHITE if active else MUTED,
        font=("Segoe UI", 11, "bold" if active else "normal"),
        anchor="w"
    ).pack(fill="x", padx=12, pady=4)

promo = ctk.CTkFrame(sidebar, height=145, corner_radius=20, fg_color=BLUE)
promo.pack(side="bottom", fill="x", padx=12, pady=22)
promo.pack_propagate(False)

ctk.CTkLabel(
    promo,
    text="8",
    width=45,
    height=38,
    corner_radius=12,
    fg_color=WHITE,
    text_color=BLUE,
    font=("Segoe UI", 22, "bold")
).pack(pady=(16, 5))

ctk.CTkLabel(
    promo,
    text="Smart Control",
    text_color=WHITE,
    font=("Segoe UI", 13, "bold")
).pack()

ctk.CTkLabel(
    promo,
    text="Kontrol lampu,\nwaktu, billing.",
    text_color=WHITE,
    font=("Segoe UI", 8),
    justify="center"
).pack(pady=6)


header = ctk.CTkFrame(main, fg_color="transparent")
header.pack(fill="x")

title_area = ctk.CTkFrame(header, fg_color="transparent")
title_area.pack(side="left")

ctk.CTkLabel(
    title_area,
    text="Smart Billiard Lighting",
    text_color=TEXT,
    font=("Segoe UI", 28, "bold")
).pack(anchor="w")

ctk.CTkLabel(
    title_area,
    text="Dashboard kontrol lampu meja billiard berbasis Arduino Mega",
    text_color=MUTED,
    font=("Segoe UI", 11)
).pack(anchor="w")

status_area = ctk.CTkFrame(header, fg_color="transparent")
status_area.pack(side="right")

arduino_status = ctk.CTkLabel(
    status_area,
    text="● Arduino\nDisconnected",
    width=130,
    height=55,
    corner_radius=16,
    fg_color=WHITE,
    text_color=RED,
    font=("Segoe UI", 10, "bold")
)
arduino_status.pack(side="left", padx=7)

billing_status = ctk.CTkLabel(
    status_area,
    text="● Billing\nConnected",
    width=130,
    height=55,
    corner_radius=16,
    fg_color=WHITE,
    text_color=GREEN,
    font=("Segoe UI", 10, "bold")
)
billing_status.pack(side="left", padx=7)

clock_label = ctk.CTkLabel(
    status_area,
    text="",
    width=130,
    height=55,
    corner_radius=16,
    fg_color=WHITE,
    text_color=TEXT,
    font=("Segoe UI", 10, "bold")
)
clock_label.pack(side="left", padx=7)


hero = ctk.CTkFrame(main, height=72, corner_radius=22, fg_color=BLUE)
hero.pack(fill="x", pady=(22, 14))
hero.pack_propagate(False)

ctk.CTkLabel(
    hero,
    text="Dashboard Kontrol Lampu Meja Billiard",
    text_color=WHITE,
    font=("Segoe UI", 20, "bold")
).pack(anchor="w", padx=28, pady=(13, 0))

ctk.CTkLabel(
    hero,
    text="Sistem pengaturan lampu otomatis berbasis Arduino Mega dan aplikasi billing.",
    text_color=WHITE,
    font=("Segoe UI", 10)
).pack(anchor="w", padx=28)


cards = ctk.CTkFrame(main, fg_color="transparent")
cards.pack(fill="x", pady=(0, 14))


def status_card(parent, title, value, subtitle, color, bg_color):
    frame = ctk.CTkFrame(
        parent,
        height=105,
        corner_radius=24,
        fg_color=bg_color,
        border_width=1,
        border_color=BORDER
    )
    frame.pack(side="left", fill="both", expand=True, padx=8)
    frame.pack_propagate(False)

    ctk.CTkFrame(
        frame,
        width=8,
        height=62,
        corner_radius=6,
        fg_color=color
    ).pack(side="left", padx=(18, 10), pady=22)

    text_area = ctk.CTkFrame(frame, fg_color="transparent")
    text_area.pack(side="left", fill="both", expand=True, pady=16)

    ctk.CTkLabel(
        text_area,
        text=title.upper(),
        text_color=MUTED,
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w")

    value_label = ctk.CTkLabel(
        text_area,
        text=value,
        text_color=color,
        font=("Segoe UI", 32, "bold")
    )
    value_label.pack(anchor="w")

    ctk.CTkLabel(
        text_area,
        text=subtitle,
        text_color=MUTED,
        font=("Segoe UI", 9)
    ).pack(anchor="w")

    return value_label


lamp_value = status_card(cards, "Status Lampu", "OFF", "Relay lampu meja", RED, "#fff7f7")
mode_value = status_card(cards, "Mode Sistem", "AUTO", "Kontrol otomatis aktif", BLUE, "#eef2ff")
table_value = status_card(cards, "Meja Aktif", "Meja 1", "Billing berjalan", YELLOW, "#fffbea")
timer_value = status_card(cards, "Sisa Waktu", "00:35:20", "Durasi sewa tersisa", TEXT, "#f8fafc")


body = ctk.CTkFrame(main, fg_color="transparent")
body.pack(fill="both", expand=True)

left = ctk.CTkFrame(body, fg_color="transparent")
left.pack(side="left", fill="both", expand=True, padx=(8, 8))

right = ctk.CTkFrame(body, fg_color="transparent")
right.pack(side="left", fill="both", expand=True, padx=(8, 8))


control = ctk.CTkFrame(
    left,
    corner_radius=24,
    fg_color=WHITE,
    border_width=1,
    border_color=BORDER
)
control.pack(fill="both", expand=True)

ctk.CTkLabel(
    control,
    text="Panel Kontrol",
    text_color=TEXT,
    font=("Segoe UI", 18, "bold")
).pack(anchor="w", padx=24, pady=(22, 10))


def control_button(parent, text, color, command):
    button = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        height=48,
        corner_radius=16,
        fg_color=color,
        hover_color=color,
        text_color=WHITE,
        font=("Segoe UI", 11, "bold")
    )
    button.pack(fill="x", padx=24, pady=7)
    return button


connect_button = control_button(control, "CONNECT ARDUINO", BLUE_DARK, connect_arduino)
control_button(control, "AUTO MODE", BLUE, set_auto)
control_button(control, "MANUAL MODE", DARK, set_manual)
control_button(control, "LAMPU ON", GREEN, lamp_on)
control_button(control, "LAMPU OFF", RED, lamp_off)


system_info = ctk.CTkFrame(
    control,
    fg_color="#f8fafc",
    corner_radius=18,
    border_width=1,
    border_color=BORDER
)
system_info.pack(fill="x", padx=24, pady=(16, 0))

ctk.CTkLabel(
    system_info,
    text="Informasi Sistem",
    text_color=TEXT,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w", padx=16, pady=(10, 2))

ctk.CTkLabel(
    system_info,
    text="Serial Port COM3  •  Baudrate 9600  •  Arduino Mega 2560",
    text_color=MUTED,
    font=("Segoe UI", 10)
).pack(anchor="w", padx=16, pady=(0, 10))


connection_card = ctk.CTkFrame(
    control,
    fg_color="#f8fafc",
    corner_radius=18,
    border_width=1,
    border_color=BORDER
)
connection_card.pack(fill="x", padx=24, pady=(12, 0))

ctk.CTkLabel(
    connection_card,
    text="Status Koneksi",
    text_color=TEXT,
    font=("Segoe UI", 12, "bold")
).pack(anchor="w", padx=16, pady=(10, 2))

connection_info = ctk.CTkLabel(
    connection_card,
    text="Arduino Mega      ● Disconnected\n"
         "Billing App       ● Connected\n"
         "Relay Lampu       ● Standby\n"
         "Database          ● Connected",
    text_color=MUTED,
    font=("Segoe UI", 10),
    justify="left"
)
connection_info.pack(anchor="w", padx=16, pady=(0, 10))


status_meja = ctk.CTkFrame(
    right,
    height=400,
    corner_radius=24,
    fg_color=WHITE,
    border_width=1,
    border_color=BORDER
)
status_meja.pack(fill="x", pady=(0, 14))
status_meja.pack_propagate(False)

ctk.CTkLabel(
    status_meja,
    text="Status Meja",
    text_color=TEXT,
    font=("Segoe UI", 17, "bold")
).pack(anchor="w", padx=24, pady=(18, 8))

table_grid = ctk.CTkFrame(status_meja, fg_color="transparent")
table_grid.pack(fill="both", expand=True, padx=24, pady=(0, 14))


def meja_card(parent, name, status, time_text, color, row, col):
    item = ctk.CTkFrame(
        parent,
        height=72,
        corner_radius=18,
        fg_color="#f8fafc",
        border_width=1,
        border_color=BORDER
    )
    item.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)

    ctk.CTkLabel(
        item,
        text=f"● {name}",
        text_color=color,
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w", padx=16, pady=(10, 0))

    ctk.CTkLabel(
        item,
        text=f"{status}",
        text_color=MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=16)

    ctk.CTkLabel(
        item,
        text=f"Sisa: {time_text}",
        text_color=MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=16)


for col in range(2):
    table_grid.grid_columnconfigure(col, weight=1)

for row in range(3):
    table_grid.grid_rowconfigure(row, weight=1)

tables = [
    ("Meja 1", "Aktif", "00:35:20", GREEN),
    ("Meja 2", "Kosong", "-", GRAY),
    ("Meja 3", "Kosong", "-", GRAY),
    ("Meja 4", "Kosong", "-", GRAY),
    ("Meja 5", "Kosong", "-", GRAY),
    ("Meja 6", "Kosong", "-", GRAY),
]

for i, data in enumerate(tables):
    meja_card(table_grid, data[0], data[1], data[2], data[3], i // 2, i % 2)


log = ctk.CTkFrame(
    right,
    corner_radius=24,
    fg_color=WHITE,
    border_width=1,
    border_color=BORDER
)
log.pack(fill="both", expand=True)

ctk.CTkLabel(
    log,
    text="Log Sistem",
    text_color=TEXT,
    font=("Segoe UI", 17, "bold")
).pack(anchor="w", padx=24, pady=(18, 8))

log_box = ctk.CTkTextbox(
    log,
    fg_color="#fbfdff",
    text_color=MUTED,
    font=("Consolas", 11),
    corner_radius=18,
    border_width=1,
    border_color=BORDER
)
log_box.pack(fill="both", expand=True, padx=24, pady=(0, 22))


footer = ctk.CTkLabel(
    main,
    text="Smart Billiard Lighting v1.0  |  Arduino Mega 2560  |  Desktop Dashboard",
    text_color=MUTED,
    font=("Segoe UI", 10)
)
footer.pack(pady=(6, 0))


add_log("Sistem GUI berhasil dijalankan")
add_log("Menunggu koneksi Arduino Mega")
add_log("Dashboard siap digunakan")

update_clock()
app.mainloop()