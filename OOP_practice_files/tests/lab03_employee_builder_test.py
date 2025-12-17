import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/OOP_practice_files")

from source.lab03_employee_builder import EmployeeBuilder

# Простой сотрудник
emp1 = (EmployeeBuilder()
        .with_id(1)
        .with_name("Иван Иванов")
        .with_department("HR")
        .with_base_salary(4000)
        .build())
print(emp1)  # Employee

# Менеджер
mgr = (EmployeeBuilder()
       .with_id(2)
       .with_name("Анна Петрова")
       .with_department("Management")
       .with_base_salary(7000)
       .with_bonus(2500)
       .build())
print(mgr)  # Manager

# Разработчик с навыками
dev = (EmployeeBuilder()
       .with_id(3)
       .with_name("Боб Смит")
       .with_department("Development")
       .with_base_salary(6000)
       .add_skill("Python")
       .add_skill("Django")
       .add_skill("Docker")
       .with_seniority_level("senior")
       .build())
print(dev)  # Developer
print(dev.tech_stack)  # ['Python', 'Django', 'Docker']

# Продавец
sales = (EmployeeBuilder()
         .with_id(4)
         .with_name("Ева Мартинес")
         .with_department("Sales")
         .with_base_salary(4500)
         .with_commission_rate(0.15)
         .with_sales_volume(120000)
         .build())
print(sales)  # Salesperson