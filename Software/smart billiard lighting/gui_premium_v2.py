# gui_premium_v3.py
# Smart Billiard Lighting — Premium Dark UI
import sys, time, serial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

RATE_PER_HOUR = 35000
RFC2217_URL = "rfc2217://localhost:4000"

DARK_BG      = "#0D1117"
CARD_BG      = "#161B22"
CARD_HOVER   = "#1C2330"
BORDER       = "#30363D"
ACCENT_GREEN = "#3FB950"
ACCENT_DIM   = "#1A4A2A"
TEXT_PRIMARY = "#E6EDF3"
TEXT_SEC     = "#8B949E"
TEXT_MUTED   = "#484F58"
RED          = "#F85149"
AMBER        = "#D29922"
SIDEBAR_BG   = "#090D13"
SIDEBAR_SEL  = "#161B22"

QSS = f"""
QMainWindow, QWidget {{
    background: {DARK_BG};
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
    font-size: 13px;
}}

/* ── Sidebar ── */
#sidebar {{
    background: {SIDEBAR_BG};
    border-right: 1px solid {BORDER};
}}
#logo {{
    color: {ACCENT_GREEN};
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 28px 20px 8px;
}}
#logo_sub {{
    color: {TEXT_MUTED};
    font-size: 10px;
    letter-spacing: 3px;
    padding: 0 22px 24px;
}}

/* ── Nav buttons ── */
QPushButton#nav {{
    background: transparent;
    color: {TEXT_SEC};
    border: none;
    border-radius: 8px;
    text-align: left;
    padding: 10px 16px;
    font-size: 13px;
    font-weight: 500;
    margin: 1px 8px;
}}
QPushButton#nav:hover {{
    background: {SIDEBAR_SEL};
    color: {TEXT_PRIMARY};
}}
QPushButton#nav[active=true] {{
    background: {ACCENT_DIM};
    color: {ACCENT_GREEN};
    font-weight: 600;
}}

/* ── Cards ── */
QFrame#card {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}

/* ── Labels ── */
QLabel#h1 {{
    font-size: 26px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    letter-spacing: -0.5px;
}}
QLabel#h2 {{
    font-size: 18px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}
QLabel#muted {{
    font-size: 11px;
    color: {TEXT_MUTED};
    letter-spacing: 1.5px;
    text-transform: uppercase;
}}
QLabel#revenue_val {{
    font-size: 36px;
    font-weight: 700;
    color: {ACCENT_GREEN};
    letter-spacing: -1px;
}}
QLabel#stat_val {{
    font-size: 28px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
}}
QLabel#timer {{
    font-size: 32px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    font-family: 'Courier New', monospace;
    letter-spacing: 2px;
}}
QLabel#status_on {{
    font-size: 11px;
    font-weight: 600;
    color: {ACCENT_GREEN};
    letter-spacing: 1px;
}}
QLabel#status_off {{
    font-size: 11px;
    font-weight: 600;
    color: {TEXT_MUTED};
    letter-spacing: 1px;
}}
QLabel#table_num {{
    font-size: 14px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    letter-spacing: 1px;
}}
QLabel#conn_ok {{
    font-size: 12px;
    font-weight: 600;
    color: {ACCENT_GREEN};
    padding: 4px 10px;
    background: {ACCENT_DIM};
    border-radius: 20px;
}}
QLabel#conn_err {{
    font-size: 12px;
    font-weight: 600;
    color: {RED};
    padding: 4px 10px;
    background: #2D1A1A;
    border-radius: 20px;
}}
QLabel#estimate {{
    font-size: 22px;
    font-weight: 700;
    color: {ACCENT_GREEN};
}}

/* ── Progress bar ── */
QProgressBar {{
    background: #1C2330;
    border: none;
    border-radius: 3px;
    height: 4px;
    text-align: center;
    color: transparent;
}}
QProgressBar::chunk {{
    background: {ACCENT_GREEN};
    border-radius: 3px;
}}

/* ── Form elements ── */
QLineEdit, QSpinBox, QComboBox {{
    background: #0D1117;
    border: 1px solid {BORDER};
    border-radius: 8px;
    color: {TEXT_PRIMARY};
    padding: 8px 12px;
    font-size: 13px;
    min-height: 36px;
    selection-background-color: {ACCENT_DIM};
}}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border: 1px solid {ACCENT_GREEN};
    outline: none;
}}
QComboBox::drop-down {{
    border: none;
    padding-right: 8px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {TEXT_SEC};
    width: 0; height: 0;
}}
QComboBox QAbstractItemView {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 8px;
    selection-background-color: {ACCENT_DIM};
    color: {TEXT_PRIMARY};
    padding: 4px;
}}
QSpinBox::up-button, QSpinBox::down-button {{
    background: {BORDER};
    border: none;
    border-radius: 3px;
    width: 18px;
}}

/* ── Buttons ── */
QPushButton#btn_start {{
    background: {ACCENT_GREEN};
    color: #0D1117;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
    min-height: 42px;
}}
QPushButton#btn_start:hover {{
    background: #56D364;
}}
QPushButton#btn_start:pressed {{
    background: #2EA043;
}}
QPushButton#btn_stop {{
    background: transparent;
    color: {RED};
    border: 1px solid {RED};
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: 600;
    min-height: 42px;
}}
QPushButton#btn_stop:hover {{
    background: #2D1A1A;
}}

/* ── Table / History ── */
QTableWidget {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 10px;
    gridline-color: {BORDER};
    color: {TEXT_PRIMARY};
    font-size: 13px;
    outline: none;
}}
QHeaderView::section {{
    background: #0D1117;
    color: {TEXT_MUTED};
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    padding: 10px 14px;
    border: none;
    border-bottom: 1px solid {BORDER};
}}
QTableWidget::item {{
    padding: 10px 14px;
    border-bottom: 1px solid {BORDER};
}}
QTableWidget::item:selected {{
    background: {ACCENT_DIM};
    color: {ACCENT_GREEN};
}}
QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 3px;
    min-height: 40px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""


class SerialThread(QThread):
    data_received = pyqtSignal(str)
    connection_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.ser = None

    def run(self):
        while True:
            if self.ser is None:
                try:
                    self.ser = serial.serial_for_url(RFC2217_URL, baudrate=115200, timeout=1)
                    self.connection_changed.emit(True)
                except:
                    self.connection_changed.emit(False)
                    self.msleep(2000)
                    continue
            try:
                if self.ser.in_waiting:
                    self.data_received.emit(self.ser.readline().decode(errors="ignore").strip())
            except:
                self.ser = None

    def send(self, msg):
        try:
            if self.ser:
                self.ser.write((msg + "\n").encode())
        except:
            self.ser = None


def make_label(text, obj_name, parent=None):
    lbl = QLabel(text, parent)
    lbl.setObjectName(obj_name)
    return lbl


class StatCard(QFrame):
    def __init__(self, label, value, accent=False):
        super().__init__()
        self.setObjectName("card")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(110)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 18, 20, 18)
        lay.setSpacing(6)

        lbl = make_label(label.upper(), "muted")
        lay.addWidget(lbl)

        if accent:
            self.val = make_label(value, "revenue_val")
        else:
            self.val = make_label(value, "stat_val")
        lay.addWidget(self.val)
        lay.addStretch()

    def set_value(self, v):
        self.val.setText(v)


class TableCard(QFrame):
    def __init__(self, num):
        super().__init__()
        self.num = num
        self.total_duration = 1
        self.setObjectName("card")
        self.setMinimumSize(260, 200)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 18, 20, 18)
        root.setSpacing(0)

        # Header row
        hdr = QHBoxLayout()
        self.title = make_label(f"MEJA {num}", "table_num")
        hdr.addWidget(self.title)
        hdr.addStretch()
        self.status = make_label("● KOSONG", "status_off")
        hdr.addWidget(self.status)
        root.addLayout(hdr)

        root.addSpacing(16)

        self.timer = make_label("00:00:00", "timer")
        root.addWidget(self.timer)

        root.addSpacing(14)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setFixedHeight(4)
        self.progress.setTextVisible(False)
        root.addWidget(self.progress)

        root.addSpacing(10)

        self.info = make_label("Idle", "muted")
        root.addWidget(self.info)
        root.addStretch()

    def update_card(self, active, remain):
        h = remain // 3600
        m = (remain % 3600) // 60
        s = remain % 60
        self.timer.setText(f"{h:02}:{m:02}:{s:02}")

        pct = int((remain / self.total_duration) * 100) if self.total_duration else 0
        pct = max(0, min(100, pct))
        self.progress.setValue(pct)

        if active:
            self.status.setText("● AKTIF")
            self.status.setObjectName("status_on")
            self.setStyleSheet(f"""
                QFrame#card {{
                    background: #0F1F14;
                    border: 1px solid {ACCENT_GREEN};
                    border-radius: 12px;
                }}
            """)
            self.info.setText(f"Sisa {h:02}:{m:02}:{s:02}")
        else:
            self.status.setText("● KOSONG")
            self.status.setObjectName("status_off")
            self.setStyleSheet("")
            self.info.setText("Idle")

        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Billiard Lighting")
        self.resize(1300, 840)
        self.setMinimumSize(1000, 680)

        self.total_revenue = 0
        self.table_duration = {}
        self._nav_btns = []

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(210)
        s = QVBoxLayout(sidebar)
        s.setContentsMargins(0, 0, 0, 0)
        s.setSpacing(0)

        logo = make_label("SBL", "logo")
        sub  = make_label("SMART BILLIARD", "logo_sub")
        s.addWidget(logo)
        s.addWidget(sub)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {BORDER}; margin: 0 16px;")
        s.addWidget(sep)
        s.addSpacing(12)

        nav_items = [
            ("ti-layout-dashboard", "Dashboard"),
            ("ti-table",           "Monitoring"),
            ("ti-receipt",         "Billing"),
            ("ti-history",         "History"),
        ]

        for i, (icon_cls, label) in enumerate(nav_items):
            btn = QPushButton(f"  {label}")
            btn.setObjectName("nav")
            btn.setProperty("active", i == 0)
            btn.setIcon(QIcon())
            btn.clicked.connect(lambda _, idx=i: self._switch(idx))
            s.addWidget(btn)
            self._nav_btns.append(btn)

        s.addStretch()

        # Connection badge
        self.conn_badge = make_label("● Disconnected", "conn_err")
        self.conn_badge.setAlignment(Qt.AlignCenter)
        self.conn_badge.setContentsMargins(0, 0, 0, 16)
        s.addWidget(self.conn_badge)

        root.addWidget(sidebar)

        # ── Main area ────────────────────────────────────
        self.stack = QStackedWidget()
        self.stack.setContentsMargins(0, 0, 0, 0)
        root.addWidget(self.stack)

        self.stack.addWidget(self._build_dashboard())
        self.stack.addWidget(self._build_monitoring())
        self.stack.addWidget(self._build_billing())
        self.stack.addWidget(self._build_history())

        # ── Serial ───────────────────────────────────────
        self.serial = SerialThread()
        self.serial.connection_changed.connect(self._on_conn)
        self.serial.data_received.connect(self.process_data)
        self.serial.start()

    # ── Navigation ────────────────────────────────────────
    def _switch(self, idx):
        self.stack.setCurrentIndex(idx)
        for i, b in enumerate(self._nav_btns):
            b.setProperty("active", i == idx)
            b.style().unpolish(b)
            b.style().polish(b)

    # ── Pages ────────────────────────────────────────────
    def _page_wrap(self, title_text):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(32, 28, 32, 28)
        lay.setSpacing(20)

        ttl = make_label(title_text, "h1")
        lay.addWidget(ttl)
        return page, lay

    def _build_dashboard(self):
        page, lay = self._page_wrap("Dashboard")

        # Stat row
        stat_row = QHBoxLayout()
        stat_row.setSpacing(14)

        self.card_rev    = StatCard("Total Pendapatan", "Rp 0", accent=True)
        self.card_active = StatCard("Meja Aktif", "0")
        self.card_empty  = StatCard("Meja Kosong", "4")

        for c in [self.card_rev, self.card_active, self.card_empty]:
            stat_row.addWidget(c)

        lay.addLayout(stat_row)

        # Quick table preview
        lbl = make_label("STATUS MEJA", "muted")
        lay.addWidget(lbl)

        self.dash_grid = QGridLayout()
        self.dash_grid.setSpacing(14)
        self.dash_cards = []
        for i in range(4):
            c = TableCard(i + 1)
            self.dash_cards.append(c)
            self.dash_grid.addWidget(c, i // 2, i % 2)

        lay.addLayout(self.dash_grid)
        lay.addStretch()
        return page

    def _build_monitoring(self):
        page, lay = self._page_wrap("Monitoring")

        lbl = make_label("STATUS REAL-TIME", "muted")
        lay.addWidget(lbl)

        grid = QGridLayout()
        grid.setSpacing(14)
        self.cards = []

        for i in range(4):
            c = TableCard(i + 1)
            self.cards.append(c)
            grid.addWidget(c, i // 2, i % 2)

        lay.addLayout(grid)
        lay.addStretch()
        return page

    def _build_billing(self):
        page, lay = self._page_wrap("Billing")

        row = QHBoxLayout()
        row.setSpacing(24)

        # Left — form
        form_card = QFrame()
        form_card.setObjectName("card")
        fc = QVBoxLayout(form_card)
        fc.setContentsMargins(24, 22, 24, 22)
        fc.setSpacing(18)

        fc.addWidget(make_label("BUAT SESI BARU", "muted"))
        fc.addSpacing(4)

        def field(label, widget):
            box = QVBoxLayout()
            box.setSpacing(6)
            lbl = make_label(label, "muted")
            box.addWidget(lbl)
            box.addWidget(widget)
            return box

        self.nama  = QLineEdit(); self.nama.setPlaceholderText("Nama pelanggan…")
        self.meja  = QComboBox(); self.meja.addItems(["1","2","3","4"])
        self.durasi = QSpinBox(); self.durasi.setRange(1, 999); self.durasi.setValue(60)
        self.durasi.setSuffix(" menit")

        fc.addLayout(field("Nama Pelanggan", self.nama))
        fc.addLayout(field("Nomor Meja",     self.meja))
        fc.addLayout(field("Durasi",         self.durasi))

        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {BORDER};")
        fc.addWidget(sep)

        est_row = QHBoxLayout()
        est_row.addWidget(make_label("ESTIMASI BIAYA", "muted"))
        est_row.addStretch()
        self.lblEstimate = make_label("Rp 35,000", "estimate")
        est_row.addWidget(self.lblEstimate)
        fc.addLayout(est_row)

        btn_start = QPushButton("▶  START SESSION")
        btn_start.setObjectName("btn_start")
        btn_stop  = QPushButton("■  STOP MEJA")
        btn_stop.setObjectName("btn_stop")

        fc.addWidget(btn_start)
        fc.addWidget(btn_stop)
        fc.addStretch()

        row.addWidget(form_card, 1)

        # Right — live info cards
        info_col = QVBoxLayout()
        info_col.setSpacing(14)

        self.bill_cards = []
        for i in range(4):
            c = TableCard(i + 1)
            self.bill_cards.append(c)
            info_col.addWidget(c)

        info_col.addStretch()
        row.addLayout(info_col, 1)

        lay.addLayout(row)

        self.durasi.valueChanged.connect(self.update_estimate)
        btn_start.clicked.connect(self.start_billing)
        btn_stop.clicked.connect(self.stop_billing)

        return page

    def _build_history(self):
        page, lay = self._page_wrap("History")

        self.history = QTableWidget(0, 5)
        self.history.setHorizontalHeaderLabels(
            ["Jam", "Pelanggan", "Meja", "Durasi", "Biaya"])
        self.history.horizontalHeader().setStretchLastSection(True)
        self.history.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history.verticalHeader().setVisible(False)
        self.history.setShowGrid(False)
        self.history.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.history.setAlternatingRowColors(False)

        lay.addWidget(self.history)
        return page

    # ── Logic ────────────────────────────────────────────
    def _on_conn(self, ok):
        if ok:
            self.conn_badge.setText("● Connected")
            self.conn_badge.setObjectName("conn_ok")
        else:
            self.conn_badge.setText("● Disconnected")
            self.conn_badge.setObjectName("conn_err")
        self.conn_badge.style().unpolish(self.conn_badge)
        self.conn_badge.style().polish(self.conn_badge)

    def update_estimate(self):
        biaya = int((self.durasi.value() / 60) * RATE_PER_HOUR)
        self.lblEstimate.setText(f"Rp {biaya:,.0f}")

    def start_billing(self):
        meja  = int(self.meja.currentText())
        dur   = self.durasi.value()
        nama  = self.nama.text() or "—"

        self.serial.send(f"M{meja},{dur}")

        biaya = int((dur / 60) * RATE_PER_HOUR)
        self.total_revenue += biaya
        self.card_rev.set_value(f"Rp {self.total_revenue:,.0f}")

        self.table_duration[meja] = dur * 60
        td = dur * 60
        for card_set in [self.cards, self.dash_cards, self.bill_cards]:
            card_set[meja - 1].total_duration = td

        row = self.history.rowCount()
        self.history.insertRow(row)

        data = [
            time.strftime("%H:%M:%S"),
            nama,
            f"Meja {meja}",
            f"{dur} menit",
            f"Rp {biaya:,.0f}",
        ]
        for c, v in enumerate(data):
            item = QTableWidgetItem(v)
            item.setForeground(QColor(TEXT_PRIMARY))
            self.history.setItem(row, c, item)

        self.history.scrollToBottom()

    def stop_billing(self):
        self.serial.send(f"STOP,{self.meja.currentText()}")

    def update_dashboard(self):
        active = sum(1 for c in self.cards if "AKTIF" in c.status.text())
        self.card_active.set_value(str(active))
        self.card_empty.set_value(str(4 - active))

    def process_data(self, txt):
        if txt.startswith("T"):
            try:
                t, s, r = txt.split(":")
                idx    = int(t[1:]) - 1
                remain = int(r)
                active = s == "ON"

                for card_set in [self.cards, self.dash_cards, self.bill_cards]:
                    card_set[idx].update_card(active, remain)

                self.update_dashboard()
            except:
                pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window,          QColor(DARK_BG))
    palette.setColor(QPalette.WindowText,      QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Base,            QColor(CARD_BG))
    palette.setColor(QPalette.AlternateBase,   QColor(DARK_BG))
    palette.setColor(QPalette.Text,            QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Button,          QColor(CARD_BG))
    palette.setColor(QPalette.ButtonText,      QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Highlight,       QColor(ACCENT_DIM))
    palette.setColor(QPalette.HighlightedText, QColor(ACCENT_GREEN))
    app.setPalette(palette)

    app.setStyleSheet(QSS)

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())