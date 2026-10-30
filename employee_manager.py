"""Employee and department CRUD operations."""
import pandas as pd
from database import get_connection


def add_department(name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO departments (department_name) VALUES (%s)", (name,)
    )
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return new_id


def list_departments():
    connection = get_connection()
    df = pd.read_sql(
        """SELECT department_id, department_name
           FROM departments ORDER BY department_name""",
        connection,
    )
    connection.close()
    return df


def add_employee(name, email, phone, department_id, monthly_salary, joining_date):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO employees
           (employee_name, email, phone, department_id, monthly_salary, joining_date)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (name, email or None, phone or None, department_id or None,
         monthly_salary, joining_date or None),
    )
    connection.commit()
    employee_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return employee_id


def list_employees():
    connection = get_connection()
    query = """
        SELECT e.employee_id, e.employee_name, e.email, e.phone,
               d.department_name, e.monthly_salary, e.joining_date
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.department_id
        ORDER BY e.employee_id
    """
    df = pd.read_sql(query, connection)
    connection.close()
    return df


def update_employee(employee_id, name, email, phone, department_id,
                    monthly_salary, joining_date):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """UPDATE employees
           SET employee_name=%s, email=%s, phone=%s, department_id=%s,
               monthly_salary=%s, joining_date=%s
           WHERE employee_id=%s""",
        (name, email or None, phone or None, department_id or None,
         monthly_salary, joining_date or None, employee_id),
    )
    connection.commit()
    changed = cursor.rowcount
    cursor.close()
    connection.close()
    return changed


def delete_employee(employee_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM employees WHERE employee_id=%s", (employee_id,))
    connection.commit()
    deleted = cursor.rowcount
    cursor.close()
    connection.close()
    return deleted
