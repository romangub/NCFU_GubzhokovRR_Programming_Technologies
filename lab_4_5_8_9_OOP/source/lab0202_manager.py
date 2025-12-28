import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab0202_employee import Employee
from typing import Dict, Any

class Manager(Employee):
    
    def __init__(self, 
                 id: int,
                 name: str,
                 department: str,
                 base_salary: float,
                 bonus: float):
        super().__init__(id, name, department, base_salary)
        self.bonus = bonus
    
    @property
    def bonus(self) -> float:
        return self.__bonus
    
    @bonus.setter
    def bonus(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError("Бонус должен быть числом.")
        if value < 0:
            raise ValueError("Бонус должен быть неотрицательным числом.")
        self.__bonus = float(value)
    
    def get_info(self) -> str:
        return (f"Менеджер [id: {self.id}, имя: {self.name}, отдел: {self.department}, "
                f"базовая зарплата: {self.base_salary:.2f}, бонус: {self.bonus:.2f}, "
                f"итоговая зарплата: {self.calculate_salary():.2f}]")
    
    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data['bonus'] = self.bonus
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Manager':
        id_val = int(data['id'])
        name_val = str(data['name'])
        department_val = data.get('department', '')
        
        base_salary_val = data.get('base_salary', data.get('salary', 0))
        base_salary_val = float(base_salary_val)
        
        bonus_val = data.get('bonus', 0)
        bonus_val = float(bonus_val)
        
        manager = cls(
            id=id_val,
            name=name_val,
            department=department_val,
            base_salary=base_salary_val,
            bonus=bonus_val
        )
        
        return manager
    
    def __str__(self) -> str:
        return f"Manager {self.name} (Bonus: {self.bonus:.2f})"
    
    def __repr__(self) -> str:
        return f"Manager(id={self.id}, name='{self.name}', department='{self.department}', bonus={self.bonus})"