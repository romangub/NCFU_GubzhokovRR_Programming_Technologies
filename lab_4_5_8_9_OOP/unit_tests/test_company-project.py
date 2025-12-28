import pytest
import sys
import os
import tempfile
from pathlib import Path

project_path = "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP"
sys.path.insert(0, project_path)

from source.lab0202_employee import Employee
from source.lab0203_department import Department
from source.lab0204_company import Company
from source.lab0204_project import Project
from source.lab0202_manager import Manager
from source.lab0202_developer import Developer
from source.lab0202_salesperson import Salesperson
from source.lab0204_errors import (
    EmployeeNotFoundError, DepartmentNotFoundError, ProjectNotFoundError,
    InvalidStatusError, DuplicateIdError
)


class TestProject:
    def test_project_team_management(self):
        project = Project(1, "AI Platform", "Разработка AI системы", 100000, "2024-12-31", "2025-03-31", "planning")
        dev = Developer(1, "John", "DEV", 5000, ["Python"], "senior")

        project.add_team_member(dev)

        assert len(project.get_team()) == 1
        assert project.get_team_size() == 1

        project.remove_team_member(1)

        assert len(project.get_team()) == 0
    
    def test_project_total_salary(self):
        project = Project(1, "AI Platform", "Разработка AI системы", 100000, "2024-12-31", "2025-03-31", "planning")
        manager = Manager(1, "Rick", "DEV", 7000, 2000)
        developer = Developer(2, "Robert", "DEV", 5000, ["Python"], "senior")
        
        project.add_team_member(manager)
        project.add_team_member(developer)
        
        total = project.calculate_total_salary()

        expected = manager.calculate_salary() + developer.calculate_salary()
        assert total == expected
    
    def test_project_invalid_status_raises_error(self):

        with pytest.raises(InvalidStatusError) as error:
            Project(1, "Test", "Test", 100000, "2024-12-31", "2025-03-31", "error")
        
        print(error)
            
        valid_statuses = ["planning", "active", "completed", "cancelled"]
        for status in valid_statuses:
            project = Project(1, "Test", "Test", 100000, "2024-12-31", "2025-03-31", status)
            assert project.status == status


class TestCompany:
    def test_company_department_management(self):

        company = Company("TechCorp")
        dept = Department("Development")
        company.add_department(dept)

        assert len(company.get_departments()) == 1
        
        company.remove_department("Development")
        
        assert len(company.get_departments()) == 0
    
    def test_company_find_employee(self):
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000)
        dept.add_employee(emp)
        company.add_department(dept)
        found = company.find_employee_by_id(1)

        assert found is not None
        assert found[0].name == "John"
    
    def test_company_cannot_delete_department_with_employees(self):
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000)
        dept.add_employee(emp)
        company.add_department(dept)

        with pytest.raises(ValueError) as e:
            company.remove_department("Development")
        print(e)
    
    def test_company_duplicate_employee_id_raises_error(self):
        company = Company("TechCorp")
        dept = Department("Development")
        emp1 = Employee(1, "John", "DEV", 5000)
        emp2 = Employee(1, "Jane", "DEV", 6000)
        dept.add_employee(emp1)
        company.add_department(dept)

        with pytest.raises(ValueError) as e:
            dept.add_employee(emp2)
        
        print(e)
    
    def test_company_get_all_employees(self):
        company = Company("TechCorp")
        dept1 = Department("Development")
        dept2 = Department("Sales")
        emp1 = Employee(1, "John", "DEV", 5000)
        emp2 = Employee(2, "Jane", "SAL", 6000)
        dept1.add_employee(emp1)
        dept2.add_employee(emp2)
        company.add_department(dept1)
        company.add_department(dept2)
        all_employees = company.get_all_employees()

        assert len(all_employees) == 2
    
    def test_company_calculate_total_monthly_cost(self):
        company = Company("TechCorp")
        dept = Department("Development")
        manager = Manager(1, "Rick", "DEV", 7000, 2000)
        developer = Developer(2, "Robert", "DEV", 5000, ["Python"], "senior")
        dept.add_employee(manager)
        dept.add_employee(developer)
        company.add_department(dept)
        total_cost = company.calculate_total_monthly_cost()

        expected = manager.calculate_salary() + developer.calculate_salary()
        assert total_cost == expected


class TestCompanySerialization:
    def test_company_serialization_roundtrip(self):
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000)
        
        dept.add_employee(emp)
        company.add_department(dept)

        test_output_dir = Path("test_output")
        test_output_dir.mkdir(exist_ok=True)
        
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.json', 
            delete=False,
            dir=test_output_dir
        ) as f:
            filename = f.name
        
        company.to_json(filename)
            
        print(f"Файл сохранен в: {os.path.abspath(filename)}")
            
        loaded_company = Company.from_json(filename)
            
        assert loaded_company.name == "TechCorp"
        assert len(loaded_company.get_departments()) == 1
        assert len(loaded_company.get_all_employees()) == 1


class TestCompanyBusinessMethods:
    def test_company_department_statistics(self):
        company = Company("TechCorp")
        dept = Department("Development")
        
        manager = Manager(1, "Rick", "DEV", 7000, 2000)
        developer1 = Developer(2, "Robert", "DEV", 5000, ["Python"], "senior")
        developer2 = Developer(3, "Rita", "DEV", 5000, ["Java"], "middle")
        
        dept.add_employee(manager)
        dept.add_employee(developer1)
        dept.add_employee(developer2)
        company.add_department(dept)

        stats = company.get_departments_statistics()

        assert "Development" in stats
        assert stats["Development"]["total_employees"] == 3
        assert stats["Development"]["total_monthly_salary"] > 0
        assert stats["Development"]["employee_types"]["Manager"] == 1
        assert stats["Development"]["employee_types"]["Developer"] == 2


class TestComplexCompanyStructure:
    def test_complex_company_structure(self):
        company = Company("TechInnovations")
        dev_department = Department("Development")
        sales_department = Department("Sales")

        manager = Manager(1, "Rick Johnson", "DEV", 7000, 2000)
        developer = Developer(2, "Robert Smith", "DEV", 5000, ["Python", "SQL"], "senior")
        salesperson = Salesperson(3, "Rita Brown", "SAL", 4000, 0.15, 50000)

        dev_department.add_employee(manager)
        dev_department.add_employee(developer)
        sales_department.add_employee(salesperson)

        company.add_department(dev_department)
        company.add_department(sales_department)

        assert company.calculate_total_monthly_cost() > 0
        assert len(company.get_all_employees()) == 3

        found_employee = company.find_employee_by_id(2)
        assert found_employee is not None
        assert found_employee[0].name == "Robert Smith"
    
    def test_company_project_management(self):
        company = Company("TechCorp")
        dept = Department("Development")
        developer = Developer(1, "Robert", "DEV", 5000, ["Python"], "senior")
        
        dept.add_employee(developer)
        company.add_department(dept)
        
        project = Project(1, "AI Platform", "Разработка AI системы", 100000, "2024-12-31", "2025-03-31", "active")
        company.add_project(project)

        company.assign_employee_to_project(1, 1)

        assert project.get_team_size() == 1
        assert project.calculate_total_salary() == developer.calculate_salary()
    
    def test_company_duplicate_project_id(self):
        company = Company("TechCorp")
        project1 = Project(1, "AI Platform", "Разработка AI системы", 100000, "2024-12-31", "2025-03-31", "planning")
        project2 = Project(1, "AI Platform2", "Разработка AI системы2", 100002, "2024-11-21", "2025-03-11", "active")
        
        company.add_project(project1)

        with pytest.raises(DuplicateIdError):
            company.add_project(project2)
    
    def test_company_cannot_delete_project_with_team(self):
        company = Company("TechCorp")
        dept = Department("Development")
        developer = Developer(1, "Robert", "DEV", 5000, ["Python"], "senior")
        
        dept.add_employee(developer)
        company.add_department(dept)
        
        project = Project(1, "AI Platform", "Разработка AI системы", 100000, "2024-12-31", "2025-03-31", "active")
        company.add_project(project)
        company.assign_employee_to_project(1, 1)

        with pytest.raises(ValueError):
            company.remove_project(1)
            
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])