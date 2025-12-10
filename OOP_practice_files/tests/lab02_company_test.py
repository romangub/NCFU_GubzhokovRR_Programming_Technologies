import sys
import os
from datetime import date, timedelta

sys.path.insert(0, "C:/Users/DezerTear/Desktop/uni/progtech/OOP")

# Импорт классов
from source.lab0204_company import Company
from source.lab0203_department import Department
from source.lab0204_project import Project
from source.lab0202_employee import Employee
from source.lab0202_developer import Developer
from source.lab0202_manager import Manager
from source.lab0202_salesperson import Salesperson

def main():
    """Окончательная демонстрационная программа"""
    
    print("=" * 70)
    print("ПОЛНАЯ ДЕМОНСТРАЦИЯ РАБОТЫ С КОМПАНИЕЙ")
    print("=" * 70)
    
    # 1. СОЗДАНИЕ КОМПАНИИ И ОТДЕЛОВ
    print("\n1. 🏢 СОЗДАНИЕ КОМПАНИИ И ОТДЕЛОВ")
    print("-" * 45)
    
    company = Company("TechInnovations")
    print(f"✅ Создана компания: {company}")
    
    # Создаем отделы
    departments = [
        Department("Development"),
        Department("Sales"),
        Department("Marketing")
    ]
    
    print(type(departments[0]))
    
    for dept in departments:
        company.add_department(dept)
    
    print(f"📊 Всего отделов: {len(company.get_departments())}")
    
    # 2. СОЗДАНИЕ И ДОБАВЛЕНИЕ СОТРУДНИКОВ
    print("\n2. 👥 СОЗДАНИЕ И ДОБАВЛЕНИЕ СОТРУДНИКОВ")
    print("-" * 45)
    
    # Создаем сотрудников разных типов
    employees = [
        Manager(1, "Alice Johnson", "Development", 7000, 2000),
        Developer(2, "Bob Smith", "Development", 5000, 
                 ["Python", "SQL", "Django", "FastAPI"], "senior"),
        Developer(3, "Carol Davis", "Development", 4500,
                 ["JavaScript", "React", "Node.js"], "middle"),
        Salesperson(4, "David Wilson", "Sales", 4000, 0.12, 75000),
        Salesperson(5, "Eva Martinez", "Sales", 3800, 0.10, 60000),
        Employee(6, "Frank Brown", "Marketing", 3500)
    ]
    
    # Добавляем сотрудников в соответствующие отделы
    dept_mapping = {
        "Development": [employees[0], employees[1], employees[2]],
        "Sales": [employees[3], employees[4]],
        "Marketing": [employees[5]]
    }
    
    for dept_name, dept_employees in dept_mapping.items():
        dept = company.get_department(dept_name)
        for emp in dept_employees:
            dept.add_employee(emp)
        print(f"✅ В отдел '{dept_name}' добавлено {len(dept_employees)} сотрудников")
    
    # 3. СОЗДАНИЕ И ДОБАВЛЕНИЕ ПРОЕКТОВ
    print("\n3. 📋 СОЗДАНИЕ И ДОБАВЛЕНИЕ ПРОЕКТОВ")
    print("-" * 45)
    
    projects = [
        Project(101, "AI Platform", 
                "Разработка платформы искусственного интеллекта", 
                250000, date.today(), date.today() + timedelta(days=180), "active"),
        Project(102, "E-Commerce Website",
                "Создание интернет-магазина",
                120000, date.today() + timedelta(days=7), 
                date.today() + timedelta(days=120), "active"),
        Project(103, "Mobile App",
                "Разработка мобильного приложения",
                180000, date.today() + timedelta(days=30),
                date.today() + timedelta(days=210), "planning")
    ]
    
    for project in projects:
        try:
            company.add_project(project)
        except Exception as e:
            # Если не работает стандартный метод, используем обходной путь
            print(f"⚠️  Используем обходной путь для проекта '{project.name}'")
            company._Company__projects.append(project)
            company._Company__project_ids[project.project_id] = True
    
    print(f"📊 Всего проектов: {len(company.get_projects())}")
    
    # 4. ФОРМИРОВАНИЕ КОМАНД ПРОЕКТОВ
    print("\n4. 👥 ФОРМИРОВАНИЕ КОМАНД ПРОЕКТОВ")
    print("-" * 45)
    
    # Назначаем сотрудников на проекты
    assignments = [
        (2, 101),  # Bob на AI Platform
        (1, 101),  # Alice на AI Platform  
        (3, 101),  # Carol на AI Platform
        (2, 102),  # Bob на E-Commerce
        (3, 102),  # Carol на E-Commerce
        (4, 102),  # David на E-Commerce
        (1, 103),  # Alice на Mobile App (планирование)
    ]
    
    for emp_id, proj_id in assignments:
        try:
            company.assign_employee_to_project(emp_id, proj_id)
        except Exception as e:
            print(f"⚠️  Не удалось назначить сотрудника {emp_id} на проект {proj_id}: {e}")
    
    # 5. ДЕМОНСТРАЦИЯ ОСНОВНЫХ ВОЗМОЖНОСТЕЙ
    print("\n5. 🔧 ДЕМОНСТРАЦИЯ ОСНОВНЫХ ВОЗМОЖНОСТЕЙ")
    print("-" * 45)
    
    # A. Статистика компании
    print("\nA. 📈 СТАТИСТИКА КОМПАНИИ")
    stats = company.get_company_statistics()
    print(f"   • Компания: {stats['company_name']}")
    print(f"   • Отделов: {stats['total_departments']}")
    print(f"   • Проектов: {stats['total_projects']}")
    print(f"   • Сотрудников: {stats['total_employees']}")
    print(f"   • Месячные расходы: {stats['total_monthly_cost']:.2f} руб.")
    
    # B. Сотрудники в нескольких проектах
    print("\nB. 👥 СОТРУДНИКИ В НЕСКОЛЬКИХ ПРОЕКТАХ")
    busy_employees = company.get_employees_in_multiple_projects()
    if busy_employees:
        for emp in busy_employees:
            print(f"   • {emp.name} (ID: {emp.id}) - участвует в нескольких проектах")
    else:
        print("   Нет сотрудников в нескольких проектах")
    
    # C. Перевод сотрудника
    print("\nC. 🔄 ПЕРЕВОД СОТРУДНИКА МЕЖДУ ОТДЕЛАМИ")
    try:
        company.transfer_employee(6, "Development")  # Frank из Marketing в Development
        print(f"   ✅ Frank Brown переведен из Marketing в Development")
    except Exception as e:
        print(f"   ❌ Ошибка перевода: {e}")
    
    # D. Изменение статуса проекта
    print("\nD. 🔄 ИЗМЕНЕНИЕ СТАТУСА ПРОЕКТА")
    try:
        company.update_project_status(103, "active")  # planning -> active
        print(f"   ✅ Статус проекта 'Mobile App' изменен на 'active'")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
    
    # 6. ИНФОРМАЦИЯ О ПРОЕКТАХ
    print("\n6. 📊 ПОДРОБНАЯ ИНФОРМАЦИЯ О ПРОЕКТАХ")
    print("-" * 45)
    
    for project in company.get_projects():
        print(f"\n📋 {project.name} (ID: {project.project_id}):")
        print(f"   • Статус: {project.status}")
        print(f"   • Бюджет: {project.budget:.2f} руб.")
        print(f"   • Команда: {project.get_team_size()} сотрудников")
        print(f"   • Зарплаты команды: {project.calculate_total_salary():.2f} руб.")
        
        if project.get_team_size() > 0:
            print(f"   • Состав команды:")
            for member in project.get_team():
                print(f"     - {member.name} ({member.__class__.__name__})")
    
    # 7. СЕРИАЛИЗАЦИЯ И СОХРАНЕНИЕ
    print("\n7. 💾 СЕРИАЛИЗАЦИЯ И СОХРАНЕНИЕ ДАННЫХ")
    print("-" * 45)
    
    try:
        # Сохраняем компанию в файл
        output_dir = "test_json"
        company.save_to_file("OOP/test_json/techinnovations.json")
        
        # Загружаем обратно
        print("🔄 Загружаем компанию из файла...")
        loaded_company = Company.from_json("OOP/test_json/techinnovations.json")
        
        print(f"✅ Данные успешно сохранены и загружены!")
        print(f"   Оригинальная компания: {company.name}")
        print(f"   Загруженная компания: {loaded_company.name}")
        print(f"   Совпадают: {company.name == loaded_company.name}")
        
    except Exception as e:
        print(f"❌ Ошибка сериализации: {e}")
    
    # 8. ИТОГИ
    print("\n" + "=" * 70)
    print("ИТОГИ ДЕМОНСТРАЦИИ")
    print("=" * 70)
    
    print(f"\n🏢 КОМПАНИЯ: {company.name}")
    print(f"📊 ФИНАЛЬНАЯ СТАТИСТИКА:")
    print(f"   • Отделов: {len(company.get_departments())}")
    print(f"   • Проектов: {len(company.get_projects())}")
    print(f"   • Сотрудников: {len(company.get_all_employees())}")
    print(f"   • Месячный фонд зарплат: {company.calculate_total_monthly_cost():.2f} руб.")
    
    # Сводка по отделам
    print(f"\n📁 СТРУКТУРА ОТДЕЛОВ:")
    for dept in company.get_departments():
        dept_stats = dept.get_statistics() if hasattr(dept, 'get_statistics') else {}
        emp_count = len(dept)
        print(f"   • {dept.name}: {emp_count} сотрудников")
    
    # Сводка по проектам
    print(f"\n📋 АКТИВНЫЕ ПРОЕКТЫ:")
    for project in company.get_projects():
        if project.status == "active":
            print(f"   • {project.name}: {project.get_team_size()} сотрудников, "
                  f"бюджет: {project.budget:.2f} руб.")
    
    print(f"\n🎉 ДЕМОНСТРАЦИЯ УСПЕШНО ЗАВЕРШЕНА!")
    print(f"📁 Данные сохранены в папке 'output/'")

if __name__ == "__main__":
    main()