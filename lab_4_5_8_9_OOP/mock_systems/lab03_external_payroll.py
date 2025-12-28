from typing import Dict, Any

class PayrollSystem:
    
    tax_rate = 0.13
        
    def calculate_payroll(self, emp_data: Dict[str, Any]) -> float:
        hourly_rate = emp_data.get("hourly_rate", 0.0)
        hours = emp_data.get("hours_worked", 160.0)
        overtime = emp_data.get("overtime_hours", 0.0)
        bonus = emp_data.get("bonus", 0.0)
        
        gross = (hourly_rate * hours) + (hourly_rate * 1.5 * overtime) + bonus
        net = gross * (1 - self.tax_rate)
        
        return net