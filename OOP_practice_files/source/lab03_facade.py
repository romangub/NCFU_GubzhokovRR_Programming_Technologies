from typing import Optional, List
import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/OOP_practice_files")

from source.lab0204_company import Company
from source.lab0203_department import Department
from source.lab0202_abstract_employee import AbstractEmployee
from source.lab03_employee_builder import EmployeeBuilder

class CompanyFacade:
    def __init__(self, company_name: str = "MyCompany"):
        self.company = Company(company_name)

    def hire_employee(self,
                    emp_type: str,  # Не используется сейчас, но можно для будущей логики
                    name: str,
                    department_name: str,
                    base_salary: float,
                    **extra_params) -> AbstractEmployee:
        try:
            try:
                department = self.company.get_department(department_name)
            except:
                department = Department(department_name)
                self.company.add_department(department)

            all_emps = self.company.get_all_employees()
            new_id = max([e.id for e in all_emps], default=0) + 1

            builder = (EmployeeBuilder()
                    .with_id(new_id)  
                    .with_name(name)
                    .with_department(department_name)
                    .with_base_salary(base_salary))

            if extra_params.get("bonus") is not None:
                builder.with_bonus(extra_params["bonus"])
            if extra_params.get("tech_stack") is not None:
                builder.with_tech_stack(extra_params["tech_stack"])
            if extra_params.get("seniority_level") is not None:
                builder.with_seniority_level(extra_params["seniority_level"])
            if extra_params.get("commission_rate") is not None:
                builder.with_commission_rate(extra_params["commission_rate"])
            if extra_params.get("sales_volume") is not None:
                builder.with_sales_volume(extra_params["sales_volume"])

            employee = builder.build()

            department.add_employee(employee)

            print(f"Сотрудник {name} нанят в отдел {department_name} с ID {new_id}")
            return employee

        except Exception as e:
            print(f"Ошибка при найме: {e}")
            raise
    
    def fire_employee(self, employee_id: int) -> None:
        try:
            emp_dep = self.company.find_employee_by_id(employee_id)
            if not emp_dep:
                raise ValueError(f"Сотрудник с ID {employee_id} не найден")
            employee, department = emp_dep
            department.remove_employee(employee_id)
            print(f"Сотрудник {employee.name} (ID: {employee_id}) уволен из отдела {department.name}")
        except Exception as e:
            print(f"Ошибка при увольнении: {e}")
            raise

    def calculate_total_payroll(self) -> float:
        total = self.company.calculate_total_monthly_cost()
        print(f"Общий фонд зарплаты: {total:.2f}")
        return total

    def get_employee_salary(self, employee_id: int) -> float:
        try:
            employee, _ = self.company.find_employee_by_id(employee_id)
            salary = employee.calculate_salary()
            print(f"Зарплата {employee.name}: {salary:.2f}")
            return salary
        except Exception as e:
            print(f"Ошибка: {e}")
            raise

    def transfer_employee(self, employee_id: int, new_department_name: str) -> None:
        try:
            self.company.transfer_employee(employee_id, new_department_name)
            print(f"Сотрудник ID {employee_id} переведён в {new_department_name}")
        except Exception as e:
            print(f"Ошибка перевода: {e}")

    def get_statistics(self) -> dict:
        return self.company.get_company_statistics()

    def save_to_db(self, db_path: str = "company.db"):
        self.company.save_to_db(db_path)

    def load_from_db(self, db_path: str = "company.db"):
        self.company.load_from_db(db_path)