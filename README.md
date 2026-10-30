# Employee Management System

A beginner-friendly, menu-driven Python project to manage employee details,
departments, attendance and simple monthly salary calculations.

## Technologies

- Python
- Pandas — read, organize and export employee data
- NumPy — perform salary calculations
- MySQL — store employee, department, attendance and salary records
- `mysql-connector-python` — connect Python to MySQL

> MySQL requires a Python database connector. The project uses
> `mysql-connector-python` for this connection. Pandas and NumPy are used
> for data processing and calculations. No web framework is used.

## Features

1. Add and view departments
2. Register and view employees
3. Update and delete employee records (CRUD)
4. Mark daily attendance as Present or Absent
5. View attendance by month
6. Calculate simple monthly salary based on present days
7. View monthly salary report
8. Export employee, attendance and salary reports to CSV

## Project structure

```text
employee-management-system/
├── main.py
├── config.py
├── database.py
├── employee_manager.py
├── attendance_manager.py
├── salary_manager.py
├── report_manager.py
├── requirements.txt
├── README.md
├── .gitignore
└── reports/
```

## Requirements

- Python 3.10 or newer
- MySQL Server running on your computer

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/employee-management-system.git
cd employee-management-system
```

### 2. Create and activate a virtual environment (optional but recommended)

Windows:

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python packages

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database

Open MySQL Workbench or the MySQL command line and run:

```sql
CREATE DATABASE employee_management;
```

The application creates its tables the first time it starts.

### 5. Set your MySQL connection details

The defaults in `config.py` are:
- Host: `localhost`
- User: `root`
- Password: empty
- Database: `employee_management`
- Port: `3306`

For a safer setup, set environment variables instead of putting your password
in source code.

Windows PowerShell:

```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="your_mysql_password"
$env:MYSQL_DATABASE="employee_management"
$env:MYSQL_PORT="3306"
```

macOS/Linux:

```bash
export MYSQL_HOST="localhost"
export MYSQL_USER="root"
export MYSQL_PASSWORD="your_mysql_password"
export MYSQL_DATABASE="employee_management"
export MYSQL_PORT="3306"
```

### 6. Run the application

```bash
python main.py
```

Use the numbered menu to manage departments, employees, attendance and salary.

## Salary calculation rule

This beginner project uses a simple example:

`Daily salary = Monthly salary / Working days`

`Calculated salary = Daily salary * Present days`

For example, if monthly salary is ₹30,000, working days are 30 and present
days are 26, calculated salary is ₹26,000.

This is a learning example, not a complete payroll system. It does not calculate
tax, overtime, bonuses, paid leave, weekly offs or statutory deductions.
Enter the correct number of salary working days for the month.

## CSV reports

The application creates these reports inside `reports/`:

- `employees_report.csv`
- `attendance_YYYY-MM.csv`
- `salary_YYYY-MM.csv`

## Important notes

- Attendance can be marked once per employee per date. Marking it again updates
  that day's status.
- Employee IDs are created by MySQL.
- Deleting an employee also deletes that employee's attendance and salary rows.
- Do not upload database passwords or private employee information to GitHub.
- Use sample or fictional employee data in a public repository.

## Resume project description

**Employee Management System | Python, Pandas, NumPy, MySQL**

- Developed a Python-based employee management application to maintain employee
  records, department details, daily attendance and monthly salary information.
- Implemented employee CRUD operations and stored employee and attendance data
  in a MySQL database.
- Used Pandas to process employee records and generate CSV reports, and NumPy
  to calculate attendance-based monthly salaries.

## Future improvements

- Add paid leave and half-day options
- Search employees by name or department
- Add input validation for dates and salary values
- Add unit tests
