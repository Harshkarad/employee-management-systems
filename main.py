"""Menu-driven Employee Management System."""
from datetime import date
import mysql.connector

from database import initialize_database
from employee_manager import (
    add_department, list_departments, add_employee, list_employees,
    update_employee, delete_employee,
)
from attendance_manager import mark_attendance, get_attendance
from salary_manager import calculate_monthly_salaries, get_salary_report
from report_manager import (
    export_employee_report, export_attendance_report, export_salary_report,
)


def show_menu():
    print("\n===== EMPLOYEE MANAGEMENT SYSTEM =====")
    print("1. Add department")
    print("2. View departments")
    print("3. Register employee")
    print("4. View employees")
    print("5. Update employee")
    print("6. Delete employee")
    print("7. Mark attendance")
    print("8. View monthly attendance")
    print("9. Calculate monthly salary")
    print("10. View salary report")
    print("11. Export employee CSV report")
    print("12. Export monthly attendance CSV")
    print("13. Export monthly salary CSV")
    print("0. Exit")


def get_department_id():
    departments = list_departments()
    if departments.empty:
        print("Add a department first.")
        return None
    print(departments.to_string(index=False))
    value = input("Department ID (leave blank for none): ").strip()
    return int(value) if value else None


def main():
    try:
        initialize_database()
    except mysql.connector.Error as error:
        print(f"Could not connect to MySQL: {error}")
        print("Check MySQL is running and your settings in config.py/environment.")
        return

    print("Database is ready.")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                name = input("Department name: ").strip()
                if name:
                    print("Department added. ID:", add_department(name))

            elif choice == "2":
                print(list_departments().to_string(index=False))

            elif choice == "3":
                name = input("Employee name: ").strip()
                email = input("Email (optional): ").strip()
                phone = input("Phone (optional): ").strip()
                department_id = get_department_id()
                salary = float(input("Monthly salary: "))
                joining_date = input("Joining date YYYY-MM-DD (optional): ").strip()
                employee_id = add_employee(
                    name, email, phone, department_id, salary, joining_date
                )
                print("Employee registered. ID:", employee_id)

            elif choice == "4":
                print(list_employees().to_string(index=False))

            elif choice == "5":
                employee_id = int(input("Employee ID to update: "))
                name = input("New employee name: ").strip()
                email = input("New email (optional): ").strip()
                phone = input("New phone (optional): ").strip()
                department_id = get_department_id()
                salary = float(input("New monthly salary: "))
                joining_date = input("Joining date YYYY-MM-DD (optional): ").strip()
                result = update_employee(
                    employee_id, name, email, phone, department_id,
                    salary, joining_date
                )
                print("Employee updated." if result else "Employee ID not found.")

            elif choice == "6":
                employee_id = int(input("Employee ID to delete: "))
                result = delete_employee(employee_id)
                print("Employee deleted." if result else "Employee ID not found.")

            elif choice == "7":
                employee_id = int(input("Employee ID: "))
                attendance_date = input("Date YYYY-MM-DD (default today): ").strip()
                if not attendance_date:
                    attendance_date = date.today().isoformat()
                status = input("Status (Present/Absent): ").strip().title()
                mark_attendance(employee_id, attendance_date, status)
                print("Attendance saved.")

            elif choice == "8":
                month = input("Month YYYY-MM: ").strip()
                print(get_attendance(month).to_string(index=False))

            elif choice == "9":
                month = input("Month YYYY-MM: ").strip()
                working_days = int(input("Number of salary working days: "))
                result = calculate_monthly_salaries(month, working_days)
                print(result.to_string(index=False) if not result.empty
                      else "No employees found.")

            elif choice == "10":
                month = input("Month YYYY-MM: ").strip()
                print(get_salary_report(month).to_string(index=False))

            elif choice == "11":
                print("Saved:", export_employee_report())

            elif choice == "12":
                month = input("Month YYYY-MM: ").strip()
                print("Saved:", export_attendance_report(month))

            elif choice == "13":
                month = input("Month YYYY-MM: ").strip()
                print("Saved:", export_salary_report(month))

            elif choice == "0":
                print("Thank you for using the Employee Management System.")
                break

            else:
                print("Please choose a valid menu option.")

        except (ValueError, mysql.connector.Error) as error:
            print("Could not complete the action:", error)


if __name__ == "__main__":
    main()
