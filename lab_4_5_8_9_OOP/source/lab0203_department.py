import sys
import json
import os
from typing import Optional, List, Dict, Any

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP")

from source.lab0202_abstract_employee import AbstractEmployee

class Department:
    
    def __init__(self, name: str):
        if not name or not isinstance(name, str) or name.strip() == "":
            raise ValueError("Название отдела не может быть пустой строкой")
        self.name = name.strip()
        self.emp_list: List[AbstractEmployee] = []
        
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Название отдела должно быть непустой строкой")
        self.__name = value
        
    def __iter__(self) -> List[AbstractEmployee]:
        return iter(self.emp_list)
    
    def __len__(self) -> int:
        return len(self.emp_list)
    
    def __getitem__(self, key) -> AbstractEmployee:
        if isinstance(key, int):
            return self.emp_list[key]
        elif isinstance(key, slice):
            return self.emp_list[key]
        else:
            raise TypeError("Индекс должен быть целым числом или срезом")
    
    def __contains__(self, employee: AbstractEmployee) -> bool:
        if not isinstance(employee, AbstractEmployee):
            return False
        return any(emp.id == employee.id for emp in self.emp_list)
    
    def __str__(self) -> str:
        return f"Department '{self.name}' ({len(self)} сотрудников)"
    
    def __repr__(self) -> str:
        return f"Department(name='{self.name}', employees={len(self)})"
        
    def add_employee(self, employee: AbstractEmployee) -> None:
        """Добавить сотрудника в отдел"""
        if not isinstance(employee, AbstractEmployee):
            raise TypeError("Можно добавлять только объекты AbstractEmployee")
        
        # Проверяем уникальность ID
        if any(emp.id == employee.id for emp in self.emp_list):
            raise ValueError(
                f'Сотрудник {employee.name} (ID: {employee.id}) '
                f'уже находится в отделе "{self.name}"'
            )
        
        # Устанавливаем отдел сотруднику
        employee.department = self.name
        self.emp_list.append(employee)
        
    def add_employee_direct(self, employee: AbstractEmployee) -> None:
        """Прямое добавление сотрудника без проверок (для загрузки из файла)"""
        employee.department = self.name
        self.emp_list.append(employee)
    
    def remove_employee(self, employee_id: int) -> None:
        """Удалить сотрудника по ID"""
        initial_count = len(self.emp_list)
        employee_to_remove = None
        
        # Находим сотрудника
        for emp in self.emp_list:
            if emp.id == employee_id:
                employee_to_remove = emp
                break
        
        if employee_to_remove:
            self.emp_list.remove(employee_to_remove)
            print(f"Сотрудник {employee_to_remove.name} (ID: {employee_id}) удален из отдела '{self.name}'")
        else:
            raise ValueError(f'В отделе "{self.name}" нет сотрудника с ID = {employee_id}')
    
    def get_employees(self) -> List[Dict[str, Any]]:
        """Получить список сотрудников в виде словарей"""
        return [
            {
                "Name": emp.name,
                "ID": emp.id,
                "Department": emp.department,
                "Base Salary": emp.base_salary,
                "Calculated Salary": emp.calculate_salary(),
                "Type": emp.__class__.__name__
            }
            for emp in self.emp_list
        ]
    
    def calculate_total_salary(self) -> float:
        """Рассчитать общую зарплату всех сотрудников отдела"""
        return sum(emp.calculate_salary() for emp in self.emp_list)
    
    def get_employee_count(self) -> Dict[str, int]:
        """Получить статистику по типам сотрудников"""
        count_dict = {}
        for emp in self.emp_list:
            emp_type = emp.__class__.__name__
            count_dict[emp_type] = count_dict.get(emp_type, 0) + 1
        return count_dict
    
    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Найти сотрудника по ID"""
        for emp in self.emp_list:
            if emp.id == employee_id:
                return emp
        return None
    
    def save_to_file(self, filename: str) -> None:
        """Сохранить отдел в файл"""
        data = self.to_dict()
        
        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Отдел '{self.name}' сохранен в файл: {filename}")
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'Department':
        """Загрузить отдел из файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return cls.from_dict(data)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filename} не найден")
        except KeyError as e:
            raise ValueError(f"Некорректный формат файла: отсутствует ключ {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Некорректный JSON формат: {e}")
        except Exception as e:
            raise ValueError(f"Ошибка при загрузке файла: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Полная сериализация отдела в словарь"""
        return {
            'type': 'Department',
            'name': self.name,
            'employee_count': len(self.emp_list),
            'total_salary': self.calculate_total_salary(),
            'employees': [emp.to_dict() for emp in self.emp_list]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Department':
        if 'type' not in data or data['type'] != 'Department':
            raise ValueError("Некорректный формат данных отдела")
        
        if 'name' not in data:
            raise ValueError("Отсутствует название отдела")
        
        department = cls(data['name'])
        
        # Импортируем здесь, чтобы избежать циклических импортов
        from source.lab0202_employee import Employee
        from source.lab0202_manager import Manager
        from source.lab0202_developer import Developer
        from source.lab0202_salesperson import Salesperson
        
        employee_classes = {
            'Employee': Employee,
            'Manager': Manager,
            'Developer': Developer,
            'Salesperson': Salesperson
        }
        
        # Восстанавливаем сотрудников
        employees_data = data.get('employees', [])
        successful = 0
        failed = 0
        
        for emp_data in employees_data:
            try:
                emp_type = emp_data.get('type', 'Employee')
                
                if emp_type in employee_classes:
                    employee_class = employee_classes[emp_type]
                    employee = employee_class.from_dict(emp_data)
                    department.add_employee_direct(employee)  # ← используем прямой метод
                    successful += 1
                else:
                    print(f"Неизвестный тип сотрудника: {emp_type}")
                    failed += 1
            except Exception as e:
                print(f"Ошибка создания сотрудника: {e}")
                failed += 1
        
        if failed > 0:
            print(f"Успешно загружено: {successful}, не удалось: {failed}")
        
        return department
    
    # @classmethod
    # def from_dict(cls, data: Dict[str, Any]) -> 'Department':
    #     """Десериализация отдела из словаря"""
    #     print(f"\n>>> Department.from_dict: начало для отдела '{data.get('name')}'")
        
    #     if 'type' not in data or data['type'] != 'Department':
    #         raise ValueError("Некорректный формат данных отдела")
        
    #     if 'name' not in data:
    #         raise ValueError("Отсутствует название отдела")
        
    #     department = cls(data['name'])
    #     print(f">>> Создан объект отдела '{department.name}'")
        
    #     # Восстанавливаем сотрудников
    #     employees_data = data.get('employees', [])
    #     print(f">>> Всего сотрудников в данных: {len(employees_data)}")
        
    #     if len(employees_data) > 0:
    #         print(f">>> Первый сотрудник в данных: {employees_data[0]}")
        
    #     for i, emp_data in enumerate(employees_data):
    #         print(f"\n>>> Обработка сотрудника {i+1}/{len(employees_data)}:")
    #         print(f">>>   Данные: ID={emp_data.get('id')}, Имя={emp_data.get('name')}, Тип={emp_data.get('type')}")
            
    #         try:
    #             emp_type = emp_data.get('type', 'Employee')
                
    #             if emp_type == 'Employee':
    #                 from source.lab0202_employee import Employee
    #                 employee_class = Employee
    #             elif emp_type == 'Manager':
    #                 from source.lab0202_manager import Manager
    #                 employee_class = Manager
    #             elif emp_type == 'Developer':
    #                 from source.lab0202_developer import Developer
    #                 employee_class = Developer
    #             elif emp_type == 'Salesperson':
    #                 from source.lab0202_salesperson import Salesperson
    #                 employee_class = Salesperson
    #             else:
    #                 print(f">>>   Неизвестный тип сотрудника: {emp_type}")
    #                 continue
                
    #             print(f">>>   Создаем объект класса {employee_class.__name__}...")
    #             employee = employee_class.from_dict(emp_data)
    #             print(f">>>   Сотрудник создан: ID={employee.id}, Имя={employee.name}")
    #             print(f">>>   Отдел сотрудника до добавления: '{employee.department}'")
    #             print(f">>>   Тип объекта: {type(employee)}")
                
    #             # Прямое добавление без проверок
    #             print(f">>>   Прямое добавление в emp_list...")
    #             employee.department = department.name
    #             department.emp_list.append(employee)
    #             print(f">>>   Успешно добавлен. emp_list теперь: {len(department.emp_list)} сотрудников")
                
    #         except Exception as e:
    #             print(f">>>   ОШИБКА: {e}")
    #             import traceback
    #             traceback.print_exc()
        
    #     print(f">>> Department.from_dict: завершено. В отделе {len(department.emp_list)} сотрудников")
    #     return department
    
    def get_statistics(self) -> Dict[str, Any]:
        total_salary = self.calculate_total_salary()
        avg_salary = total_salary / len(self.emp_list) if self.emp_list else 0
        
        return {
            'department_name': self.name,
            'total_employees': len(self.emp_list),
            'employee_types': self.get_employee_count(),
            'total_monthly_salary': total_salary,
            'average_salary': avg_salary,
            'min_salary': min((emp.calculate_salary() for emp in self.emp_list), default=0),
            'max_salary': max((emp.calculate_salary() for emp in self.emp_list), default=0)
        }
    
    def clear(self) -> None:
        """Очистить отдел (удалить всех сотрудников)"""
        count = len(self.emp_list)
        self.emp_list.clear()
        print(f"Отдел '{self.name}' очищен. Удалено сотрудников: {count}")
    
    def transfer_employee_to(self, employee_id: int, target_department: 'Department') -> None:
        """Перевести сотрудника в другой отдел"""
        employee = self.find_employee_by_id(employee_id)
        if not employee:
            raise ValueError(f"Сотрудник с ID {employee_id} не найден в отделе '{self.name}'")
        
        # Удаляем из текущего отдела
        self.remove_employee(employee_id)
        
        # Добавляем в целевой отдел
        try:
            target_department.add_employee(employee)
            print(f"Сотрудник {employee.name} переведен из '{self.name}' в '{target_department.name}'")
        except Exception as e:
            # Если не удалось добавить в целевой отдел, возвращаем обратно
            self.add_employee(employee)
            raise ValueError(f"Не удалось перевести сотрудника: {e}")