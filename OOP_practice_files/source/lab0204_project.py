import sys
import os
from datetime import datetime, date
from typing import List, Dict, Any, Optional

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/OOP_practice_files")

from source.lab0202_abstract_employee import AbstractEmployee

class Project:
    
    statuses = ["planning", "active", "completed", "cancelled"]
    
    def __init__(self, 
                 project_id: int, 
                 name: str, 
                 description: str = "", 
                 budget: float = 0.0,
                 start_date: date = None,
                 end_date: date = None,
                 status: str = "planning"):
        
        self.project_id = project_id
        self.name = name
        self.description = description
        
        self.start_date = start_date if start_date else date.today()
        self.end_date = end_date if end_date else date.today()
        
        self.budget = budget
        self.status = status
        self.__team: List[AbstractEmployee] = []
        self.created_at = datetime.now()
    
    @property
    def project_id(self) -> int:
        return self.__project_id
    
    @project_id.setter
    def project_id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("ID проекта должен быть положительным целым числом")
        self.__project_id = value
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Название проекта не может быть пустой строкой")
        self.__name = value.strip()
    
    @property
    def description(self) -> str:
        return self.__description
    
    @description.setter
    def description(self, value: str):
        if not isinstance(value, str):
            value = str(value)
        self.__description = value.strip()
    
    @property
    def start_date(self) -> date:
        return self.__start_date
    
    @start_date.setter
    def start_date(self, value: date):
        if not isinstance(value, date):
            raise ValueError("Дата начала должна быть объектом date")
        self.__start_date = value
    
    @property
    def end_date(self) -> date:
        return self.__end_date
    
    @end_date.setter
    def end_date(self, value: date):
        if not isinstance(value, date):
            raise ValueError("Дата окончания должна быть объектом date")
        
        if value < self.start_date:
            raise ValueError("Дата окончания не может быть раньше даты начала")
        
        if value < date.today():
            print(f"Внимание: дата окончания проекта {value} уже прошла")
        
        self.__end_date = value
    
    @property
    def budget(self) -> float:
        return self.__budget
    
    @budget.setter
    def budget(self, value: float):
        if not isinstance(value, (int, float)):
            raise ValueError("Бюджет должен быть числом")
        if value < 0:
            raise ValueError("Бюджет не может быть отрицательным")
        self.__budget = float(value)
    
    @property
    def status(self) -> str:
        return self.__status
    
    @status.setter
    def status(self, value: str):
        if value not in self.statuses:
            raise ValueError(f"Статус должен быть одним из: {', '.join(self.statuses)}")
        self.__status = value
    
    def add_team_member(self, employee: AbstractEmployee) -> None:
        if not isinstance(employee, AbstractEmployee):
            raise TypeError("Можно добавлять только объекты AbstractEmployee")
        
        if any(member.id == employee.id for member in self.__team):
            raise ValueError(f"Сотрудник {employee.name} (ID: {employee.id}) уже в команде проекта")
        
        self.__team.append(employee)
        print(f"Сотрудник {employee.name} добавлен в проект '{self.name}'")
    
    def remove_team_member(self, employee_id: int) -> None:
        initial_size = len(self.__team)
        employee_to_remove = None
        
        for member in self.__team:
            if member.id == employee_id:
                employee_to_remove = member
                break
        
        if employee_to_remove:
            self.__team.remove(employee_to_remove)
            print(f"Сотрудник {employee_to_remove.name} (ID: {employee_id}) удален из проекта '{self.name}'")
        else:
            raise ValueError(f"Сотрудник с ID {employee_id} не найден в команде проекта")
    
    def get_team(self) -> List[AbstractEmployee]:
        return self.__team.copy()
    
    def get_team_size(self) -> int:
        return len(self.__team)
    
    def calculate_total_salary(self) -> float:
        return sum(member.calculate_salary() for member in self.__team)
    
    def get_project_info(self) -> str:
        days_until_end = (self.end_date - date.today()).days
        team_size = self.get_team_size()
        total_salary = self.calculate_total_salary()
        
        info = [
            f"=== ИНФОРМАЦИЯ О ПРОЕКТЕ ===",
            f"ID: {self.project_id}",
            f"Название: {self.name}",
            f"Описание: {self.description}",
            f"Статус: {self.status}",
            f"Бюджет: {self.budget:.2f} руб.",
            f"Период: {self.start_date.strftime('%d.%m.%Y')} - {self.end_date.strftime('%d.%m.%Y')}",
            f"Дней до окончания: {days_until_end}",
            f"Размер команды: {team_size} сотрудников",
            f"Общая зарплата команды: {total_salary:.2f} руб.",
        ]
        
        if team_size > 0:
            info.append(f"\nКоманда проекта:")
            for i, member in enumerate(self.__team, 1):
                info.append(f"  {i}. {member.name} ({member.__class__.__name__}) - {member.calculate_salary():.2f} руб.")
        
        return "\n".join(info)
    
    def change_status(self, new_status: str) -> None:
        if new_status not in self.statuses:
            raise ValueError(f"Статус должен быть одним из: {', '.join(self.statuses)}")
        
        old_status = self.status
        self.status = new_status
        print(f"Статус проекта '{self.name}' изменен: {old_status} → {new_status}")
    
    def get_team_member_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        for member in self.__team:
            if member.id == employee_id:
                return member
        return None
    
    def is_employee_in_project(self, employee_id: int) -> bool:
        return any(member.id == employee_id for member in self.__team)
    
    def clear_team(self) -> None:
        count = len(self.__team)
        self.__team.clear()
        print(f"Команда проекта '{self.name}' очищена. Удалено сотрудников: {count}")
    
    def get_duration_days(self) -> int:
        return (self.end_date - self.start_date).days
    
    def is_active(self) -> bool:
        return self.status == "active" and date.today() <= self.end_date
    
    def is_over_budget(self) -> bool:
        return self.calculate_total_salary() > self.budget
    
    # ===== МАГИЧЕСКИЕ МЕТОДЫ =====
    
    def __str__(self) -> str:
        return f"Project '{self.name}' (ID: {self.project_id}, Status: {self.status}, Team: {self.get_team_size()})"
    
    def __repr__(self) -> str:
        return f"Project(id={self.project_id}, name='{self.name}', status='{self.status}', team_size={self.get_team_size()})"
    
    def __len__(self) -> int:
        return self.get_team_size()
    
    def __contains__(self, employee: AbstractEmployee) -> bool:
        if not isinstance(employee, AbstractEmployee):
            return False
        return self.is_employee_in_project(employee.id)
    
    # ===== СЕРИАЛИЗАЦИЯ =====
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'Project',
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'budget': self.budget,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'status': self.status,
            'team_size': self.get_team_size(),
            'total_salary': self.calculate_total_salary(),
            'duration_days': self.get_duration_days(),
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            'team': [emp.to_dict() for emp in self.__team],
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        if 'type' not in data or data['type'] != 'Project':
            raise ValueError("Некорректный формат данных проекта")
        
        from datetime import datetime
        
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        
        if start_date_str:
            start_date = datetime.fromisoformat(start_date_str).date()
        else:
            start_date = date.today()
        
        if end_date_str:
            end_date = datetime.fromisoformat(end_date_str).date()
        else:
            end_date = date.today()
        
        project = cls(
            project_id=int(data['project_id']),
            name=str(data['name']),
            description=data.get('description', ''),
            budget=float(data.get('budget', 0)),
            start_date=start_date,
            end_date=end_date,
            status=data.get('status', 'planning')
        )
        
        if 'created_at' in data and data['created_at']:
            project.created_at = datetime.fromisoformat(data['created_at'])
        
        from .lab0202_employee import Employee
        from .lab0202_manager import Manager
        from .lab0202_developer import Developer
        from .lab0202_salesperson import Salesperson
        
        employee_classes = {
            'Employee': Employee,
            'Manager': Manager,
            'Developer': Developer,
            'Salesperson': Salesperson
        }
        
        team_data = data.get('team', [])
        successful = 0
        failed = 0
        
        for emp_data in team_data:
            try:
                emp_type = emp_data.get('type', 'Employee')
                
                if emp_type in employee_classes:
                    employee_class = employee_classes[emp_type]
                    employee = employee_class.from_dict(emp_data)
                    # Используем внутренний список, чтобы избежать проверок дублирования
                    project._Project__team.append(employee)
                    successful += 1
                else:
                    print(f"Неизвестный тип сотрудника в проекте: {emp_type}")
                    failed += 1
            except Exception as e:
                print(f"Ошибка добавления сотрудника в проект: {e}")
                failed += 1
        
        if failed > 0:
            print(f"Успешно загружено: {successful}, не удалось: {failed}")
        
        return project
    
    def save_to_file(self, filename: str) -> None:
        """Сохранить проект в файл"""
        data = self.to_dict()
        
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Проект '{self.name}' сохранен в файл: {filename}")
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'Project':
        import json
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return cls.from_dict(data)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filename} не найден")
        except json.JSONDecodeError as e:
            raise ValueError(f"Некорректный JSON формат: {e}")
        except Exception as e:
            raise ValueError(f"Ошибка при загрузке проекта: {e}")