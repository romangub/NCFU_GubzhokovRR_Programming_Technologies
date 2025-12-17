from abc import ABC, abstractmethod
from typing import Dict, Any
import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/OOP_practice_files")

from source.lab0202_abstract_employee import AbstractEmployee
from mock_systems.lab03_external_payroll import PayrollSystem

class SalaryCalc(ABC):
    @abstractmethod
    def calculate_salary(self, employee: AbstractEmployee) -> float:
        pass
    
class PayrollAdapter(SalaryCalc):
    def __init__(self, legacy_system: PayrollSystem = None):
        self.legacy_system = legacy_system or PayrollSystem()
        
    def calculate_salary(self, emp: AbstractEmployee) -> float:
        hourly_rate = emp.base_salary / 160.0
        
        emp_data: Dict[str, Any] = {
            "hourly_rate": hourly_rate,
            "hours_worked": 160.0,
            "overtime_hours": 0.0,
        }
        
        if hasattr(emp, "bonus"):
            emp_data["bonus"] = getattr(emp, "bonus", 0.0)
            
        if hasattr(emp, "sales_volume") and hasattr(emp, "commission_rate"):  # Salesperson
            commission = emp.sales_volume * emp.commission_rate
            emp_data["bonus"] = emp_data.get("bonus", 0.0) + commission
        
        return self.legacy_system.calculate_payroll(emp_data)