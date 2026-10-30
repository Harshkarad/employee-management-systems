"""Record and view employee attendance."""
import pandas as pd
from database import get_connection


def mark_attendance(employee_id, attendance_date, status):
    if status not in ("Present", "Absent"):
        raise ValueError("Status must be Present or Absent.")

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO attendance (employee_id, attendance_date, status)
           VALUES (%s, %s, %s)
           ON DUPLICATE KEY UPDATE status=VALUES(status)""",
        (employee_id, attendance_date, status),
    )
    connection.commit()
    cursor.close()
    connection.close()


def get_attendance(month):
    connection = get_connection()
    query = """
        SELECT a.employee_id, e.employee_name, a.attendance_date, a.status
        FROM attendance a
        JOIN employees e ON e.employee_id = a.employee_id
        WHERE DATE_FORMAT(a.attendance_date, '%Y-%m') = %s
        ORDER BY a.attendance_date, a.employee_id
    """
    df = pd.read_sql(query, connection, params=(month,))
    connection.close()
    return df
