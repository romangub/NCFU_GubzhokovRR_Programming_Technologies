from abc import ABC, abstractmethod
from typing import Dict, Any
import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab0202_employee import Employee
from source.lab0202_manager import Manager
from source.lab0202_developer import Developer
from source.lab0202_salesperson import Salesperson

class EmployeeFactory(ABC):
    @abstractmethod
    def create_employee(self, **kwargs) -> Employee:
        pass
    
    @staticmethod
    def _check_params(req_params: list, params: Dict[str, Any]) -> None:
        missing = [p for p in req_params if p not in params]
        if missing:
            raise ValueError(f"Отсутствуют обязательные параметры: {', '.join(missing)}")


class BasicEmployeeFactory(EmployeeFactory): 
    def create_employee(self, **kwargs) -> Employee:
        params = ['id', 'name', 'department', 'base_salary']
        self._check_params(params, kwargs)
        
        return Employee(
            id=kwargs['id'],
            name=kwargs['name'],
            department=kwargs['department'],
            base_salary=kwargs['base_salary']
        )

class ManagerFactory(EmployeeFactory):
    def create_employee(self, **kwargs) -> Manager:
        params = ['id', 'name', 'department', 'base_salary', 'bonus']
        self._check_params(params, kwargs)
        
        return Manager(
            id=kwargs['id'],
            name=kwargs['name'],
            department=kwargs['department'],
            base_salary=kwargs['base_salary'],
            bonus=kwargs['bonus']
        )

class DeveloperFactory(EmployeeFactory):
    def create_employee(self, **kwargs) -> Developer:
        params = ['id', 'name', 'department', 'base_salary', 'tech_stack', 'seniority_level']
        self._check_params(params, kwargs)
        
        return Developer(
            id=kwargs['id'],
            name=kwargs['name'],
            department=kwargs['department'],
            base_salary=kwargs['base_salary'],
            tech_stack=kwargs['tech_stack'],
            seniority_level=kwargs['seniority_level']
        )

class SalespersonFactory(EmployeeFactory):
    def create_employee(self, **kwargs) -> Salesperson:
        params = ['id', 'name', 'department', 'base_salary', 'commission_rate', 'sales_volume']
        self._check_params(params, kwargs)
        
        return Salesperson(
            id=kwargs['id'],
            name=kwargs['name'],
            department=kwargs['department'],
            base_salary=kwargs['base_salary'],
            commission_rate=kwargs['commission_rate'],
            sales_volume=kwargs['sales_volume']
        )