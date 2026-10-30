"""Calculate monthly salary using NumPy."""
import numpy as np
import pandas as pd
from database import get_connection


def calculate_monthly_salaries(month, working_days):
    """Calculate salary after deducting absent days.

    Simple rule for this beginner project:
    daily rate = monthly salary / working days
    final salary = daily rate * present days

    This example does not include tax, overtime, bonuses or statutory deductions.
    """
    if working_days <= 0:
        raise ValueError("Working days must be greater than zero.")

    connection = get_connection()
    employees = pd.read_sql(
        """SELECT employee_id, employee_name, monthly_salary
           FROM employees ORDER BY employee_id""",
        connection,
    )
    attendance = pd.read_sql(
        """SELECT employee_id, status FROM attendance
           WHERE DATE_FORMAT(attendance_date, '%Y-%m') = %s""",
        connection,
        params=(month,),
    )

    if employees.empty:
        connection.close()
        return pd.DataFrame()

    present_counts = (
        attendance[attendance["status"] == "Present"]
        .groupby("employee_id")
        .size()
    )

    employees["present_days"] = (
        employees["employee_id"].map(present_counts).fillna(0).astype(int)
    )
    employees["present_days"] = employees["present_days"].clip(
        lower=0, upper=working_days
    )

    monthly = employees["monthly_salary"].astype(float).to_numpy()
    present = employees["present_days"].to_numpy(dtype=float)

    daily_rates = np.divide(monthly, working_days)
    calculated = np.round(daily_rates * present, 2)

    employees["working_days"] = working_days
    employees["calculated_salary"] = calculated

    cursor = connection.cursor()
    for row in employees.itertuples(index=False):
        cursor.execute(
            """INSERT INTO salary_records
               (employee_id, salary_month, working_days, present_days,
                monthly_salary, calculated_salary)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE
                 working_days=VALUES(working_days),
                 present_days=VALUES(present_days),
                 monthly_salary=VALUES(monthly_salary),
                 calculated_salary=VALUES(calculated_salary)""",
            (int(row.employee_id), month, working_days, int(row.present_days),
             float(row.monthly_salary), float(row.calculated_salary)),
        )

    connection.commit()
    cursor.close()
    connection.close()

    return employees[
        ["employee_id", "employee_name", "monthly_salary",
         "working_days", "present_days", "calculated_salary"]
    ]


def get_salary_report(month):
    connection = get_connection()
    df = pd.read_sql(
        """SELECT s.employee_id, e.employee_name, s.salary_month,
                  s.working_days, s.present_days, s.monthly_salary,
                  s.calculated_salary
           FROM salary_records s
           JOIN employees e ON e.employee_id = s.employee_id
           WHERE s.salary_month = %s
           ORDER BY s.employee_id""",
        connection,
        params=(month,),
    )
    connection.close()
    return df
