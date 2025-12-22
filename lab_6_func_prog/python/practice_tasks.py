from functools import wraps, reduce
import math

students = [
    {'name': 'Alice', 'grade': 85, 'age': 20},
    {'name': 'Bob', 'grade': 92, 'age': 22},
    {'name': 'Charlie', 'grade': 78, 'age': 19},
    {'name': 'Diana', 'grade': 95, 'age': 21},
    {'name': 'Eve', 'grade': 88, 'age': 20}
]

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        f_name = func.__name__
        f_arguments = args, kwargs
        f_results = func(*args, **kwargs)
        return {'Name': f_name,
                'Arguments': f_arguments,
                'Results': f_results}
    return wrapper

@logger
def logged_analyze_students(students):
    average = 0
    number = 0
    high_grades = []
    for student in students:
        grade = student['grade']
        average += grade
        number += 1
        if grade >= 90:
            high_grades.append({"name": student['name'], "grade": student['grade']})
    average = average / number
    return {
        "Average grade": average,
        "High grades": high_grades,
        "Quantity": number
    }
    
def analyze_students(students):
    average = 0
    number = 0
    high_grades = []
    for student in students:
        grade = student['grade']
        average += grade
        number += 1
        if grade >= 90:
            high_grades.append({"name": student['name'], "grade": student['grade']})
    average = average / number
    return {
        "Average grade": average,
        "High grades": high_grades,
        "Quantity": number
    }

def prime_generator(limit=10000):
    primes = [2]
    
    def next_number(num):
        primes_to_check = [p for p in primes if p <= math.isqrt(num)]
        if not primes_to_check:
            primes.append(num)
            return True
        is_prime = all(num % prime != 0 for prime in primes_to_check)
        if is_prime:
            primes.append(num)
        return True

    check_next = 3
    generated_count = 1 
    
    while generated_count < limit:
        next_number(check_next)
        check_next += 2
        generated_count = len(primes)
        if check_next > 10**9:
            break
    return primes[:limit]
        

print(analyze_students(students))
print('\n')
print(logged_analyze_students(students))
print('\n')
print(prime_generator(100))