import random
import sys
from datetime import date, timedelta
from typing import Dict, Any, List

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/OOP_practice_files")

from source.lab0204_company import Company
from source.lab0203_department import Department
from source.lab0204_project import Project
from source.lab0202_abstract_employee import AbstractEmployee
from source.lab0202_salesperson import Salesperson
from source.lab0202_manager import Manager
from source.lab0202_employee import Employee  # базовый сотрудник для поддержки

from source.lab03_abstract_сompany_factory import AbstractCompanyFactory


class SalesCompanyFactory(AbstractCompanyFactory):

    def create_department(self, name: str) -> Department:
        return Department(name)

    def create_project(self, 
                       project_id: int, 
                       name: str, 
                       description: str = "", 
                       budget: float = 150000.0,
                       start_date: date = None,
                       end_date: date = None,
                       status: str = "planning") -> Project:
        if description == "":
            description = f"Маркетинговая кампания / увеличение продаж для {name}"
        if start_date is None:
            start_date = date.today() + timedelta(days=30)
        if end_date is None:
            end_date = start_date + timedelta(days=90)
        
        return Project(
            project_id=project_id,
            name=name,
            description=description,
            budget=budget,
            start_date=start_date,
            end_date=end_date,
            status=status
        )

    def create_employee(self, emp_type: str, **kwargs) -> 'AbstractEmployee':
        emp_type = emp_type.lower()
        if emp_type not in ["salesperson", "manager", "employee"]:
            raise ValueError(f"SalesCompanyFactory поддерживает только 'salesperson', 'manager', 'employee'. Получено: {emp_type}")
        
        defaults = {
            "id": kwargs.get("id", 1),
            "name": kwargs.get("name", "Unnamed Salesperson"),
            "department": kwargs.get("department", "Sales"),
            "base_salary": kwargs.get("base_salary", 4000.0)
        }
        defaults.update(kwargs)
        
        if emp_type == "salesperson":
            return Salesperson(
                id=defaults["id"],
                name=defaults["name"],
                department=defaults["department"],
                base_salary=defaults["base_salary"],
                commission_rate=defaults.get("commission_rate", 0.15),  # Высокая комиссия
                sales_volume=defaults.get("sales_volume", random.uniform(50000, 200000))
            )
        elif emp_type == "manager":
            return Manager(
                id=defaults["id"],
                name=defaults["name"],
                department=defaults["department"],
                base_salary=defaults["base_salary"],
                bonus=defaults.get("bonus", 1800.0)
            )
        elif emp_type == "employee":
            return Employee(
                id=defaults["id"],
                name=defaults["name"],
                department=defaults["department"],
                base_salary=defaults["base_salary"]
            )

    def create_company(self, name: str) -> Company:
        return Company(name)

    def _get_dept_names(self, num: int) -> List[str]:
        possible_names = ["Sales", "Marketing", "Customer Support", "Business Development", "Account Management"]
        return possible_names[:num]

    def _choose_emp_type(self) -> str:
        return random.choices(["salesperson", "manager", "employee"], weights=[80, 15, 5])[0]

    def _get_emp_kwargs(self, emp_type: str) -> Dict[str, Any]:
        if emp_type == "salesperson":
            return {
                "commission_rate": round(random.uniform(0.10, 0.20), 2),  # 10-20%
                "sales_volume": round(random.uniform(40000, 300000), 2)
            }
        elif emp_type == "manager":
            return {"bonus": random.uniform(1000, 3000)}
        return {}
    