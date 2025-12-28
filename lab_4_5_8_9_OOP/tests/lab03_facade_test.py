import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab03_facade import CompanyFacade

facade = CompanyFacade("SuperCorp")

# Найм сотрудников "в один клик"
facade.hire_employee("developer", "Боб Смит", "Development", 6000, tech_stack=["Python", "Django"], seniority_level="senior")
facade.hire_employee("salesperson", "Ева", "Sales", 4500, commission_rate=0.15, sales_volume=100000)
facade.hire_employee("manager", "Анна", "Management", 8000, bonus=3000)

# Расчёт зарплат
facade.calculate_total_payroll()

# Увольнение
facade.fire_employee(1)  # предположим, ID=1

# Статистика
print(facade.get_statistics())