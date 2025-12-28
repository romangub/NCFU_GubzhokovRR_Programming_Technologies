import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab0202_manager import Manager
from source.lab0202_developer import Developer
from source.lab03_payroll_adapter import PayrollAdapter

# Создаём сотрудников
mgr = Manager(1, "Alice", "Management", 8000.0, bonus=3000.0)
dev = Developer(2, "Bob", "Development", 6000.0, tech_stack=["Python"], seniority_level="senior")

# Без адаптера — наш расчёт
print("Наш расчёт:")
print(mgr.calculate_salary())  # 8000 + 3000 = 11000
print(dev.calculate_salary())  # 6000 (или с коэффициентом seniority, если есть)

# С адаптером — внешняя система
adapter = PayrollAdapter()

print("\nЧерез адаптер (внешняя система):")
print(adapter.calculate_salary(mgr))  # ~ (8000/160 * 160 + 3000) * 0.87 ≈ 9570
print(adapter.calculate_salary(dev))  # ~ (6000/160 * 160) * 0.87 ≈ 5220