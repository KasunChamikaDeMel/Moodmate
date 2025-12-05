from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QCheckBox, QScrollArea, QWidget
)
from PySide6.QtCore import Qt, QTimer
import json
import os
from datetime import datetime

DATA_SOURCES = [
    os.path.join(os.path.dirname(__file__), '..', 'backend', 'data', 'analytics.json'),
    os.path.join(os.path.dirname(__file__), '..', 'backend', 'data', 'emotion_history.json'),
]

class LogsPage(QFrame):
    """Simple logging page that reads recent entries from backend JSON files."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.auto_refresh = False
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.load_logs)
        self.setup_ui()
        self.load_logs()

    def setup_ui(self):
        self.setStyleSheet("background-color: #3a404d;")

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title = QLabel("📜 Logs")
        title.setStyleSheet("QLabel { font-size: 24px; color: white; font-weight: bold; }")
        layout.addWidget(title)

        # Controls
        controls = QHBoxLayout()
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_logs)
        refresh_btn.setStyleSheet("QPushButton { background-color: #6c5ce7; color: white; border: none; border-radius: 8px; padding: 8px 16px; }")

        self.auto_refresh_check = QCheckBox("Auto refresh")
        self.auto_refresh_check.setStyleSheet("QCheckBox { color: #cccccc; }")
        self.auto_refresh_check.stateChanged.connect(self.on_auto_refresh_toggle)

        controls.addStretch()
        controls.addWidget(self.auto_refresh_check)
        controls.addWidget(refresh_btn)
        layout.addLayout(controls)

        # Table
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Time", "Source", "Type", "Message"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet(
            "QTableWidget { background-color: #424758; color: white; border: 1px solid #5c6378; }"
        )
        layout.addWidget(self.table)

        scroll.setWidget(content)
        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.addWidget(scroll)

    def on_auto_refresh_toggle(self, state):
        self.auto_refresh = bool(state)
        if self.auto_refresh:
            self._timer.start(3000)  # 3s
        else:
            self._timer.stop()

    def _read_json(self, path):
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return None

    def _normalize_entries(self, data, source):
        entries = []
        if isinstance(data, list):
            for item in data:
                ts = item.get('timestamp') or item.get('time') or item.get('date')
                msg = item.get('message') or item.get('mood') or item.get('emotion') or ''
                typ = item.get('type') or item.get('level') or 'info'
                entries.append({
                    'time': self._fmt_time(ts),
                    'source': source,
                    'type': str(typ),
                    'message': str(msg)
                })
        elif isinstance(data, dict):
            # Dict of events or a single event
            ts = data.get('timestamp') or data.get('time') or data.get('date')
            msg = data.get('message') or ''
            typ = data.get('type') or data.get('level') or 'info'
            entries.append({
                'time': self._fmt_time(ts),
                'source': source,
                'type': str(typ),
                'message': str(msg)
            })
        return entries

    def _fmt_time(self, ts):
        if not ts:
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            # Accept ISO or epoch seconds
            if isinstance(ts, (int, float)):
                return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            return str(ts)
        except Exception:
            return str(ts)

    def load_logs(self):
        rows = []
        for path in DATA_SOURCES:
            data = self._read_json(path)
            if data is not None:
                rows.extend(self._normalize_entries(data, os.path.basename(path)))
        # Fill table
        self.table.setRowCount(len(rows))
        for r, entry in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(entry['time']))
            self.table.setItem(r, 1, QTableWidgetItem(entry['source']))
            self.table.setItem(r, 2, QTableWidgetItem(entry['type']))
            self.table.setItem(r, 3, QTableWidgetItem(entry['message']))
        # Sort by time descending (string sort acceptable for common formats)
        self.table.sortItems(0, Qt.DescendingOrder)
