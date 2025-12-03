import json
from typing import Dict, Any
from abc import ABC, abstractmethod

class AbstractEmployee(ABC):
    
    def __init__(self, id: int, name: str, department: str, base_salary: float):
        self.id = id  # @id.setter
        self.name = name  # @name.setter
        self.department = department  # @department.setter
        self.base_salary = base_salary  # @base_salary.setter
    
    @abstractmethod
    def calculate_salary(self) -> float:
        pass
    
    @abstractmethod
    def get_info(self) -> str:
        pass
    

    @staticmethod
    def from_dict(data: dict) -> 'AbstractEmployee':
        class_name = data.get('type') or data.get('class_name')
        
        if class_name == 'Employee':
            from .lab0202_employee import Employee
            return Employee.from_dict(data)
        elif class_name == 'Manager':
            from .lab0202_manager import Manager
            return Manager.from_dict(data)
        elif class_name == 'Developer':
            from .lab0202_developer import Developer
            return Developer.from_dict(data)
        elif class_name == 'Salesperson':
            from .lab0202_salesperson import Salesperson
            return Salesperson.from_dict(data)
        else:
            raise ValueError(f"Неизвестный класс сотрудника: {class_name}")
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, AbstractEmployee):
            return False
        return self.id == other.id
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, AbstractEmployee):
            return NotImplemented
        return self.calculate_salary() < other.calculate_salary()
    
    def __add__(self, other) -> float:
        if isinstance(other, AbstractEmployee):
            return self.calculate_salary() + other.calculate_salary()
        elif isinstance(other, (int, float)):
            return self.calculate_salary() + other
        return NotImplemented
    
    def __radd__(self, other) -> float:
        if other == 0:
            return self.calculate_salary()
        elif isinstance(other, (int, float)):
            return other + self.calculate_salary()
        return NotImplemented
    
    def __str__(self) -> str:
        return f"{self.name} (ID: {self.id}, Отдел: {self.department})"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}', salary={self.base_salary})"
    
    # === СВОЙСТВА ===
    
    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID должен быть положительным целым числом.")
        self.__id = value
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Имя не может быть пустой строкой.")
        self.__name = value.strip()
    
    @property
    def department(self) -> str:
        return self.__department
    
    @department.setter
    def department(self, value: str) -> None:
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Название отдела не может быть пустой строкой.")
        self.__department = value.strip()
    
    @property
    def base_salary(self) -> float:
        return self.__base_salary
    
    @base_salary.setter
    def base_salary(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError("Зарплата должна быть числом.")
        if value < 0:
            raise ValueError("Зарплата не может быть отрицательной.")
        self.__base_salary = float(value)
    
    @property
    def salary(self) -> float:
        return self.base_salary
    
    # === МЕТОД СЕРИАЛИЗАЦИИ ===
    
    def to_dict(self) -> Dict[str, Any]:
        """Полная сериализация сотрудника в словарь"""
        return {
            'type': self.__class__.__name__,
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'base_salary': float(self.base_salary),
            'calculated_salary': float(self.calculate_salary())
        }
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AbstractEmployee':
        pass