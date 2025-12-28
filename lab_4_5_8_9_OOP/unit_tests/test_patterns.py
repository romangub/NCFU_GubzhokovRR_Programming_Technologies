import pytest
import sys
import os

project_path = "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP"
sys.path.insert(0, project_path)

from source.lab0202_employee import Employee
from source.lab0202_manager import Manager
from source.lab0202_developer import Developer
from source.lab0202_salesperson import Salesperson
from source.lab03_singleton import DatabaseConnection
from source.lab03_employee_builder import EmployeeBuilder
from source.lab03_abstract_сompany_factory import AbstractCompanyFactory
from source.lab03_sales_company_factory import SalesCompanyFactory
from source.lab03_tech_company_factory import TechCompanyFactory
from mock_systems.lab03_external_payroll import PayrollSystem
from source.lab03_payroll_adapter import PayrollAdapter
from source.lab03_employee_decorators import (
    BonusDecorator, TrainingDecorator
)
from source.lab03_facade import CompanyFacade


class TestDatabaseConnectionSingleton:
    def test_singleton_same_instance(self):
        db_path = os.path.abspath("temp_test_company.db")
        
        conn1 = DatabaseConnection.get_instance(db_path)
        conn2 = DatabaseConnection.get_instance(db_path)
        
        assert conn1 is conn2
        assert id(conn1) == id(conn2)

    def test_different_paths_different_instances(self):
        path1 = os.path.abspath("db1.db")
        path2 = os.path.abspath("db2.db")
        
        conn1 = DatabaseConnection.get_instance(path1)
        conn2 = DatabaseConnection.get_instance(path2)
        
        assert conn1 is not conn2


class TestEmployeeBuilder:
    def test_build_simple_employee(self):
        emp = (EmployeeBuilder()
               .with_id(7)
               .with_name("Мария Сидорова")
               .with_department("HR")
               .with_base_salary(4800)
               .build())
        
        assert isinstance(emp, Employee)
        assert not isinstance(emp, (Manager, Developer, Salesperson))
        assert emp.id == 7
        assert emp.name == "Мария Сидорова"
        assert emp.base_salary == 4800

    def test_build_manager(self):
        mgr = (EmployeeBuilder()
               .with_id(8)
               .with_name("Сергей Ковалёв")
               .with_department("Tech")
               .with_base_salary(8500)
               .with_bonus(3200)
               .build())
        
        assert isinstance(mgr, Manager)
        assert mgr.bonus == 3200
        assert mgr.calculate_salary() == 8500 + 3200

    def test_build_developer(self):
        dev = (EmployeeBuilder()
               .with_id(9)
               .with_name("Дмитрий Волков")
               .with_department("Development")
               .with_base_salary(6200)
               .add_skill("Go")
               .add_skill("Kubernetes")
               .with_seniority_level("senior")
               .build())
        
        assert isinstance(dev, Developer)
        assert dev.tech_stack == ["Go", "Kubernetes"]
        assert dev.seniority_level == "senior"


class TestAbstractCompanyFactory:
    def test_tech_company_factory_creates_correct_types(self):
        factory = TechCompanyFactory()
        company = factory.build_company("TechNova", num_depts=2, num_employees_per_dept=3, num_projects=1)
        
        stats = company.get_company_statistics()
        
        # Проверяем, что есть отделы с разработчиками (например, Development)
        assert "departments" in stats
        dept_names = stats["departments"].keys()
        
        # В тех-компании должны быть разработческие отделы
        dev_departments = ["Development", "Dev", "R&D", "Engineering"]  # возможные названия
        has_dev_dept = any(dev_name in dept_names for dev_name in dev_departments)
        assert has_dev_dept, f"Ожидался хотя бы один разработческий отдел, а есть: {list(dept_names)}"
        
        # Проверяем, что в разработческих отделах есть сотрудники
        total_dev_employees = 0
        for dept_name, dept_data in stats["departments"].items():
            if any(dev_name in dept_name for dev_name in dev_departments):
                total_dev_employees += dept_data["employee_count"]
        
        assert total_dev_employees > 0, "В тех-компании должны быть сотрудники в разработческих отделах"
        
        # Дополнительно: должны быть менеджеры — обычно в каждом отделе есть хотя бы один
        # Но если их нет в статистике по типам — проверяем косвенно через зарплаты или просто наличие отделов
        assert len(stats["departments"]) >= 2  # num_depts=2
        
        # Salesperson не должен доминировать — в тех-компании их быть не должно или минимум
        sales_departments = ["Sales", "Продажи"]
        has_sales_dept = any(sales_name in dept_names for sales_name in sales_departments)
        assert not has_sales_dept, "В тех-компании не должно быть отдела продаж"

    def test_sales_company_factory_creates_correct_types(self):
        factory = SalesCompanyFactory()
        company = factory.build_company("SellFast", num_depts=2, num_employees_per_dept=4, num_projects=0)
        
        stats = company.get_company_statistics()
        
        assert "departments" in stats
        dept_names = stats["departments"].keys()
        
        # В продажной компании должен быть отдел продаж
        sales_departments = ["Sales", "Продажи", "Sales Department"]
        has_sales_dept = any(sales_name in dept_names for sales_name in sales_departments)
        assert has_sales_dept, f"Ожидался отдел продаж, а есть: {list(dept_names)}"
        
        total_sales_employees = 0
        for dept_name, dept_data in stats["departments"].items():
            if any(sales_name in dept_name for sales_name in sales_departments):
                total_sales_employees += dept_data["employee_count"]
        
        assert total_sales_employees > 0, "В отделе продаж должны быть сотрудники"
        
        # В продажной компании не должно быть разработческих отделов
        dev_departments = ["Development", "Dev", "R&D", "Engineering", "QA"]
        has_dev_dept = any(dev_name in dept_names for dev_name in dev_departments)
        assert not has_dev_dept, "В продажной компании не должно быть разработческих отделов"


class TestPayrollAdapter:
    @pytest.fixture
    def sample_employees(self):
        mgr = Manager(10, "Ольга", "Management", 9000, bonus=4000)
        dev = Developer(11, "Павел", "Dev", 5800, ["Java"], "middle")
        return mgr, dev

    def test_adapter_calculates_different_from_native(self, sample_employees):
        mgr, dev = sample_employees
        
        native_mgr = mgr.calculate_salary()
        native_dev = dev.calculate_salary()
        
        adapter = PayrollAdapter()
        
        adapted_mgr = adapter.calculate_salary(mgr)
        adapted_dev = adapter.calculate_salary(dev)
        
        assert adapted_mgr != native_mgr
        assert adapted_dev != native_dev
        # Здесь можно добавить более точные проверки, если известна точная формула адаптера


class TestEmployeeDecorators:
    @pytest.fixture
    def base_employee(self):
        return Employee(12, "Антон", "Support", 5200)

    def test_bonus_decorator(self, base_employee):
        decorated = BonusDecorator(base_employee, fixed_bonus=1800)
        
        assert decorated.calculate_salary() == 5200 + 1800
        assert "Бонус" in decorated.get_info()

    def test_training_decorator(self, base_employee):
        decorated = TrainingDecorator(base_employee, "Advanced Communication")
        
        assert decorated.calculate_salary() == pytest.approx(5200 * 1.10, 0.01)  # 10% надбавка — типичный кейс
        assert "Прошёл тренинг" in decorated.get_info()

    def test_decorator_composition(self, base_employee):
        bonus = BonusDecorator(base_employee, 2500)
        double = TrainingDecorator(bonus, "Team Lead Course")
        
        expected = (5200 + 2500) * 1.10
        assert double.calculate_salary() == pytest.approx(expected, 0.01)


class TestCompanyFacade:
    def test_facade_hire_and_statistics(self):
        facade = CompanyFacade("TestMegaCorp")
        
        facade.hire_employee("manager", "Виктор", "Management", 9500, bonus=3500)
        facade.hire_employee("developer", "Яна", "Development", 6400, tech_stack=["Rust", "Go"], seniority_level="senior")
        facade.hire_employee("salesperson", "Максим", "Sales", 4800, commission_rate=0.13, sales_volume=180000)
        
        stats = facade.get_statistics()
        
        # Вместо плоских employees_count и total_salary проверяем через departments
        departments = stats["departments"]
        total_employees = sum(info["employee_count"] for info in departments.values())
        total_salary = sum(info["total_salary"] for info in departments.values())
        
        assert total_employees == 3
        assert total_salary > 50000  # грубо, но надёжно
        
        # Увольнение
        facade.fire_employee(1)
        new_stats = facade.get_statistics()
        new_total = sum(info["employee_count"] for info in new_stats["departments"].values())
        assert new_total == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])