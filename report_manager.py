"""Export employee, attendance and salary reports to CSV."""
from pathlib import Path
import pandas as pd
from employee_manager import list_employees
from attendance_manager import get_attendance
from salary_manager import get_salary_report

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


def export_employee_report():
    df = list_employees()
    path = REPORT_DIR / "employees_report.csv"
    df.to_csv(path, index=False)
    return path


def export_attendance_report(month):
    df = get_attendance(month)
    path = REPORT_DIR / f"attendance_{month}.csv"
    df.to_csv(path, index=False)
    return path


def export_salary_report(month):
    df = get_salary_report(month)
    path = REPORT_DIR / f"salary_{month}.csv"
    df.to_csv(path, index=False)
    return path
