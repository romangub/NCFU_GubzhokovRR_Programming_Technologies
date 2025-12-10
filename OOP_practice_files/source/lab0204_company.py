import sys
import os
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import sqlite3

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/OOP_practice_files/source")

from lab0203_department import Department
from lab0204_project import Project
from lab0202_abstract_employee import AbstractEmployee
from lab0202_employee import Employee
from lab0202_manager import Manager
from lab0202_developer import Developer
from lab0202_salesperson import Salesperson
from lab0204_errors import EmployeeNotFoundError
from lab0204_errors import DepartmentNotFoundError
from lab0204_errors import ProjectNotFoundError
from lab0204_errors import InvalidStatusError
from lab0204_errors import DuplicateIdError
from lab03_singleton import DatabaseConnection

class Company:
    MIN_PROJECT_BUDGET = 1000.0
    MAX_PROJECT_BUDGET = 10_000_000.0
    MIN_EMPLOYEE_SALARY = 0.0
    MAX_EMPLOYEE_SALARY = 1_000_000.0
    
    def __init__(self, name: str):
        self.name = name  # Вызывает сеттер
        self.__departments: List[Department] = []  
        self.__projects: List[Project] = []
        self.__employee_ids: Dict[int, str] = {}
        self.__project_ids: Dict[int, bool] = {}
    
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Название компании не может быть пустой строкой")
        self.__name = value.strip()
    
    # === ВАЛИДАЦИОННЫЕ МЕТОДЫ ===
    
    def __validate_department_exists(self, department_name: str) -> None:
        if not any(dept.name == department_name for dept in self.__departments):
            raise DepartmentNotFoundError(department_name)
    
    def __validate_employee_id_unique(self, employee_id: int, department_name: str = None) -> None:
        if employee_id in self.__employee_ids:
            if department_name and self.__employee_ids[employee_id] != department_name:
                return
            raise DuplicateIdError(str(employee_id))
    
    def __validate_project_id_unique(self, project_id: int) -> None:
        if project_id in self.__project_ids:
            raise ValueError(f"Проект с ID {project_id} уже существует в компании")
    
    def __validate_project_status(self, status: str, project_name: str = "") -> None:
        if status not in Project.statuses:
            if project_name:
                raise InvalidStatusError(project_name, status)
            else:
                raise InvalidStatusError("unknown", status)
    
    def __validate_project_dates(self, start_date: date, end_date: date) -> None:
        if not isinstance(start_date, date) or not isinstance(end_date, date):
            raise TypeError("Даты должны быть объектами datetime.date")
        if start_date >= end_date:
            raise ValueError(f"Дата начала ({start_date}) должна быть раньше даты окончания ({end_date})")
        if end_date < date.today():
            raise ValueError(f"Дата окончания проекта ({end_date}) не может быть в прошлом")
    
    def __validate_project_budget(self, budget: float) -> None:
        if not isinstance(budget, (int, float)):
            raise TypeError("Бюджет должен быть числом")
        if budget < self.MIN_PROJECT_BUDGET:
            raise ValueError(f"Бюджет проекта не может быть меньше {self.MIN_PROJECT_BUDGET}")
        if budget > self.MAX_PROJECT_BUDGET:
            raise ValueError(f"Бюджет проекта не может превышать {self.MAX_PROJECT_BUDGET}")
    
    def __validate_employee_salary(self, salary: float) -> None:
        if not isinstance(salary, (int, float)):
            raise TypeError("Зарплата должна быть числом")
        if salary < self.MIN_EMPLOYEE_SALARY:
            raise ValueError(f"Зарплата не может быть отрицательной")
        if salary > self.MAX_EMPLOYEE_SALARY:
            raise ValueError(f"Зарплата не может превышать {self.MAX_EMPLOYEE_SALARY}")
    
    # ============================
    
    def add_department(self, department: Department) -> None:
        pass
        
        if any(dept.name == department.name for dept in self.__departments):
            raise ValueError(f"Отдел '{department.name}' уже существует в компании")
        
        # Валидируем ID сотрудников перед добавлением
        for employee in department.emp_list:
            try:
                self.__validate_employee_id_unique(employee.id, department.name)
                self.__employee_ids[employee.id] = department.name
            except DuplicateIdError as e:
                # Откатываем уже добавленных сотрудников
                for added_id in list(self.__employee_ids.keys()):
                    if self.__employee_ids.get(added_id) == department.name:
                        del self.__employee_ids[added_id]
                raise e
        
        self.__departments.append(department)
        print(f"Отдел '{department.name}' добавлен в компанию '{self.name}'")
    
    def remove_department(self, department_name: str) -> None:
        self.__validate_department_exists(department_name)
        department = self.get_department(department_name)
        
        if len(department) > 0:
            raise ValueError(f"Невозможно удалить отдел '{department_name}', в котором находятся сотрудники")
        
        for emp in department.emp_list:
            if emp.id in self.__employee_ids:
                del self.__employee_ids[emp.id]
        
        self.__departments = [dept for dept in self.__departments if dept.name != department_name]
        print(f"Отдел '{department_name}' удален из компании '{self.name}'")
    
    def get_department(self, department_name: str) -> Department:
        for department in self.__departments:
            if department.name == department_name:
                return department
        raise DepartmentNotFoundError(department_name)
    
    def get_departments(self):
        return self.__departments
    
    def clear_departments(self):
        self.__departments.clear()
        return True
    
    def add_project(self, project) -> None:
        required_attrs = ['project_id', 'name', 'budget', 'start_date', 'end_date', 'status']
        for attr in required_attrs:
            if not hasattr(project, attr):
                raise TypeError(f"Объект не имеет атрибута '{attr}', не является проектом")
        
        self.__validate_project_id_unique(project.project_id)
        self.__validate_project_status(project.status, project.name)
        self.__validate_project_dates(project.start_date, project.end_date)
        self.__validate_project_budget(project.budget)

        self.__projects.append(project)
        self.__project_ids[project.project_id] = True   
        print(f"Проект '{project.name}' (ID: {project.project_id}) добавлен в компанию '{self.name}'")
    
    def remove_project(self, project_id: int) -> None:
        project = self.get_project(project_id)
        
        if project.get_team_size() > 0:
            raise ValueError(
                f"Невозможно удалить проект '{project.name}' (ID: {project_id}), "
                f"пока над ним работает команда ({project.get_team_size()} сотрудников)"
            )
        
        self.__projects = [proj for proj in self.__projects if proj.project_id != project_id]
        if project_id in self.__project_ids:
            del self.__project_ids[project_id]
        
        print(f"Проект '{project.name}' (ID: {project_id}) удален из компании '{self.name}'")
    
    def get_project(self, project_id: int) -> Project:
        for project in self.__projects:
            if project.project_id == project_id:
                return project
        raise ProjectNotFoundError(str(project_id))
    
    def get_projects(self):
        return self.__projects
    
    def get_all_employees(self) -> List[AbstractEmployee]:
        all_employees = []
        for department in self.__departments:
            all_employees.extend(department.emp_list)
        return all_employees
    
    def find_employee_by_id(self, employee_id: int) -> List:
        for department in self.__departments:
            employee = department.find_employee_by_id(employee_id)
            if employee:
                return [employee, department]
        
        if employee_id in self.__employee_ids:
            dept_name = self.__employee_ids[employee_id]
            raise EmployeeNotFoundError(dept_name, str(employee_id))
        
        raise EmployeeNotFoundError("неизвестный отдел", str(employee_id))
    
    def calculate_total_monthly_cost(self) -> float:
        return sum(dept.calculate_total_salary() for dept in self.__departments)
    
    def get_projects_by_status(self, status: str) -> List[Project]:
        self.__validate_project_status(status)
        return [project for project in self.__projects if project.status == status]
    
    def update_project_status(self, project_id: int, new_status: str) -> None:
        project = self.get_project(project_id)
        self.__validate_project_status(new_status, project.name)
        
        valid_transitions = {
            "planning": ["active", "cancelled"],
            "active": ["completed", "cancelled"],
            "completed": [],
            "cancelled": []
        }
        
        if project.status in valid_transitions:
            if new_status not in valid_transitions[project.status]:
                raise ValueError(
                    f"Невозможно изменить статус проекта '{project.name}' с '{project.status}' на '{new_status}'. "
                    f"Допустимые переходы: {valid_transitions[project.status]}"
                )
        
        old_status = project.status
        project.status = new_status
        print(f"Статус проекта '{project.name}' изменен с '{old_status}' на '{new_status}'")
    
    def get_company_statistics(self) -> Dict[str, Any]:
        total_employees = len(self.get_all_employees())
        total_salary = self.calculate_total_monthly_cost()
        
        departments_stats = {}
        for department in self.__departments:
            departments_stats[department.name] = {
                'employee_count': len(department),
                'total_salary': department.calculate_total_salary()
            }
        
        projects_stats = {}
        for project in self.__projects:
            projects_stats[project.name] = {
                'status': project.status,
                'team_size': project.get_team_size(),
                'project_salary': project.calculate_total_salary()
            }
        
        status_stats = {}
        for status in Project.statuses:
            projects_with_status = self.get_projects_by_status(status)
            status_stats[status] = len(projects_with_status)
        
        return {
            'company_name': self.name,
            'total_departments': len(self.__departments),
            'total_projects': len(self.__projects),
            'total_employees': total_employees,
            'total_monthly_cost': total_salary,
            'departments': departments_stats,
            'projects': projects_stats,
            'project_statuses': status_stats
        }
    
    def assign_employee_to_project(self, employee_id: int, project_id: int) -> None:
        try:
            empdep = self.find_employee_by_id(employee_id)
            employee = empdep[0]
        except EmployeeNotFoundError as e:
            raise e
        
        try:
            project = self.get_project(project_id)
        except ProjectNotFoundError as e:
            raise e
        
        employee_projects = sum(1 for proj in self.__projects if employee in proj.get_team())
        if employee_projects >= 3:
            raise ValueError(
                f"Сотрудник {employee.name} уже участвует в {employee_projects} проектах (максимум 3)"
            )
        
        if project.status != "active":
            raise ValueError(
                f"Сотрудника можно назначать только на активные проекты. "
                f"Текущий статус проекта '{project.name}': {project.status}"
            )
        
        project.add_team_member(employee)
        print(f"Сотрудник {employee.name} назначен на проект '{project.name}'")
    
    def get_employees_in_multiple_projects(self) -> List[AbstractEmployee]:
        from collections import defaultdict
        
        employee_project_count = defaultdict(int)
        
        for project in self.__projects:
            for employee in project.get_team():
                employee_project_count[employee.id] += 1
        
        busy_employees = []
        all_employees = self.get_all_employees()
        
        for employee in all_employees:
            if employee_project_count.get(employee.id, 0) >= 2:
                busy_employees.append(employee)
        
        return busy_employees
    
    def transfer_employee(self, employee_id: int, to_dept_name: str) -> None:
        try:
            empdep = self.find_employee_by_id(employee_id)
            emp = empdep[0]
            current_dep = empdep[1]
        except EmployeeNotFoundError as e:
            raise e
        
        try:
            new_dep = self.get_department(to_dept_name)
        except DepartmentNotFoundError as e:
            raise e
        
        if current_dep.name == new_dep.name:
            raise ValueError(f"Сотрудник {emp.name} уже находится в отделе '{to_dept_name}'")
        
        if any(employee.id == employee_id for employee in new_dep.emp_list):
            raise DuplicateIdError(str(employee_id))
        
        current_dep.remove_employee(employee_id)
        
        new_dep.add_employee(emp)
        
        self.__employee_ids[employee_id] = new_dep.name
        
        print(f"Сотрудник {emp.name} переведен из отдела '{current_dep.name}' в отдел '{new_dep.name}'")
    
    # ===== СЕРИАЛИЗАЦИЯ =====
    
    def to_dict(self) -> Dict[str, Any]:
        all_employees = self.get_all_employees()
        
        return {
            'version': '1.0',
            'type': 'Company',
            'name': self.name,
            'serialized_at': datetime.now().isoformat(),
            
            'departments': [dept.to_dict() for dept in self.__departments],
            'projects': [proj.to_dict() for proj in self.__projects],
            
            'all_employees': [emp.to_dict() for emp in all_employees],
            
            'statistics': {
                'total_departments': len(self.__departments),
                'total_projects': len(self.__projects),
                'total_employees': len(all_employees),
                'total_monthly_cost': self.calculate_total_monthly_cost(),
                'average_salary_per_employee': (
                    self.calculate_total_monthly_cost() / len(all_employees) 
                    if all_employees else 0
                )
            },
            
            'indices': {
                'employee_departments': {
                    emp.id: dept.name
                    for dept in self.__departments
                    for emp in dept.emp_list
                },
                'employee_projects': {
                    emp.id: [proj.project_id for proj in self.__projects if emp in proj.get_team()]
                    for emp in all_employees
                }
            }
        }
    
    def to_json(self, filepath: str = None, indent: int = 2) -> Optional[str]:
        data = self.to_dict()
        
        class CompanyJSONEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, (datetime, date)):
                    return obj.isoformat()
                if hasattr(obj, 'to_dict'):
                    return obj.to_dict()
                return super().default(obj)
        
        json_str = json.dumps(
            data, 
            cls=CompanyJSONEncoder, 
            indent=indent, 
            ensure_ascii=False,
            sort_keys=True
        )
        
        if filepath:
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)
            
            print(f"Компания сохранена в файл: {filepath}")
            print(f"Размер файла: {os.path.getsize(filepath)} байт")
            return None
        else:
            return json_str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Company':
        if 'type' not in data or data['type'] != 'Company':
            raise ValueError("Некорректный формат данных компании")
        
        company = cls(data['name'])
        
        company.__employee_ids.clear()
        company.__project_ids.clear()
        
        for dept_data in data.get('departments', []):
            try:
                department = Department.from_dict(dept_data)
                company.__departments.append(department)
                
                # Обновляем кэш сотрудников
                for emp in department.emp_list:
                    company.__employee_ids[emp.id] = department.name
                
                print(f"Отдел: {department.name} ({len(department)} сотрудников)")
            except Exception as e:
                print(f"Ошибка восстановления отдела: {e}")
        
        for proj_data in data.get('projects', []):
            try:
                project = Project.from_dict(proj_data)
                company.__projects.append(project)
                company.__project_ids[project.project_id] = True
                
                print(f"Проект: {project.name} (ID: {project.project_id})")
            except Exception as e:
                print(f"Ошибка восстановления проекта: {e}")
        
        loaded_employees = len(company.get_all_employees())
        expected_employees = data.get('statistics', {}).get('total_employees', 0)
        
        if loaded_employees != expected_employees:
            print(f"Расхождение в количестве сотрудников: "
                  f"загружено {loaded_employees}, ожидалось {expected_employees}")
        
        print(f"\nКомпания '{company.name}' успешно загружена")
        print(f"Отделов: {len(company.__departments)}")
        print(f"Проектов: {len(company.__projects)}")
        print(f"Сотрудников: {loaded_employees}")
        
        return company
    
    @classmethod
    def from_json(cls, json_str_or_file: str) -> 'Company':
        if os.path.exists(json_str_or_file):
            with open(json_str_or_file, 'r', encoding='utf-8') as f:
                json_str = f.read()
                print(f"Загружаем из файла: {json_str_or_file}")
        else:
            json_str = json_str_or_file
            print(f"Загружаем из строки JSON ({len(json_str)} символов)")
        
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Некорректный JSON: {e}")
        
        return cls.from_dict(data)
    
    def save_to_file(self, filepath: str = "company_full.json") -> None:
        self.to_json(filepath)
        
        human_filepath = filepath.replace('.json', '_readable.json')
        self.to_json(human_filepath, indent=4)
        
        print(f"\nСтатистика сохранения:")
        print(f"Основной файл: {filepath}")
        print(f"Читаемая версия: {human_filepath}")
        
        data = self.to_dict()
        departments_size = len(data.get('departments', []))
        projects_size = len(data.get('projects', []))
        employees_size = len(data.get('all_employees', []))
        
        print(f"Данные: {departments_size} отделов, {projects_size} проектов, {employees_size} сотрудников")
    
    def load_from_file(self, filepath: str = "company_full.json") -> None:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        
        
        loaded_company = self.from_json(filepath)
        self.__dict__.update(loaded_company.__dict__)
        
        print(f"Состояние загружено")
    
    def validate_data_integrity(self) -> Dict[str, Any]:
        
        original_stats = {
            'company_name': self.name,
            'departments': len(self.__departments),
            'projects': len(self.__projects),
            'employees': len(self.get_all_employees()),
            'total_salary': self.calculate_total_monthly_cost()
        }
        
        print("Сериализуем...")
        json_str = self.to_json()
        
        print("Десериализуем...")
        restored_company = self.from_json(json_str)
        
        restored_stats = {
            'company_name': restored_company.name,
            'departments': len(restored_company._Company__departments),
            'projects': len(restored_company._Company__projects),
            'employees': len(restored_company.get_all_employees()),
            'total_salary': restored_company.calculate_total_monthly_cost()
        }
        
        is_valid = True
        differences = {}
        
        for key in original_stats:
            if original_stats[key] != restored_stats[key]:
                is_valid = False
                differences[key] = {
                    'original': original_stats[key],
                    'restored': restored_stats[key]
                }
        
        return {
            'is_valid': is_valid,
            'original': original_stats,
            'restored': restored_stats,
            'differences': differences,
            'json_size': len(json_str)
        }
        
    def save_to_db(self, db_path: str = 'company.db') -> None:
        db_conn = DatabaseConnection.get_instance(db_path).get_connection()
        cursor = db_conn.cursor()
        
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    base_salary REAL NOT NULL,
                    type TEXT NOT NULL, -- 'Employee', 'Manager', 'Developer', 'Salesperson'
                    extra_data TEXT -- JSON для бонусов, tech_stack и т.д.
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS departments (
                    name TEXT PRIMARY KEY,
                    employee_ids TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    project_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    budget REAL NOT NULL,
                    start_date TEXT,
                    end_date TEXT,
                    team_ids TEXT
                )
            ''')
            
            cursor.execute("DELETE FROM employees")
            cursor.execute("DELETE FROM departments")
            cursor.execute("DELETE FROM projects")
            
            for dept in self.__departments:
                emp_ids = [str(emp.id) for emp in dept.emp_list]
                cursor.execute(
                    "INSERT INTO departments (name, employee_ids) VALUES (?, ?)",
                    (dept.name, json.dumps(emp_ids))
                )
                
            all_employees = self.get_all_employees()
            for emp in all_employees:
                extra = json.dumps(emp.to_dict())
                cursor.execute(
                    "INSERT INTO employees (id, name, department, base_salary, type, extra_data) VALUES (?, ?, ?, ?, ?, ?)",
                    (emp.id, emp.name, emp.department, emp.base_salary, type(emp).__name__, extra)
                )
            
            for proj in self.__projects:
                team_ids = [str(emp.id) for emp in proj.get_team()]
                cursor.execute(
                    "INSERT INTO projects (project_id, name, status, budget, start_date, end_date, team_ids) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (proj.project_id, proj.name, proj.status, proj.budget,
                     proj.start_date.isoformat() if proj.start_date else None,
                     proj.end_date.isoformat() if proj.end_date else None,
                     json.dumps(team_ids))
                )
            
            db_conn.commit()
            print(f"Компания '{self.name}' сохранена в БД: {db_path}")
            print(f"Сотрудников: {len(all_employees)}, Отделов: {len(self.__departments)}, Проектов: {len(self.__projects)}")
        
        except sqlite3.Error as e:
            db_conn.rollback()
            raise ValueError(f"Ошибка БД: {e}")
        finally:
            cursor.close()
    
    def load_from_db(self, db_path: str = "company.db") -> None:
        db_conn = DatabaseConnection.get_instance(db_path).get_connection()
        cursor = db_conn.cursor()

        try:
            self.__departments.clear()
            self.__projects.clear()
            self.__employee_ids.clear()
            self.__project_ids.clear()

            cursor.execute("SELECT * FROM employees")
            employees_by_id = {}

            for row in cursor.fetchall():
                emp_data = json.loads(row['extra_data'])
                emp_type = row['type']

                if emp_type == "Manager":
                    emp = Manager.from_dict(emp_data)
                elif emp_type == "Developer":
                    emp = Developer.from_dict(emp_data)
                elif emp_type == "Salesperson":
                    emp = Salesperson.from_dict(emp_data)
                elif emp_type == "Employee":
                    emp = Employee.from_dict(emp_data)
                else:
                    raise ValueError(f"Неизвестный тип: {emp_type}")

                employees_by_id[emp.id] = emp
                self.__employee_ids[emp.id] = emp.department

            cursor.execute("SELECT * FROM departments")
            for row in cursor.fetchall():
                dept_name = row['name']
                emp_ids_json = row['employee_ids']
                emp_ids = json.loads(emp_ids_json) if emp_ids_json else []

                dept = Department(dept_name)
                for emp_id_str in emp_ids:
                    emp_id = int(emp_id_str)
                    if emp_id in employees_by_id:
                        dept.add_employee(employees_by_id[emp_id])
                    else:
                        print(f"Предупреждение: сотрудник ID {emp_id} не найден при загрузке отдела {dept_name}")

                self.__departments.append(dept)

            cursor.execute("SELECT * FROM projects")
            for row in cursor.fetchall():
                start_date = datetime.fromisoformat(row['start_date']).date() if row['start_date'] else None
                end_date = datetime.fromisoformat(row['end_date']).date() if row['end_date'] else None

                proj_data = {
                    'project_id': row['project_id'],
                    'name': row['name'],
                    'description': '',
                    'start_date': start_date,
                    'end_date': end_date,
                    'budget': row['budget'],
                    'status': row['status'],
                    'team': []
                }
                proj = Project.from_dict(proj_data)
                self.__projects.append(proj)
                self.__project_ids[proj.project_id] = True


                team_ids_json = row['team_ids']
                team_ids = json.loads(team_ids_json) if team_ids_json else []
                for emp_id_str in team_ids:
                    emp_id = int(emp_id_str)
                    if emp_id in employees_by_id:
                        proj.add_team_member(employees_by_id[emp_id])

            print(f"Компания '{self.name}' успешно загружена из БД: {db_path}")
            print(f"→ Сотрудников: {len(employees_by_id)}, Отделов: {len(self.__departments)}, Проектов: {len(self.__projects)}")

        except sqlite3.Error as e:
            db_conn.rollback()
            raise ValueError(f"Ошибка загрузки из БД: {e}")
        finally:
            cursor.close()
                
            
    
    # ===== МАГИЧЕСКИЕ МЕТОДЫ =====
    
    def __str__(self) -> str:
        dept_count = len(self.__departments)
        project_count = len(self.__projects)
        employee_count = len(self.get_all_employees())
        total_cost = self.calculate_total_monthly_cost()
        
        return (f"Company '{self.name}' (Отделов: {dept_count}, "
                f"Проектов: {project_count}, Сотрудников: {employee_count}, "
                f"Месячные расходы: {total_cost:.2f} руб.)")
    
    def __repr__(self) -> str:
        return f"Company(name='{self.name}', departments={len(self.__departments)}, projects={len(self.__projects)})"
    
    def __len__(self) -> int:
        return len(self.get_all_employees())
    
    def __contains__(self, item) -> bool:
        if isinstance(item, Department):
            return any(dept.name == item.name for dept in self.__departments)
        elif isinstance(item, Project):
            return any(proj.project_id == item.project_id for proj in self.__projects)
        elif isinstance(item, AbstractEmployee):
            try:
                empdep = self.find_employee_by_id(item.id)
                return empdep[0] is not None
            except EmployeeNotFoundError:
                return False
        elif isinstance(item, int):  # employee_id
            try:
                empdep = self.find_employee_by_id(item)
                return empdep[0] is not None
            except EmployeeNotFoundError:
                return False
        else:
            return False