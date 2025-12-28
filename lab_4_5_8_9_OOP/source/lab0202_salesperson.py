import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab0202_employee import Employee
from typing import Dict, Any

class Salesperson(Employee):
    
    def __init__(self, 
                 id: int, 
                 name: str, 
                 department: str, 
                 base_salary: float, 
                 commission_rate: float, 
                 sales_volume: float):
        super().__init__(id, name, department, base_salary)
        self.commission_rate = commission_rate
        self.sales_volume = sales_volume
    
    @property
    def commission_rate(self) -> float:
        return self.__commission_rate
    
    @commission_rate.setter
    def commission_rate(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError("Процент комиссии должен быть числом.")
        value = float(value)
        if value < 0 or value > 1:
            raise ValueError("Процент комиссии должен быть в диапазоне от 0 до 1 включительно.")
        self.__commission_rate = value
    
    @property
    def sales_volume(self) -> float:
        return self.__sales_volume
    
    @sales_volume.setter
    def sales_volume(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise ValueError("Объем продаж должен быть числом.")
        value = float(value)
        if value < 0:
            raise ValueError("Объем продаж должен быть неотрицательным числом.")
        self.__sales_volume = value
    
    def update_sales(self, amount: float) -> None:
        if not isinstance(amount, (int, float)):
            raise ValueError("Изменение объёма продаж должно быть числом.")
        new_volume = self.sales_volume + amount
        if new_volume < 0:
            raise ValueError(
                f"Объём продаж не может быть отрицательным. "
                f"Текущий: {self.sales_volume:.2f}, изменение: {amount:.2f}"
            )
        self.sales_volume = new_volume
        
    def calculate_salary(self) -> float:
        return self.base_salary + (self.sales_volume * self.commission_rate)
    
    def get_info(self) -> str:
        return (f"Продавец [id: {self.id}, имя: {self.name}, отдел: {self.department}, "
                f"базовая зарплата: {self.base_salary:.2f}, процент комиссии: {self.commission_rate:.1%}, "
                f"объём продаж: {self.sales_volume:.2f}, итоговая зарплата: {self.calculate_salary():.2f}]")
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            'commission_rate': self.commission_rate,
            'sales_volume': self.sales_volume,
            'commission_earned': self.sales_volume * self.commission_rate  # Добавляем для информации
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Salesperson':
        id_val = int(data['id'])
        name_val = str(data['name'])
        department_val = data.get('department', '')
        
        base_salary_val = data.get('base_salary', data.get('salary', 0))
        base_salary_val = float(base_salary_val)
        
        commission_rate_val = data.get('commission_rate', 0.0)
        commission_rate_val = float(commission_rate_val)
        
        sales_volume_val = data.get('sales_volume', 0.0)
        sales_volume_val = float(sales_volume_val)
        
        salesperson = cls(
            id=id_val,
            name=name_val,
            department=department_val,
            base_salary=base_salary_val,
            commission_rate=commission_rate_val,
            sales_volume=sales_volume_val
        )
        
        return salesperson
    
    def __str__(self) -> str:
        return f"Salesperson {self.name} (Sales: {self.sales_volume:.2f}, Commission: {self.commission_rate:.1%})"
    
    def __repr__(self) -> str:
        return (f"Salesperson(id={self.id}, name='{self.name}', "
                f"commission={self.commission_rate}, sales={self.sales_volume})")