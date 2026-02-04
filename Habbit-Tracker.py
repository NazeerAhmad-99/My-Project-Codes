import calendar
import datetime
import sys

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QProgressBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ConsistencyDashboard(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.today = datetime.date.today()
        self.year = self.today.year
        self.month = self.today.month
        self.days_in_month = calendar.monthrange(self.year, self.month)[1]
        self.is_updating_table = False

        self.table: QTableWidget | None = None
        self.habit_input: QLineEdit | None = None
        self.weekly_bar: QProgressBar | None = None
        self.week_info: QLabel | None = None
        self.weekly_refresh_timer: QTimer | None = None
        self.active_week_start_day = ((self.today.day - 1) // 7) * 7 + 1

        self.setWindowTitle("Consistency Dashboard")
        self.resize(1360, 820)

        self._apply_theme()
        self._build_layout()
        self._configure_table()
        self._connect_signals()
        self._seed_demo_habits()
        self._refresh_weekly_progress()
        self._start_weekly_refresh_timer()

    def _apply_theme(self) -> None:
        self.setStyleSheet(
            """
            QWidget { color: #1f1f1f; }
            QMainWindow { background-color: #f4f4f4; }
            QLabel#titleLabel { font-size: 28px; font-weight: 700; color: #1f1f1f; }
            QLabel#monthLabel { font-size: 44px; font-weight: 800; color: #1f1f1f; letter-spacing: 1px; }
            QFrame.card { background-color: #fbfbfb; border: 1px solid #d6d6d6; border-radius: 12px; }
            QLineEdit { background: #ffffff; color: #1f1f1f; border: 2px solid #111111; border-radius: 8px; padding: 8px; font-size: 14px; }
            QPushButton { background-color: #5fbf6a; color: #ffffff; border: none; border-radius: 8px; padding: 9px 14px; font-weight: 600; }
            QPushButton:hover { background-color: #4cae58; }
            QTableWidget { background: #ffffff; color: #1f1f1f; gridline-color: #d9d9d9; font-size: 13px; alternate-background-color: #f8fdf8; }
            QTableWidget::indicator {
                width: 14px;
                height: 14px;
                border: 1px solid #111111;
                background: #ffffff;
            }
            QTableWidget::indicator:checked {
                border: 1px solid #111111;
                background-color: #5fbf6a;
            }
            QHeaderView::section { background-color: #6fcb74; color: #1a1a1a; border: 1px solid #9cdb9f; font-weight: 700; padding: 4px; }
            QProgressBar { border: 1px solid #cfcfcf; border-radius: 8px; text-align: center; background: #ffffff; min-height: 34px; font-weight: 600; }
            QProgressBar::chunk { background-color: #5fbf6a; border-radius: 7px; }
            """
        )

    def _build_layout(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(14)

        top_row = QHBoxLayout()
        top_row.setSpacing(14)
        root_layout.addLayout(top_row, 2)

        title_card = QFrame()
        title_card.setProperty("class", "card")
        title_layout = QVBoxLayout(title_card)

        title_label = QLabel("THE CONSISTENCY DASHBOARD")
        title_label.setObjectName("titleLabel")

        month_text = datetime.date(self.year, self.month, 1).strftime("%B").upper()
        month_label = QLabel(month_text)
        month_label.setObjectName("monthLabel")

        title_layout.addWidget(title_label)
        title_layout.addWidget(month_label)
        title_layout.addStretch()

        graph_card = QFrame()
        graph_card.setProperty("class", "card")
        graph_layout = QVBoxLayout(graph_card)

        graph_title = QLabel("Monthly Progress")
        graph_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #252525;")

        graph_placeholder = QLabel("Line graph goes here")
        graph_placeholder.setAlignment(Qt.AlignCenter)
        graph_placeholder.setMinimumHeight(220)
        graph_placeholder.setStyleSheet(
            "background-color: #e8f5e9; border: 1px solid #b9dfbc; border-radius: 10px; font-size: 14px; color: #3a6b3d;"
        )

        graph_layout.addWidget(graph_title)
        graph_layout.addWidget(graph_placeholder)

        top_row.addWidget(title_card, 1)
        top_row.addWidget(graph_card, 2)

        content_row = QHBoxLayout()
        content_row.setSpacing(14)
        root_layout.addLayout(content_row, 5)

        tracker_card = QFrame()
        tracker_card.setProperty("class", "card")
        tracker_layout = QVBoxLayout(tracker_card)

        add_row = QHBoxLayout()
        self.habit_input = QLineEdit()
        self.habit_input.setPlaceholderText("Add habit (e.g. Study, Run, Read 20 pages)")

        self.add_button = QPushButton("Add Habit")
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.setStyleSheet(
            "QPushButton { background-color: #1f1f1f; color: #ffffff; border: none; border-radius: 8px; padding: 9px 14px; font-weight: 600; }"
            "QPushButton:hover { background-color: #000000; }"
        )
        add_row.addWidget(self.habit_input)
        add_row.addWidget(self.add_button)
        add_row.addWidget(self.remove_button)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)

        tracker_layout.addLayout(add_row)
        tracker_layout.addWidget(self.table)

        right_card = QFrame()
        right_card.setProperty("class", "card")
        right_layout = QVBoxLayout(right_card)

        weekly_title = QLabel("Weekly Progress")
        weekly_title.setAlignment(Qt.AlignCenter)
        weekly_title.setStyleSheet("font-size: 20px; font-weight: 700; color: #1f1f1f;")

        self.weekly_bar = QProgressBar()
        self.weekly_bar.setRange(0, 100)
        self.weekly_bar.setValue(0)
        self.weekly_bar.setFormat("%p%")

        self.week_info = QLabel("Current week completion: 0%")
        self.week_info.setAlignment(Qt.AlignCenter)
        self.week_info.setStyleSheet("font-size: 14px; color: #3d3d3d;")

        right_layout.addWidget(weekly_title)
        right_layout.addWidget(self.weekly_bar)
        right_layout.addWidget(self.week_info)
        right_layout.addStretch()

        content_row.addWidget(tracker_card, 4)
        content_row.addWidget(right_card, 1)

    def _configure_table(self) -> None:
        headers = ["Habits"] + [str(day) for day in range(1, self.days_in_month + 1)] + ["%"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(0)

        self.table.setColumnWidth(0, 230)
        for col in range(1, self.days_in_month + 1):
            self.table.setColumnWidth(col, 32)
        self.table.setColumnWidth(self.days_in_month + 1, 55)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(self.days_in_month + 1, QHeaderView.Fixed)

    def _connect_signals(self) -> None:
        self.add_button.clicked.connect(self._add_habit_from_input)
        self.remove_button.clicked.connect(self._remove_selected_habits)
        self.table.itemChanged.connect(self._handle_item_changed)

    def _start_weekly_refresh_timer(self) -> None:
        # Re-check date periodically so weekly bar resets automatically when a new week starts.
        self.weekly_refresh_timer = QTimer(self)
        self.weekly_refresh_timer.setInterval(60_000)
        self.weekly_refresh_timer.timeout.connect(self._sync_active_week_with_today)
        self.weekly_refresh_timer.start()

    def _sync_active_week_with_today(self) -> None:
        today = datetime.date.today()
        if today.year != self.year or today.month != self.month:
            return
        current_week_start = ((today.day - 1) // 7) * 7 + 1
        if current_week_start != self.active_week_start_day:
            self.active_week_start_day = current_week_start
        self._refresh_weekly_progress()

    def _seed_demo_habits(self) -> None:
        for habit_name in ["Gym", "Study for 4 hours", "Keep diet consistent", "Journal"]:
            self._add_habit_row(habit_name)

    def _add_habit_from_input(self) -> None:
        habit_name = self.habit_input.text().strip()
        if not habit_name:
            return

        self._add_habit_row(habit_name)
        self.habit_input.clear()
        self._refresh_weekly_progress()

    def _add_habit_row(self, habit_name: str) -> None:
        self.is_updating_table = True

        row = self.table.rowCount()
        self.table.insertRow(row)

        name_item = QTableWidgetItem(habit_name)
        name_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.table.setItem(row, 0, name_item)

        for day_col in range(1, self.days_in_month + 1):
            check_item = QTableWidgetItem("")
            check_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            check_item.setCheckState(Qt.Unchecked)
            check_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, day_col, check_item)

        percent_item = QTableWidgetItem("0%")
        percent_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        percent_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, self.days_in_month + 1, percent_item)

        self.is_updating_table = False

    def _remove_selected_habits(self) -> None:
        selected_rows = sorted({index.row() for index in self.table.selectionModel().selectedRows()}, reverse=True)
        if not selected_rows:
            return

        self.is_updating_table = True
        for row in selected_rows:
            self.table.removeRow(row)
        self.is_updating_table = False
        self._refresh_weekly_progress()

    def _handle_item_changed(self, item: QTableWidgetItem) -> None:
        if self.is_updating_table:
            return

        column = item.column()
        if 1 <= column <= self.days_in_month:
            self.active_week_start_day = ((column - 1) // 7) * 7 + 1
            self._update_row_percent(item.row())
            self._refresh_weekly_progress()

    def _update_row_percent(self, row: int) -> None:
        checked_count = 0

        for col in range(1, self.days_in_month + 1):
            cell = self.table.item(row, col)
            if cell and cell.checkState() == Qt.Checked:
                checked_count += 1

        percent = round((checked_count / self.days_in_month) * 100) if self.days_in_month else 0

        self.is_updating_table = True
        percent_item = self.table.item(row, self.days_in_month + 1)
        if percent_item:
            percent_item.setText(f"{percent}%")
        self.is_updating_table = False

    def _refresh_weekly_progress(self) -> None:
        if self.table.rowCount() == 0:
            self.weekly_bar.setValue(0)
            self.week_info.setText("Current week completion: 0%")
            return

        week_start_day = self.active_week_start_day
        week_end_day = min(week_start_day + 6, self.days_in_month)
        days_in_week_slice = week_end_day - week_start_day + 1
        total_boxes = self.table.rowCount() * days_in_week_slice
        checked_boxes = 0

        for row in range(self.table.rowCount()):
            for day in range(week_start_day, week_end_day + 1):
                cell = self.table.item(row, day)
                if cell and cell.checkState() == Qt.Checked:
                    checked_boxes += 1

        week_percent = round((checked_boxes / total_boxes) * 100) if total_boxes else 0
        self.weekly_bar.setValue(week_percent)
        self.week_info.setText(f"Week {week_start_day}-{week_end_day} completion: {week_percent}%")


def main() -> None:
    app = QApplication(sys.argv)
    window = ConsistencyDashboard()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
