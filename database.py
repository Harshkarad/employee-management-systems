"""Small MySQL helper functions."""
import mysql.connector
from config import DB_CONFIG


def get_connection():
    """Open and return a MySQL database connection."""
    return mysql.connector.connect(**DB_CONFIG)


def initialize_database():
    """Create the tables used by this project."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            department_id INT AUTO_INCREMENT PRIMARY KEY,
            department_name VARCHAR(100) NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INT AUTO_INCREMENT PRIMARY KEY,
            employee_name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE,
            phone VARCHAR(20),
            department_id INT,
            monthly_salary DECIMAL(10, 2) NOT NULL,
            joining_date DATE,
            FOREIGN KEY (department_id)
                REFERENCES departments(department_id)
                ON DELETE SET NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id INT NOT NULL,
            attendance_date DATE NOT NULL,
            status ENUM('Present', 'Absent') NOT NULL,
            UNIQUE KEY unique_employee_day (employee_id, attendance_date),
            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id)
                ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salary_records (
            salary_id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id INT NOT NULL,
            salary_month CHAR(7) NOT NULL,
            working_days INT NOT NULL,
            present_days INT NOT NULL,
            monthly_salary DECIMAL(10, 2) NOT NULL,
            calculated_salary DECIMAL(10, 2) NOT NULL,
            UNIQUE KEY unique_employee_month (employee_id, salary_month),
            FOREIGN KEY (employee_id)
                REFERENCES employees(employee_id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()
