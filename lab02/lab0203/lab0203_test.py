# lab0205_demo.py
# Демонстрация и тестирование всех возможностей системы сотрудников и отделов

import sys
import os
import functools

# Добавляем пути для импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lab0202.lab0202_abstract_employee import AbstractEmployee
from lab0202.lab0202_employee import Employee
from lab0202.lab0202_manager import Manager
from lab0202.lab0202_developer import Developer
from lab0202.lab0202_salesperson import Salesperson
from lab0203.lab0203_department import Department

# Функции-компараторы для сортировки
def compare_by_name(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Компаратор для сортировки по имени (алфавитный порядок)"""
    if emp1.name < emp2.name:
        return -1
    elif emp1.name > emp2.name:
        return 1
    else:
        return 0

def compare_by_salary(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Компаратор для сортировки по зарплате (по убыванию)"""
    salary1 = emp1.calculate_salary()
    salary2 = emp2.calculate_salary()
    if salary1 > salary2:
        return -1
    elif salary1 < salary2:
        return 1
    else:
        return 0

def compare_by_department_then_name(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Компаратор для сортировки по отделу, а затем по имени"""
    if emp1.department < emp2.department:
        return -1
    elif emp1.department > emp2.department:
        return 1
    else:
        return compare_by_name(emp1, emp2)

def main():
    """Основная демонстрационная функция"""
    
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ СИСТЕМЫ СОТРУДНИКОВ И ОТДЕЛОВ")
    print("=" * 70)
    
    # 1. СОЗДАНИЕ ОТДЕЛА И ДОБАВЛЕНИЕ СОТРУДНИКОВ
    print("\n1. СОЗДАНИЕ ОТДЕЛА И ДОБАВЛЕНИЕ СОТРУДНИКОВ")
    print("-" * 50)
    
    # Создаем отдел
    it_department = Department("IT Департамент")
    print(f"Создан отдел: {it_department}")
    
    # Создаем сотрудников разных типов
    employee1 = Employee(id=100, name="Иван Иванов", department="", base_salary=50000)
    employee2 = Employee(id=101, name="Анна Петрова", department="", base_salary=45000)
    manager1 = Manager(id=102, name="Петр Сидоров", department="", base_salary=70000, bonus=15000)
    developer1 = Developer(id=103, name="Дмитрий Орлов", department="", base_salary=60000,
                          tech_stack=["Python", "Django", "PostgreSQL"], seniority_level="middle")
    developer2 = Developer(id=104, name="Екатерина Белова", department="", base_salary=65000,
                          tech_stack=["Java", "Spring", "Hibernate"], seniority_level="senior")
    salesperson1 = Salesperson(id=105, name="Мария Смирнова", department="", base_salary=40000, 
                              commission_rate=0.1, sales_volume=500000)
    
    # Добавляем сотрудников в отдел
    employees = [employee1, employee2, manager1, developer1, developer2, salesperson1]
    for emp in employees:
        it_department.add_employee(emp)
        print(f"Добавлен: {emp.name}")
    
    print(f"\nВ отделе теперь {len(it_department)} сотрудников")
    
    # 2. ВЫЗОВ calculate_total_salary() ДЛЯ ОТДЕЛА
    print("\n2. РАСЧЕТ ОБЩЕЙ ЗАРПЛАТЫ ОТДЕЛА")
    print("-" * 50)
    
    total_salary = it_department.calculate_total_salary()
    print(f"Общая зарплата отдела '{it_department.name}': {total_salary:.2f} руб.")
    
    # 3. ИСПОЛЬЗОВАНИЕ ПЕРЕГРУЖЕННЫХ ОПЕРАТОРОВ
    print("\n3. ИСПОЛЬЗОВАНИЕ ПЕРЕГРУЖЕННЫХ ОПЕРАТОРОВ")
    print("-" * 50)
    
    # 3.1 Сравнение двух сотрудников (==, <)
    print("\nа) Сравнение сотрудников:")
    print(f"employee1 == employee2: {employee1 == employee2}")
    print(f"employee1 == employee1: {employee1 == employee1}")
    print(f"employee1 < manager1 (по зарплате): {employee1 < manager1}")
    print(f"manager1 < developer1 (по зарплате): {manager1 < developer1}")
    
    # 3.2 Суммирование зарплат сотрудников (employee1 + employee2)
    print("\nб) Суммирование зарплат:")
    sum_salaries = employee1 + employee2
    print(f"employee1 + employee2 = {sum_salaries:.2f}")
    sum_complex = manager1 + developer1 + salesperson1
    print(f"manager1 + developer1 + salesperson1 = {sum_complex:.2f}")
    
    # 3.3 Суммирование списка сотрудников через sum()
    print("\nв) Суммирование списка сотрудников:")
    total_via_sum = sum(employees)
    print(f"sum(employees) = {total_via_sum:.2f}")
    print(f"Проверка: совпадает с общей зарплатой? {abs(total_via_sum - total_salary) < 0.01}")
    
    # 3.4 Проверка вхождения сотрудника в отдел (in)
    print("\nг) Проверка вхождения сотрудника в отдел:")
    print(f"employee1 в отделе: {employee1 in it_department}")
    print(f"manager1 в отделе: {manager1 in it_department}")
    
    # Создаем сотрудника, которого нет в отделе
    outsider = Employee(id=999, name="Чужой", department="", base_salary=10000)
    print(f"outsider в отделе: {outsider in it_department}")
    
    # 3.5 Доступ к сотрудникам отдела по индексу
    print("\nд) Доступ к сотрудникам по индексу:")
    print(f"Первый сотрудник: {it_department[0].name}")
    print(f"Последний сотрудник: {it_department[-1].name}")
    print(f"Второй и третий сотрудники: {[emp.name for emp in it_department[1:3]]}")
    
    # 4. ИТЕРАЦИЯ ПО ОТДЕЛУ И ПО СТЕКУ ТЕХНОЛОГИЙ РАЗРАБОТЧИКА
    print("\n4. ИТЕРАЦИЯ")
    print("-" * 50)
    
    # 4.1 Итерация по отделу
    print("\nа) Итерация по отделу:")
    for i, employee in enumerate(it_department, 1):
        print(f"  {i}. {employee.name} - {employee.calculate_salary():.2f} руб.")
    
    # 4.2 Итерация по стеку технологий разработчика
    print("\nб) Итерация по стеку технологий разработчика:")
    print(f"Технологии {developer1.name}:")
    for skill in developer1:
        print(f"  - {skill}")
    
    print(f"\nТехнологии {developer2.name}:")
    for skill in developer2:
        print(f"  - {skill}")
    
    # 5. СОХРАНЕНИЕ И ЗАГРУЗКА ОТДЕЛА ИЗ ФАЙЛА
    print("\n5. СЕРИАЛИЗАЦИЯ И ДЕСЕРИАЛИЗАЦИЯ")
    print("-" * 50)
    
    filename = "it_department_backup.json"
    
    # 5.1 Сохранение в файл
    it_department.save_to_file(filename)
    print(f"Отдел сохранен в файл: {filename}")
    
    # 5.2 Загрузка из файла
    loaded_department = Department.load_from_file(filename)
    print(f"Отдел загружен из файла: {filename}")
    print(f"Загруженный отдел: {loaded_department.name}")
    print(f"Количество сотрудников в загруженном отделе: {len(loaded_department)}")
    
    # Проверка целостности данных
    print("\nПроверка целостности данных после загрузки:")
    loaded_total = loaded_department.calculate_total_salary()
    print(f"Общая зарплата загруженного отдела: {loaded_total:.2f}")
    print(f"Данные совпадают: {abs(loaded_total - total_salary) < 0.01}")
    
    # 6. СОРТИРОВКА СОТРУДНИКОВ ПО РАЗЛИЧНЫМ КРИТЕРИЯМ
    print("\n6. СОРТИРОВКА СОТРУДНИКОВ")
    print("-" * 50)
    
    # 6.1 Сортировка с использованием key=
    print("\nа) Сортировка с использованием key=:")
    
    sorted_by_name = sorted(it_department, key=lambda emp: emp.name)
    print("По имени:")
    for emp in sorted_by_name:
        print(f"  - {emp.name}")
    
    sorted_by_salary_desc = sorted(it_department, key=lambda emp: emp.calculate_salary(), reverse=True)
    print("\nПо зарплате (убывание):")
    for emp in sorted_by_salary_desc:
        print(f"  - {emp.name}: {emp.calculate_salary():.2f}")
    
    # 6.2 Сортировка с использованием компараторов
    print("\nб) Сортировка с использованием компараторов:")
    
    sorted_with_comparator = sorted(it_department, key=functools.cmp_to_key(compare_by_department_then_name))
    print("По отделу и имени:")
    for emp in sorted_with_comparator:
        print(f"  - {emp.department}: {emp.name}")
    
    # 7. ПОИСК СОТРУДНИКА ПО ID
    print("\n7. ПОИСК СОТРУДНИКА ПО ID")
    print("-" * 50)
    
    search_ids = [100, 103, 999]  # Существующие и несуществующий ID
    
    for emp_id in search_ids:
        found_employee = it_department.find_employee_by_id(emp_id)
        if found_employee:
            print(f"Найден сотрудник с ID {emp_id}: {found_employee.name}")
        else:
            print(f"Сотрудник с ID {emp_id} не найден")
    
    # ДОПОЛНИТЕЛЬНАЯ ДЕМОНСТРАЦИЯ
    print("\n" + "=" * 70)
    print("ДОПОЛНИТЕЛЬНАЯ ДЕМОНСТРАЦИЯ")
    print("=" * 70)
    
    # Демонстрация удаления сотрудника
    print("\nУДАЛЕНИЕ СОТРУДНИКА:")
    print(f"До удаления: {len(it_department)} сотрудников")
    it_department.remove_employee(101)  # Удаляем Анну Петрову
    print(f"После удаления: {len(it_department)} сотрудников")
    
    # Демонстрация подсчета сотрудников по типам
    print("\nСТАТИСТИКА ПО ТИПАМ СОТРУДНИКОВ:")
    count_by_type = it_department.get_employee_count()
    for emp_type, count in count_by_type.items():
        print(f"  {emp_type}: {count}")
    
    # Демонстрация информации о сотрудниках
    print("\nПОДРОБНАЯ ИНФОРМАЦИЯ О СОТРУДНИКАХ:")
    for employee in it_department:
        print(f"  - {employee.get_info()}")
    
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
    print("=" * 70)

if __name__ == "__main__":
    main()