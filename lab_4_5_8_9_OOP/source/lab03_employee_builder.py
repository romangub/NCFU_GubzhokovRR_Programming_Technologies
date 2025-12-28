from typing import List, Optional, Dict, Any
from datetime import datetime
import sys

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab0202_abstract_employee import AbstractEmployee
from source.lab0202_employee import Employee
from source.lab0202_manager import Manager
from source.lab0202_developer import Developer
from source.lab0202_salesperson import Salesperson


class EmployeeBuilder:
    def __init__(self):
        self._reset()

    def _reset(self):
        self._id: Optional[int] = None
        self._name: Optional[str] = None
        self._department: Optional[str] = None
        self._base_salary: Optional[float] = None
        self._bonus: Optional[float] = None
        self._tech_stack: Optional[List[str]] = None
        self._seniority_level: Optional[str] = None
        self._commission_rate: Optional[float] = None
        self._sales_volume: Optional[float] = None

    def with_id(self, emp_id: int) -> 'EmployeeBuilder':
        self._id = emp_id
        return self

    def with_name(self, name: str) -> 'EmployeeBuilder':
        self._name = name.strip()
        return self

    def with_department(self, department: str) -> 'EmployeeBuilder':
        self._department = department.strip()
        return self

    def with_base_salary(self, base_salary: float) -> 'EmployeeBuilder':
        self._base_salary = float(base_salary)
        return self

    def with_bonus(self, bonus: float) -> 'EmployeeBuilder':
        self._bonus = float(bonus)
        return self

    def with_tech_stack(self, tech_stack: List[str]) -> 'EmployeeBuilder':
        self._tech_stack = tech_stack.copy() if tech_stack else []
        return self

    def add_skill(self, skill: str) -> 'EmployeeBuilder':
        if self._tech_stack is None:
            self._tech_stack = []
        self._tech_stack.append(skill)
        return self

    def with_seniority_level(self, level: str) -> 'EmployeeBuilder':
        valid_levels = {"junior", "middle", "senior", "lead"}
        if level.lower() not in valid_levels:
            raise ValueError(f"Недопустимый уровень: {level}. Допустимые: {valid_levels}")
        self._seniority_level = level.lower()
        return self

    def with_commission_rate(self, rate: float) -> 'EmployeeBuilder':
        if not 0 <= rate <= 1:
            raise ValueError("Комиссия должна быть от 0 до 1")
        self._commission_rate = rate
        return self

    def with_sales_volume(self, volume: float) -> 'EmployeeBuilder':
        self._sales_volume = float(volume)
        return self


    def build(self) -> AbstractEmployee:
        if None in (self._id, self._name, self._department, self._base_salary):
            missing = [field for field, value in [
                ("id", self._id),
                ("name", self._name),
                ("department", self._department),
                ("base_salary", self._base_salary)
            ] if value is None]
            raise ValueError(f"Обязательные параметры не указаны: {', '.join(missing)}")

        has_bonus = self._bonus is not None
        has_tech = self._tech_stack is not None or self._seniority_level is not None
        has_commission = self._commission_rate is not None or self._sales_volume is not None

        conflict_count = sum([has_bonus, has_tech, has_commission])
        if conflict_count > 1:
            raise ValueError("Конфликт параметров: указаны поля для разных типов сотрудников")

        if has_tech:
            if self._tech_stack is None:
                self._tech_stack = []
            if self._seniority_level is None:
                self._seniority_level = "middle"  # дефолт
            employee = Developer(
                id=self._id,
                name=self._name,
                department=self._department,
                base_salary=self._base_salary,
                tech_stack=self._tech_stack,
                seniority_level=self._seniority_level
            )
        elif has_bonus:
            if self._bonus is None:
                self._bonus = 0.0
            employee = Manager(
                id=self._id,
                name=self._name,
                department=self._department,
                base_salary=self._base_salary,
                bonus=self._bonus
            )
        elif has_commission:
            commission = self._commission_rate or 0.1
            volume = self._sales_volume or 0.0
            employee = Salesperson(
                id=self._id,
                name=self._name,
                department=self._department,
                base_salary=self._base_salary,
                commission_rate=commission,
                sales_volume=volume
            )
        else:
            employee = Employee(
                id=self._id,
                name=self._name,
                department=self._department,
                base_salary=self._base_salary
            )
        self._reset()

        return employee