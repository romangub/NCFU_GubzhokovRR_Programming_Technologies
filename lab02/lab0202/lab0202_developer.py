from .lab0202_employee import Employee
from typing import Dict, Any, List

class Developer(Employee):
    
    def __init__(self,
                 id: int,
                 name: str,
                 department: str,
                 base_salary: float, 
                 tech_stack: List[str],
                 seniority_level: str):
        super().__init__(id, name, department, base_salary)
        self.tech_stack = tech_stack
        self.seniority_level = seniority_level
        
    @property
    def tech_stack(self) -> List[str]:
        return self.__tech_stack
        
    @tech_stack.setter
    def tech_stack(self, value: List[str]) -> None:
        if not isinstance(value, list):
            raise ValueError("Компетенции должны быть списком")
        if len(value) == 0:
            raise ValueError("Компетенции должны быть непустым списком")
        if not all(isinstance(item, str) for item in value):
            raise ValueError("Все элементы tech_stack должны быть строками")
        self.__tech_stack = [item.strip() for item in value if item.strip()]
            
    @property
    def seniority_level(self) -> str:
        return self.__seniority_level
        
    @seniority_level.setter
    def seniority_level(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Уровень разработчика должен быть строкой")
        value = value.lower().strip()
        valid_levels = ["junior", "middle", "senior"]
        if value not in valid_levels:
            raise ValueError(f'Уровень разработчика должен быть одним из: {", ".join(valid_levels)}')
        self.__seniority_level = value
    
    @property
    def seniority_coefficient(self) -> float:
        table = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
        return table[self.seniority_level]
    
    def __iter__(self):
        return iter(self.tech_stack)
    
    def add_skill(self, new_skill: str) -> None:
        if not isinstance(new_skill, str) or new_skill.strip() == "":
            raise ValueError("Технология должна быть непустой строкой")
        new_skill = new_skill.strip()
        if new_skill not in self.tech_stack:
            self.tech_stack.append(new_skill)
    
    def calculate_salary(self) -> float:
        return self.base_salary * self.seniority_coefficient
    
    def get_info(self) -> str:
        return (f"Разработчик [id: {self.id}, имя: {self.name}, отдел: {self.department}, "
                f"базовая зарплата: {self.base_salary}, компетенции: {', '.join(self.tech_stack)}, "
                f"уровень: {self.seniority_level}, итоговая зарплата: {self.calculate_salary():.2f}]")
    
    def to_dict(self) -> Dict[str, Any]:
        """Полная сериализация Developer в словарь"""
        data = super().to_dict()
        data.update({
            'tech_stack': self.tech_stack.copy(),
            'seniority_level': self.seniority_level,
            'seniority_coefficient': self.seniority_coefficient
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Developer':
        """Десериализует Developer из словаря"""
        id_val = data['id']
        name_val = data['name']
        department_val = data.get('department', '')
        base_salary_val = data.get('base_salary', data.get('salary', 0))
        
        tech_stack_val = data.get('tech_stack', [])
        seniority_level_val = data.get('seniority_level', 'junior')  # Значение по умолчанию
        
        developer = cls(
            id=id_val,
            name=name_val,
            department=department_val,
            base_salary=base_salary_val,
            tech_stack=tech_stack_val,
            seniority_level=seniority_level_val
        )
        
        return developer
    
    def __str__(self) -> str:
        return f"Developer {self.name} ({self.seniority_level}) - {', '.join(self.tech_stack[:3])}{'...' if len(self.tech_stack) > 3 else ''}"
    
    def __repr__(self) -> str:
        return f"Developer(id={self.id}, name='{self.name}', level='{self.seniority_level}', skills={len(self.tech_stack)})"