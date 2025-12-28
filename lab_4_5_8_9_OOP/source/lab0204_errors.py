class EmployeeNotFoundError(Exception):
    def __init__(self, department_name: str, employee_id: str):
        self.department_name = department_name
        self.employee_id = employee_id
        super().__init__(f"Сотрудник ID: '{employee_id}' не найден в отделе '{department_name}'.")
        
class DepartmentNotFoundError(Exception):
    def __init__(self, department_name: str):
        self.department_name = department_name
        super().__init__(f"Отдел '{department_name}' не найден.")
        
class ProjectNotFoundError(Exception):
    def __init__(self, project_name: str):
        self.project_name = project_name
        super().__init__(f"Проект '{project_name}' не найден.")
        
class InvalidStatusError(Exception):
    def __init__(self, project_name: str, project_status: str):
        self.project_name = project_name
        self.project_status = project_status
        super().__init__(f'Неверный формат статуса проекта для: "{project_name}" — "{project_status}", используйте статусы: ["planning", "active", "completed", "cancelled"].')
        
class DuplicateIdError(Exception):
    def __init__(self, id: int, classname: str):
        self.id = id
        super().__init__(f"Объект класса {classname} с ID: '{id}' уже существует.")