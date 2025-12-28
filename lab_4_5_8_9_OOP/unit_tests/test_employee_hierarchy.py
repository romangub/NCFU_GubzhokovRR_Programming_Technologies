import pytest
import sys

project_path = "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP"
sys.path.insert(0, project_path)

from abc import ABC
from source.lab0202_abstract_employee import AbstractEmployee
from source.lab0202_employee import Employee
from source.lab0202_manager import Manager
from source.lab0202_developer import Developer
from source.lab0202_salesperson import Salesperson
from source.lab03_employee_builder import EmployeeBuilder


class TestAbstractEmployee:
   
    def test_abs_emp_impossible(self):
        with pytest.raises(TypeError) as error:
            AbstractEmployee()
        print(error)
        
class TestManager:
    def test_manager_sal_calc(self):
        manager = Manager(1, "Alex", "Management", 1250, 1000)
        salary = manager.calculate_salary()
        
        assert salary == 2250
    
    def test_manager_get_info_w_bonus(self):
        manager = Manager(1, "Alex", "Management", 1250, 1000)
        
        info = manager.get_info()
        
        assert "бонус: 1000" in info
        assert "итоговая зарплата: 2250" in info
    
    def test_manager_bonus_setter_valid(self):
        manager = Manager(1, "Alex", "Management", 1250, 1000)

        manager.bonus = 2000
        assert manager.bonus == 2000
        
        with pytest.raises(ValueError):
            manager.bonus = -500


class TestDeveloper:
    
    @pytest.mark.parametrize("level,expected_salary", [
        ("junior", 1250),
        ("middle", 1875),
        ("senior", 2500)
    ])
    def test_developer_salary_by_level(self, level, expected_salary):
        dev = Developer(1, "Bob", "DEV", 1250, ["Python"], level)
        
        assert dev.calculate_salary() == expected_salary
    
    def test_developer_add_skill(self):
        dev = Developer(1, "Bob", "DEV", 1250, ["Python"], "middle")
        
        dev.add_skill("Java")
        
        assert "Java" in dev.tech_stack
        assert len(dev.tech_stack) == 2
    
    def test_developer_add_duplicate_skill(self):
        dev = Developer(1, "Bob", "DEV", 1250, ["Python"], "middle")
        
        dev.add_skill("Python")  # Дубликат
        
        assert dev.tech_stack.count("Python") == 1
    
    def test_developer_get_info_includes_tech_stack(self):
        dev = Developer(1, "Bob", "DEV", 1250, ["Python", "Java"], "senior")
        
        info = dev.get_info()
        
        assert "Python" in info
        assert "Java" in info
        assert "senior" in info
    
    def test_developer_invalid_seniority_level(self):
        with pytest.raises(ValueError) as error:
            Developer(1, "Bob", "DEV", 1250, ["Python"], "invalid_level")
        print(error)
    
    def test_developer_skills_iteration(self):
        dev = Developer(1, "Alex", "DEV", 1250, ["Python", "Java", "SQL"], "senior")
        
        skills = []
        for skill in dev:
            skills.append(skill)
        
        assert skills == ["Python", "Java", "SQL"]


class TestSalesperson:
    def test_salesperson_salary_calculation(self):
        salesperson = Salesperson(3, "Peter", "SAL", 4000, 0.15, 50000)
        
        salary = salesperson.calculate_salary()
        
        assert salary == 11500  # 4000 + (50000 * 0.15)
    
    def test_salesperson_update_sales(self):
        salesperson = Salesperson(3, "Peter", "SAL", 4000, 0.15, 50000)
        
        salesperson.update_sales(10000)
        
        assert salesperson.sales_volume == 60000
        assert salesperson.calculate_salary() == 13000  # 4000 + (60000 * 0.15)
    
    def test_salesperson_get_info_includes_commission(self):
        salesperson = Salesperson(3, "Peter", "SAL", 4000, 0.15, 50000)
        
        info = salesperson.get_info()
        
        assert "процент комиссии: 15.0%" in info
        assert "объём продаж: 50000.00" in info
    
    def test_salesperson_invalid_commission_rate(self):
        with pytest.raises(ValueError) as error1:
            Salesperson(3, "Peter", "SAL", 4000, 1.5, 50000)  # > 1
        
        with pytest.raises(ValueError) as error2:
            Salesperson(3, "Peter", "SAL", 4000, -0.1, 50000)  # < 0
            
        print(error1, error2)


class TestEmployeeBuilder:

    def test_employee_builder_method(self):
        
        employee = EmployeeBuilder().with_id(1).with_name("Alex").with_department("IT").with_base_salary(5000).build()
        assert isinstance(employee, Employee)
        
        manager = EmployeeBuilder().with_id(2).with_name("Bob").with_department("MAN").with_base_salary(7000).with_bonus(2000).build()
        assert isinstance(manager, Manager)
        assert manager.calculate_salary() == 9000
        
        developer = EmployeeBuilder().with_id(3).with_name("Peter").with_department("DEV").with_base_salary(5000).add_skill("Python").with_seniority_level('senior').build()
        assert isinstance(developer, Developer)
        assert developer.calculate_salary() == 10000
        
        salesperson = EmployeeBuilder().with_id(4).with_name("Darth Vader").with_department("Death Star").with_base_salary(10000).with_commission_rate(0.5).with_sales_volume(20000).build()
        assert isinstance(salesperson, Salesperson)
        assert salesperson.calculate_salary() == 20000
        
    def test_employee_builder_missing_states(self):
        with pytest.raises(ValueError) as error:
            EmployeeBuilder().with_id(1).with_name("Alex").with_department("IT").build()
        print(error)
        
    def test_employee_builder_wrong_states(self):
        with pytest.raises(ValueError) as error:
            EmployeeBuilder().with_id(2).with_name("Bob").with_department("MAN").with_base_salary(7000).with_bonus(2000).add_skill("skill").build()
        print(error)


class TestPolymorphicBehavior:

    def test_polymorphic_behavior(self):

        employees = [
            Employee(1, "Bob", "IT", 5000),
            Manager(2, "Daniel", "MAN", 7000, 2000),
            Developer(3, "Peter", "DEV", 5000, ["Python"], "senior"),
            Salesperson(4, "Darth Vader", "SAL", 4000, 0.15, 50000)
        ]
        
        total_salary = sum(emp.calculate_salary() for emp in employees)
        
        expected = 5000 + 9000 + 10000 + 11500
        assert total_salary == expected
        assert employees[0].calculate_salary() == 5000
        assert employees[1].calculate_salary() == 9000
        assert employees[2].calculate_salary() == 10000
        assert employees[3].calculate_salary() == 11500
        
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])