from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime, date
import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab0202_abstract_employee import AbstractEmployee
from source.lab0203_department import Department
from source.lab0204_project import Project
from source.lab0204_company import Company

class AbstractCompanyFactory(ABC):
    
    @abstractmethod
    def create_department(self, name: str) -> Department:
        pass
    
    @abstractmethod
    def create_project(self, 
                 project_id: int, 
                 name: str, 
                 description: str = "", 
                 budget: float = 0.0,
                 start_date: date = None,
                 end_date: date = None,
                 status: str = "planning") -> Project:
        pass
    
    @abstractmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        pass
    
    @abstractmethod
    def create_company(name: str) -> Company:
        pass
    
    def build_company(self, name: str, num_depts: int = 2, num_employees_per_dept: int = 3, num_projects: int = 1) -> Company:
        company = self.create_company(name)

        dept_names = self._get_dept_names(num_depts)
        for dept_name in dept_names:
            dept = self.create_department(dept_name)
            company.add_department(dept)
            
            for i in range(num_employees_per_dept):
                emp_type = self._choose_emp_type()
                emp = self.create_employee(emp_type, id=i+1, name=f"Employee {i+1}", department=dept_name, base_salary=5000.0, **self._get_emp_kwargs(emp_type))
                dept.add_employee(emp)
                
        for i in range(num_projects):
            proj = self.create_project(project_id=i+1, name=f"Project {i+1}", budget=100000.0)
            company.add_project(proj)
            
            employees = company.get_all_employees()
            if employees:
                proj.add_team_member(employees[0])
        
        return company
    
    def _get_dept_names(self, num: int) -> list[str]:
        raise NotImplementedError("Должен быть реализован в подклассах")

    def _choose_emp_type(self) -> str:
        raise NotImplementedError("Должен быть реализован в подклассах")

    def _get_emp_kwargs(self, emp_type: str) -> Dict[str, Any]:
        return {}