import random
import sys
from datetime import date, timedelta
from typing import Dict, Any, List

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab0204_company import Company
from source.lab0203_department import Department
from source.lab0204_project import Project
from source.lab0202_abstract_employee import AbstractEmployee
from source.lab0202_manager import Manager
from source.lab0202_developer import Developer
from source.lab0202_employee import Employee 

from source.lab03_abstract_сompany_factory import AbstractCompanyFactory


class TechCompanyFactory(AbstractCompanyFactory):

    def create_department(self, name: str) -> Department:
        """Создаёт обычный отдел (можно добавить логику позже)."""
        return Department(name)

    def create_project(self, 
                       project_id: int, 
                       name: str, 
                       description: str = "", 
                       budget: float = 500000.0,
                       start_date: date = None,
                       end_date: date = None,
                       status: str = "active") -> Project:
        if description == "":
            description = f"Разработка {name} на современном стеке (Python, React и т.д.)"
        if start_date is None:
            start_date = date.today()
        if end_date is None:
            end_date = start_date + timedelta(days=180)
        
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
        if emp_type not in ["developer", "manager"]:
            raise ValueError(f"TechCompanyFactory поддерживает только 'developer' и 'manager', получено: {emp_type}")
        
        defaults = {
            "id": kwargs.get("id", 1),
            "name": kwargs.get("name", "Unnamed Developer"),
            "department": kwargs.get("department", "Development"),
            "base_salary": kwargs.get("base_salary", 6000.0)
        }
        defaults.update(kwargs)
        
        if emp_type == "developer":
            return Developer(
                id=defaults["id"],
                name=defaults["name"],
                department=defaults["department"],
                base_salary=defaults["base_salary"],
                tech_stack=defaults.get("tech_stack", ["Python", "JavaScript", "Docker"]),
                seniority_level=defaults.get("seniority_level", "middle")
            )
        elif emp_type == "manager":
            return Manager(
                id=defaults["id"],
                name=defaults["name"],
                department=defaults["department"],
                base_salary=defaults["base_salary"],
                bonus=defaults.get("bonus", 2500.0)
            )

    def create_company(self, name: str) -> Company:
        return Company(name)

    def _get_dept_names(self, num: int) -> List[str]:
        possible_names = ["Development", "QA", "DevOps", "Architecture", "Data Science"]
        return possible_names[:num]

    def _choose_emp_type(self) -> str:
        return random.choices(["developer", "manager"], weights=[80, 20])[0]

    def _get_emp_kwargs(self, emp_type: str) -> Dict[str, Any]:
        if emp_type == "developer":
            tech_stacks = [
                ["Python", "Django", "FastAPI"],
                ["JavaScript", "React", "Node.js"],
                ["Go", "Kubernetes", "AWS"],
                ["Java", "Spring", "Microservices"]
            ]
            return {
                "tech_stack": random.choice(tech_stacks),
                "seniority_level": random.choice(["junior", "middle", "senior"])
            }
        elif emp_type == "manager":
            return {"bonus": random.uniform(1500, 4000)}
        return {}