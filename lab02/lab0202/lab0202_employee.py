from .lab0202_abstract_employee import AbstractEmployee
from typing import Dict, Any

class Employee(AbstractEmployee):
    def __init__(self, id: int, name: str, department: str, base_salary: float):
        super().__init__(id, name, department, base_salary)

    def calculate_salary(self) -> float:
        return self.base_salary

    def get_info(self) -> str:
        return f"Сотрудник [id: {self.id}, имя: {self.name}, отдел: {self.department}, зарплата: {self.calculate_salary():.2f}]"

    def __str__(self) -> str:
        return self.get_info()
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Employee':
        """Десериализует Employee из словаря"""
        department = data.get('department', '')
        
        salary_value = data.get('base_salary', data.get('salary', 0))
        
        emp = cls(
            id=int(data['id']),
            name=str(data['name']),
            department=department,
            base_salary=float(salary_value)
        )
        return emp