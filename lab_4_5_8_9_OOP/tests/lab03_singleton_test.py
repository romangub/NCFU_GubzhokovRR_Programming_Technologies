import sys
import os

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab0204_company import Company
from source.lab03_singleton import DatabaseConnection
from source.lab0203_department import Department
from source.lab0202_manager import Manager
from source.lab0202_developer import Developer
from source.lab0202_salesperson import Salesperson
from source.lab0202_employee import Employee

db_path = os.path.abspath("OOP_practice_files/sqlite3_DB/company.db")

db_connection = DatabaseConnection.get_instance(db_path) 

company = Company("TestCorp")

employees = [
        Manager(1, "Alice Johnson", "Development", 7000, 2000),
        Developer(2, "Bob Smith", "Development", 5000, 
                 ["Python", "SQL", "Django", "FastAPI"], "senior"),
        Developer(3, "Carol Davis", "Development", 4500,
                 ["JavaScript", "React", "Node.js"], "middle"),
        Salesperson(4, "David Wilson", "Sales", 4000, 0.12, 75000),
        Salesperson(5, "Eva Martinez", "Sales", 3800, 0.10, 60000),
        Employee(6, "Frank Brown", "Marketing", 3500)
    ]
dept_mapping = {
    "Development": [employees[0], employees[1], employees[2]],
    "Sales": [employees[3], employees[4]],
    "Marketing": [employees[5]]
}

for name in dept_mapping:
    print(name)
    dept = Department(name)
    company.add_department(dept)
    
for dept_name, dept_employees in dept_mapping.items():
    dept = company.get_department(dept_name)
    for emp in dept_employees:
        dept.add_employee(emp)

company.save_to_db(db_path)
company.clear_departments()
company.load_from_db(db_path)
print(company)