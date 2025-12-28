import pytest
import sys

project_path = "C:/Users/DezerTear/Desktop/uni/progtech/lab_4_5_8_9_OOP"
sys.path.insert(0, project_path)

from source.lab0202_employee import Employee

class TestEmployee:
    def test_init_emp(self):
         
        result = "Все данные корректны!"
        print("   Инициализация работника...")
        emp = Employee(1, "Andrew", "IT", 1000)
        
        try:
            assert emp.id == 1
            assert emp.name == "Andrew"
            assert emp.department == "IT"
            assert emp.base_salary == 1000
            assert emp.calculate_salary() == 1000
        except Exception:
            result = "Ошибка ввода"
        
        print(f"   {result}")
         

    def test_emp_errors(self):
        with pytest.raises(ValueError) as exc_info:
            Employee(-1, "Andrew", "IT", 1000)

        print(f"   Тип исключения: {type(exc_info.value).__name__}")
        print(f"   Сообщение: {exc_info.value}")
        
         
        
        with pytest.raises(ValueError) as exc_info2 :
            Employee(0, "Andrew", "IT", 1000)
        
        print(f"   Сообщение: {exc_info2.value}")
        
         
            
    
    def test_emp_salary_error(self):
        
         
        
        with pytest.raises(ValueError) as exc_info:
            Employee(1, "Andrew", "IT", -1000)
        
        print(f"   Тип исключения: {type(exc_info.value).__name__}")
        print(f"   Сообщение: {exc_info.value}")
        
         
    
    def test_emp_no_name(self):
         
        with pytest.raises(ValueError) as exc_info:
            Employee(1, "", "IT", 1000)
            
        print(f"   Тип исключения: {type(exc_info.value).__name__}")
        print(f"   Сообщение: {exc_info.value}")
         
        
        with pytest.raises(ValueError) as exc_info1:
            Employee(1, "   ", "IT", 1000)
            
        print(f"   Тип исключения: {type(exc_info1.value).__name__}")
        print(f"   Сообщение: {exc_info1.value}")
         
    
    def test_emp_salary(self):
        emp = Employee(1, "Andrew", "IT", 1000)
        
        salary = emp.calculate_salary()
        
        assert salary == 1000
    
    def test_emp_str(self):
        emp = Employee(1, "Andrew", "IT", 1000)

        result = str(emp)

        expected = "Сотрудник [id: 1, имя: Andrew, отдел: IT, зарплата: 1000.00]"
        assert result == expected
    
    def test_emp_id_valid(self):
        emp = Employee(1, "Andrew", "IT", 1000)
        
        emp.id = 2
        assert emp.id == 2
        
        with pytest.raises(ValueError):
            emp.id = -1
        
        with pytest.raises(ValueError):
            emp.id = 0
    
    def test_emp_name_valid(self):
        emp = Employee(1, "Andrew", "IT", 1000)
        
        emp.name = "Bob"
        assert emp.name == "Bob"
        
        with pytest.raises(ValueError):
            emp.name = ""
        
        with pytest.raises(ValueError):
            emp.name = "   "
    
    def test_employee_salary_valid(self):
        emp = Employee(1, "Andrew", "IT", 1000)
        
        emp.base_salary = 6000
        assert emp.base_salary == 6000
        
        with pytest.raises(ValueError):
            emp.base_salary = -1000
    
    def test_employee_dept_valid(self):
        emp = Employee(1, "Andrew", "IT", 1000)
        
        emp.department = "HR"
        assert emp.department == "HR"
        
        with pytest.raises(ValueError):
            emp.department = ""
        
        with pytest.raises(ValueError):
            emp.department = "   "
    
    def test_emp_get_info(self):
        emp = Employee(1, "Andrew", "IT", 1000)
        
        info = emp.get_info()
        
        assert "Andrew" in info
        assert "1000" in info
        assert "зарплата" in info
        
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])