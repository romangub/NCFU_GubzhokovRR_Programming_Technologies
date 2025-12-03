from .lab0202_employee_factory import EmployeeFactory

def main():
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ СИСТЕМЫ СОТРУДНИКОВ")
    print("=" * 70)
    
    # 1. Создание экземпляров каждого типа сотрудника через фабрику
    print("\n1. СОЗДАНИЕ СОТРУДНИКОВ ЧЕРЕЗ ФАБРИКУ")
    print("-" * 50)
    
    try:
        # Создаем сотрудников разных типов
        employee = EmployeeFactory.create_employee(
            "employee",
            id=100,
            name="Иван Иванов",
            department="Общий отдел",
            base_salary=50000
        )
        
        manager = EmployeeFactory.create_employee(
            "manager", 
            id=200,
            name="Петр Петров",
            department="Отдел управления",
            base_salary=80000,
            bonus=20000
        )
        
        developer = EmployeeFactory.create_employee(
            "developer",
            id=300,
            name="Анна Программистова",
            department="IT отдел", 
            base_salary=70000,
            tech_stack=["Python", "Django", "PostgreSQL"],
            seniority_level="senior"
        )
        
        salesperson = EmployeeFactory.create_employee(
            "salesperson",
            id=400,
            name="Мария Продажникова",
            department="Отдел продаж",
            base_salary=40000,
            commission_rate=0.1,
            sales_volume=500000
        )
        
        print("Все сотрудники успешно созданы через фабрику")
        
    except ValueError as e:
        print(f" Ошибка при создании сотрудников: {e}")
        return

    # 2. Демонстрация работы с каждым экземпляром
    print("\n2. ДЕМОНСТРАЦИЯ РАБОТЫ С КАЖДЫМ СОТРУДНИКОМ")
    print("-" * 50)
    
    # Для каждого сотрудника показываем calculate_salary() и get_info()
    employees_list = [employee, manager, developer, salesperson]
    
    for emp in employees_list:
        print(f"\n--- {emp.__class__.__name__} ---")
        print(f"calculate_salary(): {emp.calculate_salary():.2f} руб.")
        print(f"get_info(): {emp.get_info()}")
    
    # 3. Демонстрация работы сеттеров
    print("\n3. ДЕМОНСТРАЦИЯ РАБОТЫ СЕТТЕРОВ")
    print("-" * 50)
    
    # Меняем данные через сеттеры
    print("До изменения:")
    print(f"Менеджер: {manager.get_info()}")
    
    manager.bonus = 30000  # Увеличиваем бонус
    manager.department = "Высшее руководство"
    
    print("\nПосле изменения бонуса и отдела:")
    print(f"Менеджер: {manager.get_info()}")
    
    # 4. Демонстрация полиморфизма
    print("\n4. ДЕМОНСТРАЦИЯ ПОЛИМОРФИЗМА")
    print("-" * 50)
    
    print("Итерация по списку разных типов сотрудников:")
    all_employees = [employee, manager, developer, salesperson]
    
    for i, emp in enumerate(all_employees, 1):
        print(f"{i}. {emp.get_info()}")
    
    # 5. Создание дополнительных сотрудников через фабрику
    print("\n5. ДОПОЛНИТЕЛЬНОЕ СОЗДАНИЕ ЧЕРЕЗ ФАБРИКУ")
    print("-" * 50)
    
    try:
        # Создаем еще сотрудников разных типов
        junior_dev = EmployeeFactory.create_employee(
            "developer",
            id=501,
            name="Сергей Начинающий",
            department="IT отдел",
            base_salary=40000,
            tech_stack=["Python"],
            seniority_level="junior"
        )
        
        successful_sales = EmployeeFactory.create_employee(
            "salesperson", 
            id=502,
            name="Ольга Успешная",
            department="Отдел продаж",
            base_salary=45000,
            commission_rate=0.15,
            sales_volume=1000000
        )
        
        print("Дополнительно созданные сотрудники:")
        print(f"- {junior_dev.get_info()}")
        print(f"- {successful_sales.get_info()}")
        
        # Добавляем в общий список
        all_employees.extend([junior_dev, successful_sales])
        
    except ValueError as e:
        print(f"Ошибка при создании дополнительных сотрудников: {e}")
    
    # 6. Итоговая демонстрация полиморфного поведения
    print("\n6. ИТОГОВАЯ ДЕМОНСТРАЦИЯ ПОЛИМОРФИЗМА")
    print("-" * 50)
    
    print(f"Всего сотрудников в системе: {len(all_employees)}")
    print("\nПолная информация о всех сотрудниках:")
    
    for i, emp in enumerate(all_employees, 1):
        print(f"\n{i}. {emp.get_info()}")
        print(f"   Расчитанная зарплата: {emp.calculate_salary():.2f} руб.")
    
    # 7. Демонстрация обработки ошибок фабрики
    print("\n7. ДЕМОНСТРАЦИЯ ОБРАБОТКИ ОШИБОК")
    print("-" * 50)
    
    try:
        # Неизвестный тип сотрудника
        invalid_emp = EmployeeFactory.create_employee("director", id=999, name="Тест")
    except ValueError as e:
        print(f"✅ Корректная обработка неизвестного типа: {e}")
    
    try:
        # Недостаточно параметров
        incomplete_emp = EmployeeFactory.create_employee("employee", id=999, name="Тест")
    except ValueError as e:
        print(f"✅ Корректная обработка недостающих параметров: {e}")
    
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
    print("=" * 70)

if __name__ == "__main__":
    main()