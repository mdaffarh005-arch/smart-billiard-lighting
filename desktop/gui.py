import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title("Smart Billiard Lighting")
root.geometry("1100x650")
root.configure(bg="#0f1117")


# =========================
# COLOR
# =========================
BG = "#0f1117"
SIDEBAR = "#111827"
CARD = "#1f2937"
CARD2 = "#172033"
TEXT = "#f9fafb"
MUTED = "#9ca3af"
BLUE = "#5865f2"
GREEN = "#22c55e"
YELLOW = "#facc15"
RED = "#ef4444"


# =========================
# SIDEBAR
# =========================
sidebar = tk.Frame(root, bg=SIDEBAR, width=230)
sidebar.pack(side="left", fill="y")

title = tk.Label(
    sidebar,
    text="🎱 Smart\nBilliard",
    bg=SIDEBAR,
    fg=TEXT,
    font=("Segoe UI", 22, "bold"),
    justify="left"
)
title.pack(pady=30, padx=20, anchor="w")

menus = [
    "🏠 Dashboard",
    "💡 Kontrol Lampu",
    "📊 Monitoring",
    "🧾 Billing",
    "⚙ Settings"
]

for menu in menus:
    color = BLUE if "Dashboard" in menu else SIDEBAR
    item = tk.Label(
        sidebar,
        text=menu,
        bg=color,
        fg=TEXT,
        font=("Segoe UI", 12, "bold"),
        padx=15,
        pady=12,
        anchor="w"
    )
    item.pack(fill="x", padx=15, pady=5)


# =========================
# MAIN AREA
# =========================
main = tk.Frame(root, bg=BG)
main.pack(side="left", fill="both", expand=True)

header = tk.Frame(main, bg=BG, height=80)
header.pack(fill="x")

tk.Label(
    header,
    text="Smart Billiard Lighting",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 26, "bold")
).pack(side="left", padx=30, pady=20)

tk.Label(
    header,
    text="Status: Online",
    bg=BG,
    fg=GREEN,
    font=("Segoe UI", 12, "bold")
).pack(side="right", padx=30)


# =========================
# HERO CARD
# =========================
hero = tk.Frame(main, bg=BLUE, height=160)
hero.pack(fill="x", padx=30, pady=10)

tk.Label(
    hero,
    text="Dashboard Kontrol Lampu Meja Billiard",
    bg=BLUE,
    fg="white",
    font=("Segoe UI", 22, "bold")
).pack(anchor="w", padx=25, pady=(25, 5))

tk.Label(
    hero,
    text="Sistem monitoring dan pengaturan lampu otomatis berbasis IoT",
    bg=BLUE,
    fg="white",
    font=("Segoe UI", 12)
).pack(anchor="w", padx=25)


# =========================
# CARD CONTAINER
# =========================
cards = tk.Frame(main, bg=BG)
cards.pack(fill="x", padx=30, pady=15)


def create_card(parent, title, value, status_color):
    frame = tk.Frame(parent, bg=CARD, width=250, height=130)
    frame.pack(side="left", padx=10, fill="both", expand=True)
    frame.pack_propagate(False)

    tk.Label(
        frame,
        text=title,
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 11, "bold")
    ).pack(anchor="w", padx=20, pady=(18, 5))

    tk.Label(
        frame,
        text=value,
        bg=CARD,
        fg=status_color,
        font=("Segoe UI", 24, "bold")
    ).pack(anchor="w", padx=20)

    return frame


create_card(cards, "Status Lampu", "ON", GREEN)
create_card(cards, "Mode Sistem", "AUTO", BLUE)
create_card(cards, "Meja Aktif", "Meja 1", YELLOW)
create_card(cards, "Sisa Waktu", "00:35:20", TEXT)


# =========================
# CONTROL PANEL
# =========================
content = tk.Frame(main, bg=BG)
content.pack(fill="both", expand=True, padx=30, pady=10)

control = tk.Frame(content, bg=CARD, width=420)
control.pack(side="left", fill="both", expand=True, padx=(0, 10))

tk.Label(
    control,
    text="Panel Kontrol",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 18, "bold")
).pack(anchor="w", padx=20, pady=20)

button_frame = tk.Frame(control, bg=CARD)
button_frame.pack(padx=20, pady=10, fill="x")

buttons = [
    ("AUTO MODE", BLUE),
    ("MANUAL MODE", CARD2),
    ("LAMPU ON", GREEN),
    ("LAMPU OFF", RED)
]

for text, color in buttons:
    btn = tk.Button(
        button_frame,
        text=text,
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        height=2
    )
    btn.pack(fill="x", pady=7)


# =========================
# LOG PANEL
# =========================
log_panel = tk.Frame(content, bg=CARD, width=420)
log_panel.pack(side="left", fill="both", expand=True, padx=(10, 0))

tk.Label(
    log_panel,
    text="Log Aktivitas",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 18, "bold")
).pack(anchor="w", padx=20, pady=20)

logs = [
    "✅ Sistem berhasil terhubung",
    "💡 Lampu meja 1 menyala",
    "⏱ Billing aktif selama 60 menit",
    "📡 Data dikirim ke mikrokontroler",
    "🔒 Mode otomatis aktif"
]

for log in logs:
    tk.Label(
        log_panel,
        text=log,
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 11),
        anchor="w"
    ).pack(fill="x", padx=20, pady=6)


# =========================
# FOOTER
# =========================
footer = tk.Label(
    main,
    text="UI/UX Design by Muhammad Abdi Muhyi Umam",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 10)
)
footer.pack(side="bottom", pady=10)


root.mainloop()