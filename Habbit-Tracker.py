import calendar
import datetime
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
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

def create_state() -> dict:
    today = datetime.date.today()
    return{
        "today": today,
        "year":today.year,
        "month": today.month,
        "days_in_month": calendar.monthrange(today.year, today.month)[1],
        "updating_table": False,
        "window": None,
        "table": None,
        "habit_input": None,
        "weekly_bar": None,
        "week_info": None,
    }

def apply_theme(window: QMainWindow) -> None:
    window.setStyleSheet(
    """
        QMainWindow { background-color: #f4f4f4; }
        QLabel#titleLabel { font-size: 28px; font-weight: 700; color: #1f1f1f; }
        QLabel#monthLabel { font-size: 44px; font-weight: 800; color: #1f1f1f; letter-spacing: 1px; }
        QFrame.card { background-color: #fbfbfb; border: 1px solid #d6d6d6; border-radius: 12px; }
        QLineEdit { background: #ffffff; border: 1px solid #cfcfcf; border-radius: 8px; padding: 8px; font-size: 14px; }
        QPushButton { background-color: #5fbf6a; color: #ffffff; border: none; border-radius: 8px; padding: 9px 14px; font-weight: 600; }
        QPushButton:hover { background-color: #4cae58; }
        QTableWidget { background: #ffffff; gridline-color: #d9d9d9; font-size: 13px; alternate-background-color: #f8fdf8; }
        QHeaderView::section { background-color: #6fcb74; color: #1a1a1a; border: 1px solid #9cdb9f; font-weight: 700; padding: 4px; }
        QProgressBar { border: 1px solid #cfcfcf; border-radius: 8px; text-align: center; background: #ffffff; min-height: 34px; font-weight: 600; }
        QProgressBar::chunk { background-color: #5fbf6a; border-radius: 7px; }
        """
    )
    
def configure_table(state:dict) -> None:
    table = state["table"]
    days = state["days_in_month"]
    
    headers = ["Habits"] + [str(day) for day in range(1,days + 1 )] + ["%"]
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.setRowCount(0)
    
    table.setColumnWidth(0,230)
    for col in range(1, days + 1):
        table.setColumnWidth(col,32)
    table.setColumnWidth(days + 1, 55)
    
    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.Fixed)
    header.setSectionResizeMode(days + 1, QHeaderView.Fixed)
    
def update_row_percent(state: dict, row:int) -> None:
    table = state["table"]
    days = state["days_in_month"]
    
    checked = 0
    for col in range(1, days + 1):
        cell = table.item(row, col)
        if cell and cell.checkState() == Qt.Checked:
            checked += 1
    pct = round((checked / days) * 100) if days else 0
    
    state["updating_table"] = True
    pct_item = table.item(row, days + 1)
    if pct_item:
        pct_item.setText(f"{pct}%")
    state["updating_table"] = False
    
