import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab03_tech_company_factory import TechCompanyFactory
from source.lab03_sales_company_factory import SalesCompanyFactory

# Техническая компания
tech_factory = TechCompanyFactory()
tech_co = tech_factory.build_company("InnoTech Ltd", num_depts=2, num_employees_per_dept=4, num_projects=1)
print("=== Tech Company ===")
print(tech_co.get_company_statistics())

# Компания по продажам
sales_factory = SalesCompanyFactory()
sales_co = sales_factory.build_company("MegaSales Inc", num_depts=3, num_employees_per_dept=5, num_projects=2)
print("\n=== Sales Company ===")
print(sales_co.get_company_statistics())