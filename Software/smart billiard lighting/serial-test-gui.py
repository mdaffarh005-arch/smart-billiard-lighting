import customtkinter as ctk
from datetime import datetime, timedelta
import serial

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Billiard Lighting")
app.geometry("1350x760")
app.configure(fg_color="#f5f7fb")

BLUE = "#4f5dff"
DARK = "#111827"
WHITE = "#ffffff"
TEXT = "#111827"
MUTED = "#8a9a8f"
RED = "#ef4444"
GREEN = "#22c55e"
YELLOW = "#f59e0b"
BORDER = "#e5e7eb"
GRAY = "#f7f7f7"

ser = None
selected_table = None
selected_duration = None
tarif_per_jam = 30000
billing_active = False
end_time = None

table_buttons = []
duration_buttons = []


def add_log(text):
    now = datetime.now().strftime("%H:%M:%S")
    log_box.insert("end", f"[{now}] {text}\n")
    log_box.see("end")


def send_command(cmd):
    global ser
    try:
        if ser and ser.is_open:
            ser.write((cmd + "\n").encode())
            add_log(f"Perintah dikirim: {cmd}")
        else:
            add_log("Arduino belum terhubung")
    except Exception as e:
        add_log(f"Error kirim data: {e}")


def connect_arduino():
    global ser
    try:
        ser = serial.Serial("COM6", 9600, timeout=1)
        arduino_status.configure(text="Arduino\nConnected", text_color=GREEN)
        connect_btn.configure(text="ARDUINO CONNECTED", fg_color=GREEN)
        add_log("Arduino terhubung melalui COM6")
    except Exception as e:
        add_log(f"Gagal konek COM6: {e}")


def show_dashboard():
    billing_frame.pack_forget()
    dashboard_frame.pack(fill="both", expand=True)
    dashboard_menu.configure(fg_color=BLUE, text_color=WHITE)
    billing_menu.configure(fg_color="#f0f0f0", text_color=MUTED)


def show_billing():
    dashboard_frame.pack_forget()
    billing_frame.pack(fill="both", expand=True)
    billing_menu.configure(fg_color=BLUE, text_color=WHITE)
    dashboard_menu.configure(fg_color="#f0f0f0", text_color=MUTED)


def set_mode_auto():
    mode_value.configure(text="AUTO", text_color=BLUE)
    send_command("AUTO")


def set_mode_manual():
    mode_value.configure(text="MANUAL", text_color=YELLOW)
    send_command("MANUAL")


def lamp_on():
    lamp_value.configure(text="ON", text_color=GREEN)
    send_command("ON")


def lamp_off():
    lamp_value.configure(text="OFF", text_color=RED)
    send_command("OFF")


def refresh_table_buttons():
    for btn in table_buttons:
        if btn.cget("text") == selected_table:
            btn.configure(fg_color=BLUE, text_color=WHITE)
        else:
            btn.configure(fg_color=GRAY, text_color=MUTED)


def refresh_duration_buttons():
    for btn in duration_buttons:
        text = btn.cget("text")
        if selected_duration is not None and text == f"{selected_duration} Jam":
            btn.configure(fg_color=BLUE, text_color=WHITE)
        else:
            btn.configure(fg_color=GRAY, text_color=MUTED)


def select_table(table):
    global selected_table
    selected_table = table
    table_value.configure(text=selected_table)
    refresh_table_buttons()
    update_total()
    add_log(f"{table} dipilih")


def select_duration(hour):
    global selected_duration
    selected_duration = hour
    refresh_duration_buttons()
    update_total()
    add_log(f"Durasi {hour} jam dipilih")


def update_total():
    if selected_table is None or selected_duration is None:
        total_tarif_label.configure(
            text="Meja terpilih : -\n"
                 "Durasi       : -\n"
                 "Tarif/Jam    : Rp 30.000\n\n"
                 "Total bayar  : -"
        )
        return

    total = selected_duration * tarif_per_jam
    total_tarif_label.configure(
        text=f"Meja terpilih : {selected_table}\n"
             f"Durasi       : {selected_duration} Jam\n"
             f"Tarif/Jam    : Rp {tarif_per_jam:,}\n\n"
             f"Total bayar  : Rp {total:,}".replace(",", ".")
    )


def start_billing():
    global billing_active, end_time

    if selected_table is None:
        add_log("Pilih meja terlebih dahulu")
        return

    if selected_duration is None:
        add_log("Pilih durasi terlebih dahulu")
        return

    billing_active = True
    end_time = datetime.now() + timedelta(hours=selected_duration)

    table_value.configure(text=selected_table)
    lamp_value.configure(text="ON", text_color=GREEN)
    send_command("ON")

    add_log(f"Billing dimulai untuk {selected_table} selama {selected_duration} jam")
    update_billing_timer()


def stop_billing():
    global billing_active

    billing_active = False
    timer_value.configure(text="00:00:00")
    lamp_value.configure(text="OFF", text_color=RED)
    send_command("OFF")

    billing_active_label.configure(
        text="Meja Aktif : -\n"
             "Status     : Selesai\n"
             "Sisa Waktu : 00:00:00\n"
             "Lampu      : OFF"
    )

    add_log("Billing selesai, lampu dimatikan")


def add_time():
    global end_time

    if billing_active and end_time:
        end_time += timedelta(hours=1)
        add_log("Waktu billing ditambah 1 jam")
    else:
        add_log("Tidak ada billing aktif")


def update_billing_timer():
    global billing_active

    if billing_active and end_time:
        remaining = end_time - datetime.now()

        if remaining.total_seconds() <= 0:
            stop_billing()
            return

        total_seconds = int(remaining.total_seconds())
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60

        time_text = f"{h:02d}:{m:02d}:{s:02d}"
        timer_value.configure(text=time_text)

        billing_active_label.configure(
            text=f"Meja Aktif : {selected_table}\n"
                 f"Status     : Berjalan\n"
                 f"Durasi     : {selected_duration} Jam\n"
                 f"Sisa Waktu : {time_text}\n"
                 f"Lampu      : ON"
        )

        app.after(1000, update_billing_timer)


def update_clock():
    clock_label.configure(text=datetime.now().strftime("%d/%m/%y\n%H:%M:%S"))
    app.after(1000, update_clock)


sidebar = ctk.CTkFrame(app, width=155, fg_color=WHITE, corner_radius=0)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

ctk.CTkLabel(
    sidebar,
    text="SBL",
    text_color=BLUE,
    font=("Segoe UI", 34, "bold")
).pack(pady=(35, 0))

ctk.CTkLabel(
    sidebar,
    text="Smart Billiard\nLighting",
    text_color=TEXT,
    font=("Segoe UI", 10, "bold"),
    justify="center"
).pack(pady=(0, 35))

dashboard_menu = ctk.CTkButton(
    sidebar,
    text="Dashboard",
    command=show_dashboard,
    height=26,
    corner_radius=8,
    fg_color=BLUE,
    text_color=WHITE,
    font=("Segoe UI", 10, "bold")
)
dashboard_menu.pack(fill="x", padx=18, pady=5)

billing_menu = ctk.CTkButton(
    sidebar,
    text="Billing",
    command=show_billing,
    height=26,
    corner_radius=8,
    fg_color="#f0f0f0",
    text_color=MUTED,
    font=("Segoe UI", 10, "bold")
)
billing_menu.pack(fill="x", padx=18, pady=5)


main = ctk.CTkFrame(app, fg_color="#f5f7fb", corner_radius=0)
main.pack(side="left", fill="both", expand=True, padx=28, pady=28)

header = ctk.CTkFrame(main, fg_color="transparent")
header.pack(fill="x")

ctk.CTkLabel(
    header,
    text="Smart Billiard Lighting",
    text_color=TEXT,
    font=("Segoe UI", 30, "bold")
).pack(side="left")

status_area = ctk.CTkFrame(header, fg_color="transparent")
status_area.pack(side="right")

arduino_status = ctk.CTkLabel(
    status_area,
    text="Arduino\nDisconnected",
    width=135,
    height=54,
    corner_radius=16,
    fg_color=WHITE,
    text_color=RED,
    font=("Segoe UI", 10, "bold")
)
arduino_status.pack(side="left", padx=8)

ctk.CTkLabel(
    status_area,
    text="Billing\nConnected",
    width=135,
    height=54,
    corner_radius=16,
    fg_color=WHITE,
    text_color=GREEN,
    font=("Segoe UI", 10, "bold")
).pack(side="left", padx=8)

clock_label = ctk.CTkLabel(
    status_area,
    text="",
    width=135,
    height=54,
    corner_radius=16,
    fg_color=WHITE,
    text_color=TEXT,
    font=("Segoe UI", 10, "bold")
)
clock_label.pack(side="left", padx=8)


def hero(parent, title):
    frame = ctk.CTkFrame(parent, fg_color=BLUE, height=78, corner_radius=18)
    frame.pack(fill="x", pady=(20, 16))
    frame.pack_propagate(False)

    ctk.CTkLabel(
        frame,
        text=title,
        text_color=WHITE,
        font=("Segoe UI", 28, "bold")
    ).pack(anchor="w", padx=24, pady=18)


def card(parent, title, value, color):
    box = ctk.CTkFrame(
        parent,
        height=82,
        fg_color=WHITE,
        corner_radius=16,
        border_width=1,
        border_color=BORDER
    )
    box.pack(side="left", fill="both", expand=True, padx=8)
    box.pack_propagate(False)

    ctk.CTkFrame(box, width=6, height=48, fg_color=color, corner_radius=6).pack(
        side="left", padx=(16, 10), pady=17
    )

    inner = ctk.CTkFrame(box, fg_color="transparent")
    inner.pack(side="left", fill="both", expand=True)

    ctk.CTkLabel(
        inner,
        text=title,
        text_color=MUTED,
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w", pady=(14, 0))

    lbl = ctk.CTkLabel(
        inner,
        text=value,
        text_color=color,
        font=("Segoe UI", 25, "bold")
    )
    lbl.pack(anchor="w")

    return lbl


dashboard_frame = ctk.CTkFrame(main, fg_color="#f5f7fb")
dashboard_frame.pack(fill="both", expand=True)

hero(dashboard_frame, "LIGHTING CONTROL CENTER")

status_cards = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
status_cards.pack(fill="x", pady=(0, 14))

lamp_value = card(status_cards, "STATUS LAMPU", "OFF", RED)
mode_value = card(status_cards, "MODE SISTEM", "AUTO", BLUE)
table_value = card(status_cards, "NOMOR MEJA", "-", YELLOW)
timer_value = card(status_cards, "SISA WAKTU", "00:00:00", DARK)

dash_body = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
dash_body.pack(fill="both", expand=True)

left_dash = ctk.CTkFrame(dash_body, fg_color=WHITE, corner_radius=18)
left_dash.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=8)

right_dash = ctk.CTkFrame(dash_body, fg_color="transparent")
right_dash.pack(side="right", fill="both", expand=True, padx=(8, 0), pady=8)

ctk.CTkLabel(
    left_dash,
    text="Panel Kontrol",
    text_color=TEXT,
    font=("Segoe UI", 14, "bold")
).pack(anchor="w", padx=28, pady=(22, 12))


def control_button(text, color, command):
    ctk.CTkButton(
        left_dash,
        text=text,
        command=command,
        height=45,
        corner_radius=14,
        fg_color=color,
        hover_color=color,
        text_color=WHITE,
        font=("Segoe UI", 11, "bold")
    ).pack(fill="x", padx=28, pady=8)


connect_btn = ctk.CTkButton(
    left_dash,
    text="CONNECT ARDUINO",
    command=connect_arduino,
    height=45,
    corner_radius=14,
    fg_color=DARK,
    hover_color=DARK,
    text_color=WHITE,
    font=("Segoe UI", 11, "bold")
)
connect_btn.pack(fill="x", padx=28, pady=8)

control_button("AUTO MODE", BLUE, set_mode_auto)
control_button("MANUAL MODE", BLUE, set_mode_manual)
control_button("LAMPU ON", GREEN, lamp_on)
control_button("LAMPU OFF", RED, lamp_off)

status_meja = ctk.CTkFrame(right_dash, fg_color=WHITE, corner_radius=18)
status_meja.pack(fill="x", pady=(0, 10))

ctk.CTkLabel(
    status_meja,
    text="Status Meja",
    text_color=TEXT,
    font=("Segoe UI", 14, "bold")
).pack(anchor="w", padx=18, pady=(14, 8))

grid = ctk.CTkFrame(status_meja, fg_color="transparent")
grid.pack(fill="x", padx=18, pady=(0, 16))

for i in range(4):
    meja = ctk.CTkFrame(
        grid,
        width=170,
        height=70,
        fg_color="#f7f7f7",
        corner_radius=12,
        border_width=1,
        border_color="#d7d7d7"
    )
    meja.grid(row=i // 2, column=i % 2, padx=12, pady=8)
    meja.pack_propagate(False)

    ctk.CTkLabel(
        meja,
        text=f"Meja {i+1}\nAktif\nsisa: -",
        text_color=MUTED,
        font=("Segoe UI", 9),
        justify="left"
    ).pack(anchor="w", padx=14, pady=10)

log_frame = ctk.CTkFrame(right_dash, fg_color=WHITE, corner_radius=18)
log_frame.pack(fill="both", expand=True)

ctk.CTkLabel(
    log_frame,
    text="Log Sistem",
    text_color=TEXT,
    font=("Segoe UI", 14, "bold")
).pack(anchor="w", padx=18, pady=(14, 8))

log_box = ctk.CTkTextbox(
    log_frame,
    fg_color="#f7f7f7",
    text_color=MUTED,
    font=("Consolas", 10),
    corner_radius=12,
    border_width=1,
    border_color="#d7d7d7"
)
log_box.pack(fill="both", expand=True, padx=18, pady=(0, 18))


billing_frame = ctk.CTkFrame(main, fg_color="#f5f7fb")

hero(billing_frame, "BILLING CONTROL CENTER")

billing_body = ctk.CTkFrame(billing_frame, fg_color="transparent")
billing_body.pack(fill="both", expand=True)

left_bill = ctk.CTkFrame(billing_body, fg_color="transparent")
left_bill.pack(side="left", fill="both", expand=True, padx=(0, 12))

right_bill = ctk.CTkFrame(billing_body, fg_color="transparent")
right_bill.pack(side="right", fill="both", expand=True, padx=(12, 0))


def panel(parent, title):
    box = ctk.CTkFrame(parent, fg_color=WHITE, corner_radius=18)
    box.pack(fill="both", expand=True, pady=10)
    ctk.CTkLabel(
        box,
        text=title,
        text_color=TEXT,
        font=("Segoe UI", 14, "bold")
    ).pack(anchor="w", padx=18, pady=(14, 8))
    return box


pilih_meja_panel = panel(left_bill, "Pilih Meja")
durasi_panel = panel(left_bill, "Pilih Durasi")
total_panel = panel(right_bill, "Total Tarif")
aktif_panel = panel(right_bill, "Billing Aktif")

meja_grid = ctk.CTkFrame(pilih_meja_panel, fg_color="transparent")
meja_grid.pack(padx=18, pady=8)

for i in range(4):
    btn = ctk.CTkButton(
        meja_grid,
        text=f"Meja {i + 1}",
        command=lambda n=i + 1: select_table(f"Meja {n}"),
        width=180,
        height=58,
        fg_color=GRAY,
        text_color=MUTED,
        corner_radius=12,
        border_width=1,
        border_color="#d7d7d7",
        hover_color=BLUE,
        font=("Segoe UI", 11, "bold")
    )
    btn.grid(row=i // 2, column=i % 2, padx=16, pady=8)
    table_buttons.append(btn)

durasi_grid = ctk.CTkFrame(durasi_panel, fg_color="transparent")
durasi_grid.pack(padx=18, pady=8)

labels = ["1 Jam", "2 Jam", "3 Jam", "CUSTOM"]
values = [1, 2, 3, None]

for i, label in enumerate(labels):
    btn = ctk.CTkButton(
        durasi_grid,
        text=label,
        command=lambda v=values[i]: select_duration(v if v is not None else 1),
        width=180,
        height=58,
        fg_color=GRAY,
        text_color=MUTED,
        corner_radius=12,
        border_width=1,
        border_color="#d7d7d7",
        hover_color=BLUE,
        font=("Segoe UI", 11, "bold")
    )
    btn.grid(row=i // 2, column=i % 2, padx=16, pady=8)
    duration_buttons.append(btn)

total_tarif_label = ctk.CTkLabel(
    total_panel,
    text="",
    text_color=TEXT,
    font=("Segoe UI", 11),
    justify="left",
    anchor="w"
)
total_tarif_label.pack(fill="x", padx=24, pady=(0, 10))

btns = ctk.CTkFrame(total_panel, fg_color="transparent")
btns.pack(fill="x", padx=20, pady=8)

ctk.CTkButton(
    btns,
    text="Mulai",
    command=start_billing,
    fg_color=GREEN,
    height=32
).pack(side="left", expand=True, fill="x", padx=5)

ctk.CTkButton(
    btns,
    text="Tambah",
    command=add_time,
    fg_color=BLUE,
    height=32
).pack(side="left", expand=True, fill="x", padx=5)

ctk.CTkButton(
    btns,
    text="Selesai",
    command=stop_billing,
    fg_color=RED,
    height=32
).pack(side="left", expand=True, fill="x", padx=5)

billing_active_label = ctk.CTkLabel(
    aktif_panel,
    text="Belum ada billing aktif",
    text_color=MUTED,
    font=("Consolas", 11),
    justify="left",
    anchor="nw"
)
billing_active_label.pack(fill="both", expand=True, padx=24, pady=10)

update_total()
add_log("Dashboard siap digunakan")
update_clock()
app.mainloop()