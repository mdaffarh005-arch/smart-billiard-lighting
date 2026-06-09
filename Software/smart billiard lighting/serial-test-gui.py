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
GRAY = "#f7f7f7"
BORDER = "#e5e7eb"

ser = None

selected_table = None
selected_duration = None
selected_status_table = None

current_mode = "AUTO"
manual_lamp_states = {
    "Meja 1": "OFF",
    "Meja 2": "OFF",
    "Meja 3": "OFF",
    "Meja 4": "OFF",
}

tarif_per_jam = 30000
end_time = None

table_buttons = []
duration_buttons = []
status_meja_buttons = {}
active_sessions = {}


def add_log(text):
    now = datetime.now().strftime("%H:%M:%S")
    log_box.insert("end", f"[{now}] {text}\n")
    log_box.see("end")


def get_table_number(table):
    if table is None:
        return None
    return table.replace("Meja ", "")


def send_command(cmd):
    global ser

    try:
        if ser is None or not ser.is_open:
            add_log("Arduino belum terhubung")
            return

        ser.write((cmd + "\n").encode("utf-8"))
        ser.flush()
        add_log(f"Perintah dikirim: {cmd}")

    except serial.SerialTimeoutException:
        add_log("Serial timeout, perintah gagal dikirim")

    except Exception as e:
        add_log(f"Error kirim data: {e}")


def send_lamp_command(table, state):
    table_number = get_table_number(table)

    if table_number is None:
        add_log("Meja belum dipilih")
        return

    send_command(f"{state}:{table_number}")


def connect_arduino():
    global ser

    try:
        ser = serial.Serial(
            port="COM6",
            baudrate=9600,
            timeout=1,
            write_timeout=1
        )

        arduino_status.configure(text="Arduino\nConnected", text_color=GREEN)
        connect_btn.configure(text="ARDUINO CONNECTED", fg_color=GREEN)
        add_log("Arduino terhubung melalui COM6")

    except Exception as e:
        ser = None
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


def update_lamp_status(state):
    if state == "ON":
        lamp_value.configure(text="ON", text_color=GREEN)
        lamp_bar.configure(fg_color=GREEN)
    else:
        lamp_value.configure(text="OFF", text_color=RED)
        lamp_bar.configure(fg_color=RED)


def update_mode_status(mode):
    if mode == "AUTO":
        mode_value.configure(text="AUTO", text_color=BLUE)
        mode_bar.configure(fg_color=BLUE)
    else:
        mode_value.configure(text="MANUAL", text_color=YELLOW)
        mode_bar.configure(fg_color=YELLOW)


def update_selected_lamp_view():
    if selected_status_table is None:
        update_lamp_status("OFF")
        return

    if current_mode == "AUTO":
        if selected_status_table in active_sessions:
            update_lamp_status("ON")
        else:
            update_lamp_status("OFF")
    else:
        update_lamp_status(manual_lamp_states.get(selected_status_table, "OFF"))


def set_mode_auto():
    global current_mode

    current_mode = "AUTO"
    update_mode_status("AUTO")
    update_selected_lamp_view()
    send_command("AUTO")
    add_log("Mode AUTO aktif")


def set_mode_manual():
    global current_mode

    current_mode = "MANUAL"
    update_mode_status("MANUAL")
    update_selected_lamp_view()
    send_command("MANUAL")
    add_log("Mode MANUAL aktif")


def lamp_on():
    if current_mode == "AUTO":
        add_log("Mode AUTO aktif, ubah ke MANUAL untuk kontrol lampu manual")
        return

    if selected_status_table is None:
        add_log("Pilih meja terlebih dahulu pada Status Meja")
        return

    manual_lamp_states[selected_status_table] = "ON"
    update_lamp_status("ON")
    refresh_status_meja()
    send_lamp_command(selected_status_table, "ON")
    add_log(f"Lampu {selected_status_table} dinyalakan manual")


def lamp_off():
    if current_mode == "AUTO":
        add_log("Mode AUTO aktif, ubah ke MANUAL untuk kontrol lampu manual")
        return

    if selected_status_table is None:
        add_log("Pilih meja terlebih dahulu pada Status Meja")
        return

    manual_lamp_states[selected_status_table] = "OFF"
    update_lamp_status("OFF")
    refresh_status_meja()
    send_lamp_command(selected_status_table, "OFF")
    add_log(f"Lampu {selected_status_table} dimatikan manual")


def refresh_table_buttons():
    for btn in table_buttons:
        if btn.cget("text") == selected_table:
            btn.configure(fg_color=BLUE, text_color=WHITE)
        else:
            btn.configure(fg_color=GRAY, text_color=MUTED)


def refresh_duration_buttons():
    for btn in duration_buttons:
        text = btn.cget("text")

        if selected_duration == 1 and text == "1 Jam":
            btn.configure(fg_color=BLUE, text_color=WHITE)
        elif selected_duration == 2 and text == "2 Jam":
            btn.configure(fg_color=BLUE, text_color=WHITE)
        elif selected_duration == 3 and text == "3 Jam":
            btn.configure(fg_color=BLUE, text_color=WHITE)
        elif selected_duration not in [None, 1, 2, 3] and text == "CUSTOM":
            btn.configure(fg_color=BLUE, text_color=WHITE)
        else:
            btn.configure(fg_color=GRAY, text_color=MUTED)


def select_table(table):
    global selected_table

    selected_table = table
    refresh_table_buttons()
    update_total()
    add_log(f"{table} dipilih")


def select_duration(hour):
    global selected_duration

    selected_duration = hour
    refresh_duration_buttons()
    update_total()
    add_log(f"Durasi {format_duration(hour)} dipilih")


def open_custom_duration():
    popup = ctk.CTkToplevel(app)
    popup.title("Set Durasi")
    popup.geometry("360x430")
    popup.configure(fg_color="#f5f7fb")
    popup.grab_set()

    jam_var = ctk.IntVar(value=1)
    menit_var = ctk.IntVar(value=0)

    def format_angka(n):
        return f"{n:02d}"

    def update_display():
        jam_prev.configure(text=format_angka((jam_var.get() - 1) % 24))
        jam_now.configure(text=format_angka(jam_var.get()))
        jam_next.configure(text=format_angka((jam_var.get() + 1) % 24))

        menit_prev.configure(text=format_angka((menit_var.get() - 1) % 60))
        menit_now.configure(text=format_angka(menit_var.get()))
        menit_next.configure(text=format_angka((menit_var.get() + 1) % 60))

    def jam_up(event=None):
        jam_var.set((jam_var.get() + 1) % 24)
        update_display()

    def jam_down(event=None):
        jam_var.set((jam_var.get() - 1) % 24)
        update_display()

    def menit_up(event=None):
        menit_var.set((menit_var.get() + 1) % 60)
        update_display()

    def menit_down(event=None):
        menit_var.set((menit_var.get() - 1) % 60)
        update_display()

    def simpan():
        global selected_duration

        jam = jam_var.get()
        menit = menit_var.get()

        if jam == 0 and menit == 0:
            add_log("Durasi tidak boleh 00:00")
            return

        selected_duration = jam + (menit / 60)

        refresh_duration_buttons()
        update_total()
        add_log(f"Custom durasi dipilih: {jam} jam {menit} menit")
        popup.destroy()

    card_popup = ctk.CTkFrame(popup, fg_color=WHITE, corner_radius=22)
    card_popup.pack(fill="both", expand=True, padx=22, pady=22)

    ctk.CTkLabel(
        card_popup,
        text="SET DURASI",
        text_color=TEXT,
        font=("Segoe UI", 13, "bold")
    ).pack(pady=(28, 12))

    picker = ctk.CTkFrame(card_popup, fg_color="transparent")
    picker.pack(pady=8)

    jam_col = ctk.CTkFrame(picker, fg_color="transparent")
    jam_col.grid(row=0, column=0, padx=(0, 8))

    colon_col = ctk.CTkFrame(picker, fg_color="transparent")
    colon_col.grid(row=0, column=1, padx=4)

    menit_col = ctk.CTkFrame(picker, fg_color="transparent")
    menit_col.grid(row=0, column=2, padx=(8, 0))

    jam_prev = ctk.CTkLabel(jam_col, text="00", text_color="#cfd6d1", font=("Segoe UI", 42, "bold"))
    jam_prev.pack()

    jam_now = ctk.CTkLabel(jam_col, text="01", text_color="#95a297", font=("Segoe UI", 54, "bold"))
    jam_now.pack()

    jam_next = ctk.CTkLabel(jam_col, text="02", text_color="#cfd6d1", font=("Segoe UI", 42, "bold"))
    jam_next.pack()

    ctk.CTkLabel(
        colon_col,
        text=":\n:\n:",
        text_color="#95a297",
        font=("Segoe UI", 48, "bold")
    ).pack(pady=(10, 0))

    menit_prev = ctk.CTkLabel(menit_col, text="59", text_color="#cfd6d1", font=("Segoe UI", 42, "bold"))
    menit_prev.pack()

    menit_now = ctk.CTkLabel(menit_col, text="00", text_color="#95a297", font=("Segoe UI", 54, "bold"))
    menit_now.pack()

    menit_next = ctk.CTkLabel(menit_col, text="01", text_color="#cfd6d1", font=("Segoe UI", 42, "bold"))
    menit_next.pack()

    for widget in [jam_prev, jam_now, jam_next]:
        widget.bind("<Button-1>", jam_up)
        widget.bind("<MouseWheel>", lambda e: jam_up() if e.delta > 0 else jam_down())

    for widget in [menit_prev, menit_now, menit_next]:
        widget.bind("<Button-1>", menit_up)
        widget.bind("<MouseWheel>", lambda e: menit_up() if e.delta > 0 else menit_down())

    ctk.CTkButton(
        card_popup,
        text="Simpan",
        command=simpan,
        width=210,
        height=48,
        fg_color=BLUE,
        hover_color=BLUE,
        corner_radius=14,
        font=("Segoe UI", 13, "bold")
    ).pack(pady=(18, 24))

    update_display()


def format_duration(duration):
    if duration is None:
        return "-"

    total_minutes = int(duration * 60)
    jam = total_minutes // 60
    menit = total_minutes % 60

    if menit == 0:
        return f"{jam} Jam"

    return f"{jam} Jam {menit} Menit"


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
             f"Durasi       : {format_duration(selected_duration)}\n"
             f"Tarif/Jam    : Rp {tarif_per_jam:,}\n\n"
             f"Total bayar  : Rp {int(total):,}".replace(",", ".")
    )


def get_sisa_waktu(table):
    if table not in active_sessions:
        return "-"

    remaining = active_sessions[table]["end_time"] - datetime.now()

    if remaining.total_seconds() <= 0:
        return "00:00:00"

    total_seconds = int(remaining.total_seconds())
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60

    return f"{h:02d}:{m:02d}:{s:02d}"


def update_billing_active_label():
    if not active_sessions:
        billing_active_label.configure(text="Belum ada billing aktif", text_color=MUTED)
        return

    text = ""

    for table, data in active_sessions.items():
        lamp_status = "ON" if table in active_sessions else manual_lamp_states.get(table, "OFF")

        text += (
            f"{table}\n"
            f"Status     : Berjalan\n"
            f"Durasi     : {format_duration(data['duration'])}\n"
            f"Sisa Waktu : {get_sisa_waktu(table)}\n"
            f"Lampu      : {lamp_status}\n"
            f"----------------------\n"
        )

    billing_active_label.configure(text=text, text_color=TEXT)


def select_status_meja(table):
    global selected_status_table

    selected_status_table = table
    table_value.configure(text=table)

    if table in active_sessions:
        timer_value.configure(text=get_sisa_waktu(table))
    else:
        timer_value.configure(text="00:00:00")

    update_selected_lamp_view()
    refresh_status_meja()


def refresh_status_meja():
    for i in range(1, 5):
        table = f"Meja {i}"
        btn = status_meja_buttons[table]

        if table in active_sessions:
            sisa = get_sisa_waktu(table)
            if current_mode == "AUTO":
                lamp_text = "Lampu: ON"
            else:
                lamp_text = f"Lampu: {manual_lamp_states.get(table, 'OFF')}"
            text = f"{table}\nAktif\nsisa: {sisa}\n{lamp_text}"
            fg = "#eefdf3"
            tc = GREEN
        else:
            if current_mode == "MANUAL":
                lamp_text = f"Lampu: {manual_lamp_states.get(table, 'OFF')}"
            else:
                lamp_text = "Lampu: OFF"
            text = f"{table}\nKosong\nsisa: -\n{lamp_text}"
            fg = GRAY
            tc = MUTED

        if selected_status_table == table:
            fg = BLUE
            tc = WHITE

        btn.configure(text=text, fg_color=fg, text_color=tc)


def update_status_timer():
    expired_tables = []

    for table in list(active_sessions.keys()):
        if get_sisa_waktu(table) == "00:00:00":
            expired_tables.append(table)

    for table in expired_tables:
        del active_sessions[table]
        add_log(f"{table} selesai")

        if current_mode == "AUTO":
            send_lamp_command(table, "OFF")

        if selected_status_table == table:
            timer_value.configure(text="00:00:00")

    if selected_status_table:
        if selected_status_table in active_sessions:
            timer_value.configure(text=get_sisa_waktu(selected_status_table))
        else:
            timer_value.configure(text="00:00:00")

    update_selected_lamp_view()
    refresh_status_meja()
    update_billing_active_label()
    app.after(1000, update_status_timer)


def start_billing():
    global end_time, selected_status_table

    if selected_table is None:
        add_log("Pilih meja terlebih dahulu")
        return

    if selected_duration is None:
        add_log("Pilih durasi terlebih dahulu")
        return

    end_time = datetime.now() + timedelta(hours=selected_duration)

    active_sessions[selected_table] = {
        "duration": selected_duration,
        "end_time": end_time,
        "lamp": "ON"
    }

    selected_status_table = selected_table

    table_value.configure(text=selected_table)
    timer_value.configure(text=get_sisa_waktu(selected_table))

    if current_mode == "AUTO":
        update_lamp_status("ON")
        send_lamp_command(selected_table, "ON")
    else:
        manual_lamp_states[selected_table] = "ON"
        update_lamp_status("ON")
        send_lamp_command(selected_table, "ON")

    refresh_status_meja()
    update_billing_active_label()
    add_log(f"Billing dimulai untuk {selected_table} selama {format_duration(selected_duration)}")


def stop_billing():
    if selected_status_table is None:
        add_log("Pilih meja terlebih dahulu pada Status Meja")
        return

    if selected_status_table in active_sessions:
        del active_sessions[selected_status_table]
        add_log(f"Billing {selected_status_table} dihentikan")
    else:
        add_log("Tidak ada billing aktif pada meja yang dipilih")

    timer_value.configure(text="00:00:00")

    if current_mode == "AUTO":
        send_lamp_command(selected_status_table, "OFF")
        update_lamp_status("OFF")
    else:
        manual_lamp_states[selected_status_table] = "OFF"
        send_lamp_command(selected_status_table, "OFF")
        update_lamp_status("OFF")

    refresh_status_meja()
    update_billing_active_label()


def add_time():
    if selected_status_table in active_sessions:
        active_sessions[selected_status_table]["end_time"] += timedelta(hours=1)
        active_sessions[selected_status_table]["duration"] += 1
        update_billing_active_label()
        refresh_status_meja()
        add_log(f"Waktu {selected_status_table} ditambah 1 jam")
    else:
        add_log("Tidak ada billing aktif")


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

    bar = ctk.CTkFrame(box, width=6, height=48, fg_color=color, corner_radius=6)
    bar.pack(side="left", padx=(16, 10), pady=17)

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

    return lbl, bar


dashboard_frame = ctk.CTkFrame(main, fg_color="#f5f7fb")
dashboard_frame.pack(fill="both", expand=True)

hero(dashboard_frame, "LIGHTING CONTROL CENTER")

status_cards = ctk.CTkFrame(dashboard_frame, fg_color="transparent")
status_cards.pack(fill="x", pady=(0, 14))

lamp_value, lamp_bar = card(status_cards, "STATUS LAMPU", "OFF", RED)
mode_value, mode_bar = card(status_cards, "MODE SISTEM", "AUTO", BLUE)
table_value, table_bar = card(status_cards, "NOMOR MEJA", "-", YELLOW)
timer_value, timer_bar = card(status_cards, "SISA WAKTU", "00:00:00", DARK)

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
    table_name = f"Meja {i + 1}"

    btn = ctk.CTkButton(
        grid,
        text=f"{table_name}\nKosong\nsisa: -\nLampu: OFF",
        command=lambda t=table_name: select_status_meja(t),
        width=170,
        height=76,
        fg_color=GRAY,
        text_color=MUTED,
        corner_radius=12,
        border_width=1,
        border_color="#d7d7d7",
        hover_color="#e8ecff",
        font=("Segoe UI", 9),
        anchor="w"
    )
    btn._text_label.configure(justify="left", anchor="w")
    btn.grid(row=i // 2, column=i % 2, padx=12, pady=8)
    status_meja_buttons[table_name] = btn

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
    command = open_custom_duration if label == "CUSTOM" else lambda v=values[i]: select_duration(v)

    btn = ctk.CTkButton(
        durasi_grid,
        text=label,
        command=command,
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
refresh_status_meja()
update_billing_active_label()
update_status_timer()
app.mainloop()
