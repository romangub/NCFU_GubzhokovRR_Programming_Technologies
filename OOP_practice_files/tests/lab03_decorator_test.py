import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/OOP_practice_files")

from source.lab0202_employee import Employee
from source.lab0202_developer import Developer
from source.lab03_employee_decorators import BonusDecorator, TrainingDecorator

emp = Employee(id=1, name="Иван", department="HR", base_salary=5000)
print("Обычный:", emp.calculate_salary())  # 5000
print(emp.get_info())

bonus_emp = BonusDecorator(emp, fixed_bonus=2000)
print("\nС бонусом:", bonus_emp.calculate_salary())  # 7000
print(bonus_emp.get_info())

trained_emp = TrainingDecorator(emp, training_name="Leadership Course")
print("\nС тренингом:", trained_emp.calculate_salary())  # 5500
print(trained_emp.get_info())

double_emp = TrainingDecorator(BonusDecorator(emp, fixed_bonus=2000), "Advanced Python")
print("\nБонус + тренинг:", double_emp.calculate_salary())  # (5000 + 2000) * 1.10 = 7700
print(double_emp.get_info())

from source.lab0202_abstract_employee import AbstractEmployee
print(isinstance(double_emp, AbstractEmployee))