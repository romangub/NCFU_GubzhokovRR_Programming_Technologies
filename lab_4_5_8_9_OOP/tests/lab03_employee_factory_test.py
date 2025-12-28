import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab0202_abstract_employee import AbstractEmployee
from source.lab0202_employee_factory import BasicEmployeeFactory
from source.lab0202_employee_factory import ManagerFactory
from source.lab0202_employee_factory import DeveloperFactory
from source.lab0202_employee_factory import SalespersonFactory

if __name__ == "__main__":
    try:
        emp_factory = BasicEmployeeFactory()
        emp = emp_factory.create_employee(id=1, name="John Doe", department="HR", base_salary=5000.0)
        print(f"Создан: {type(emp).__name__}, Имя: {emp.name}")

        mgr_factory = ManagerFactory()
        mgr = mgr_factory.create_employee(id=2, name="Alice Smith", department="Management", base_salary=7000.0, bonus=2000.0)
        print(f"Создан: {type(mgr).__name__}, Имя: {mgr.name}, Бонус: {mgr.bonus}")

        dev_factory = DeveloperFactory()
        dev = dev_factory.create_employee(id=3, name="Bob Johnson", department="Dev", base_salary=6000.0, tech_stack=["Python", "SQL"], seniority_level="senior")
        print(f"Создан: {type(dev).__name__}, Имя: {dev.name}, Tech Stack: {dev.tech_stack}")

        sales_factory = SalespersonFactory()
        sales = sales_factory.create_employee(id=4, name="Carol Davis", department="Sales", base_salary=4000.0, commission_rate=0.12, sales_volume=100000.0)
        print(f"Создан: {type(sales).__name__}, Имя: {sales.name}, Commission Rate: {sales.commission_rate}")

        mgr_factory.create_employee(id=5, name="Error", department="Test", base_salary=5000.0)  # Нет bonus

    except ValueError as e:
        print(f"Ошибка: {e}")