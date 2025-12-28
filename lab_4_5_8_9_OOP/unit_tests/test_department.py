import pytest
import sys

project_path = "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP"
sys.path.insert(0, project_path)

from source.lab0202_employee import Employee
from source.lab0203_department import Department
from source.lab0202_manager import Manager
from source.lab0202_developer import Developer
from source.lab0202_salesperson import Salesperson


class TestDepartment:
    def test_department_add_employee(self):
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp)
        
        assert len(dept) == 1
        assert emp in dept
    
    def test_department_remove_employee(self):
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp)
        dept.remove_employee(1)
        
        assert len(dept) == 0
    
    def test_department_get_employees(self):
        dept = Department("IT")
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "IT", 6000)
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        employees = dept.get_employees()

        assert len(employees) == 2
        assert employees[0]['ID'] == 1
        assert employees[1]['ID'] == 2
    
    def test_department_calculate_total_salary_polymorphic(self):
        dept = Department("Development")
        emp = Employee(1, "Mark", "SAL", 5000)
        manager = Manager(2, "Luke", "DEV", 7000, 2000)
        developer = Developer(3, "Oliver", "DEV", 5000, ["Python"], "senior")
        salesperson = Salesperson(4, "Govard", "SAL", 4000, 0.15, 50000)
        
        dept.add_employee(emp)
        dept.add_employee(manager)
        dept.add_employee(developer)
        dept.add_employee(salesperson)

        total = dept.calculate_total_salary()
        
        expected = emp.calculate_salary() + manager.calculate_salary() + developer.calculate_salary() + salesperson.calculate_salary()
        assert total == expected
    
    def test_department_get_employee_count(self):
        dept = Department("Development")
        manager = Manager(1, "Luke", "DEV", 7000, 2000)
        developer1 = Developer(2, "Oliver", "DEV", 5000, ["Python"], "senior")
        developer2 = Developer(3, "Govard", "DEV", 5000, ["Java"], "middle")
        
        dept.add_employee(manager)
        dept.add_employee(developer1)
        dept.add_employee(developer2)
        
        counts = dept.get_employee_count()
        
        assert counts["Manager"] == 1
        assert counts["Developer"] == 2
    
    def test_department_find_employee_by_id(self):
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp)  
        found = dept.find_employee_by_id(1)
        
        assert found is not None
        assert found.id == 1
        assert found.name == "John"
    
    def test_department_find_employee_by_id_not_found(self):
        dept = Department("IT")
        found = dept.find_employee_by_id(999)
        assert found is None


class TestEmployeeMagicMethods:
    
    def test_employee_equality(self):
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(1, "Jane", "HR", 4000)
        emp3 = Employee(2, "Oliver", "IT", 5000) 
        
        assert emp1 == emp2 
        assert emp1 != emp3 
    
    def test_employee_salary_comparison(self):
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)

        assert emp1 < emp2
        assert emp2 > emp1
    
    def test_employee_addition(self):
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)
        
        result = emp1 + emp2

        assert result == 11000
    
    def test_employee_radd(self):
        employees = [
            Employee(1, "John", "IT", 5000),
            Employee(2, "Jane", "HR", 6000),
            Employee(3, "Oliver", "IT", 7000)
        ]

        total = sum(employees)

        assert total == 18000


class TestDepartmentMagicMethods:
    def test_department_magic_methods(self):
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        
        dept.add_employee(emp)
        
        assert len(dept) == 1
        assert dept[0] == emp
        assert emp in dept
    
    def test_department_iteration(self):
        dept = Department("IT")
        employees = [Employee(i, f"Emp{i}", "IT", 5000) for i in range(1, 4)]
        
        for emp in employees:
            dept.add_employee(emp)

        count = 0
        for employee in dept:
            count += 1

        assert count == 3
    
    def test_department_getitem_index_error(self):
        dept = Department("IT")

        with pytest.raises(IndexError) as error:
            _ = dept[0]
        print(error)


class TestDeveloperSkillsIteration:
    def test_developer_skills_iteration(self):
        dev = Developer(1, "John", "DEV", 5000, ["Python", "Java", "SQL"], "senior")

        skills = []
        for skill in dev:
            skills.append(skill)

        assert skills == ["Python", "Java", "SQL"]


class TestEmployeeSerialization:
    def test_employee_serialization(self):
        emp = Employee(1, "John", "IT", 5000)
        data = emp.to_dict()
        new_emp = Employee.from_dict(data)

        assert new_emp.id == emp.id
        assert new_emp.name == emp.name
        assert new_emp.department == emp.department
        assert new_emp.base_salary == emp.base_salary
    
    def test_manager_serialization(self):
        manager = Manager(1, "John", "MAN", 7000, 2000)
        data = manager.to_dict()
        new_manager = Manager.from_dict(data)

        assert new_manager.bonus == 2000
        assert new_manager.calculate_salary() == 9000
    
    def test_developer_serialization(self):
        dev = Developer(1, "John", "DEV", 5000, ["Python", "Java"], "senior")
        data = dev.to_dict()
        new_dev = Developer.from_dict(data)

        assert new_dev.tech_stack == ["Python", "Java"]
        assert new_dev.seniority_level == "senior"


class TestEmployeeSorting:
    def test_employee_sorting(self):
        employees = [
            Employee(3, "Oliver", "IT", 7000),
            Employee(1, "Luke", "HR", 5000),
            Employee(2, "Govard", "IT", 6000)
        ]

        sorted_by_name = sorted(employees, key=lambda x: x.name)
        assert sorted_by_name[-1].name == "Oliver"

        sorted_by_salary = sorted(employees, key=lambda x: x.calculate_salary())
        assert sorted_by_salary[0].calculate_salary() == 5000
    
    def test_employee_sorting_using_lt(self):
        employees = [
            Employee(3, "Govard", "IT", 7000),
            Employee(1, "Luke", "HR", 5000),
            Employee(2, "Oliver", "IT", 6000)
        ]   
        sorted_employees = sorted(employees)

        assert sorted_employees[0].calculate_salary() == 5000
        assert sorted_employees[1].calculate_salary() == 6000
        assert sorted_employees[2].calculate_salary() == 7000


class TestDepartmentIntegration:
    def test_department_integration(self):
        dept = Department("Development")
        
        manager = Manager(1, "Luke", "DEV", 7000, 2000)
        developer = Developer(2, "Oliver", "DEV", 5000, ["Python"], "senior")
        
        dept.add_employee(manager)
        dept.add_employee(developer)

        total_salary = dept.calculate_total_salary()
        expected = manager.calculate_salary() + developer.calculate_salary()

        assert total_salary == expected
        assert dept.get_employee_count()["Manager"] == 1
        assert dept.get_employee_count()["Developer"] == 1
        assert len(dept) == 2
        assert manager in dept
        assert developer in dept
        assert dept[0] == manager
        assert dept[1] == developer


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])