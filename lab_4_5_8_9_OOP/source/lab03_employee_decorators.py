from typing import List, Dict, Any
import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab0202_abstract_employee import AbstractEmployee

class EmployeeDecorator(AbstractEmployee):
    def __init__(self, employee: AbstractEmployee):
        self._employee = employee
    
    def calculate_salary(self) -> float:
        return self._employee.calculate_salary()
    
    def get_info(self) -> str:
        return self._employee.get_info()
    
    @property
    def id(self) -> int:
        return self._employee.id
    
    @property
    def name(self) -> str:
        return self._employee.name
    
    @property
    def department(self) -> str:
        return self._employee.department
    
    @property
    def base_salary(self) -> float:
        return self._employee.base_salary
    
    @property
    def salary(self) -> float:
        return self._employee.salary
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AbstractEmployee':
        return AbstractEmployee.from_dict(data)
    
    def to_dict(self) -> dict:
        return self._employee.to_dict()
    
    def __str__(self) -> str:
        return str(self._employee)
    
    def __repr__(self) -> str:
        return repr(self._employee)


class BonusDecorator(EmployeeDecorator):
    def __init__(self, employee: AbstractEmployee, fixed_bonus: float = 0.0, percent_bonus: float = 0.0):
        super().__init__(employee)
        self._fixed_bonus = fixed_bonus
        self._percent_bonus = percent_bonus
    
    def calculate_salary(self) -> float:
        original = self._employee.calculate_salary()
        bonus = self._fixed_bonus + (original * self._percent_bonus)
        return original + bonus
    
    def get_info(self) -> str:
        original_info = self._employee.get_info()
        bonus_amount = self._fixed_bonus + (self._employee.calculate_salary() * self._percent_bonus)
        return f"{original_info} | Бонус: +{bonus_amount:.2f}"


class TrainingDecorator(EmployeeDecorator):

    def __init__(self, employee: AbstractEmployee, training_name: str, salary_increase_percent: float = 0.10):
        super().__init__(employee)
        self.training_name = training_name
        self._salary_increase = salary_increase_percent
    
    def calculate_salary(self) -> float:
        original = self._employee.calculate_salary()
        return original * (1 + self._salary_increase)
    
    def get_info(self) -> str:
        original_info = self._employee.get_info()
        increase = self._salary_increase * 100
        return f"{original_info} | Прошёл тренинг: '{self.training_name}' (+{increase:.0f}% к зарплате)"
    
    def has_training(self) -> bool:
        return True