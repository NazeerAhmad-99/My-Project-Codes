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
        
        
        
    }