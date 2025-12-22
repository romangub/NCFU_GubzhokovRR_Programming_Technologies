numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

students = [
    {'name': 'Alice', 'grade': 85, 'age': 20},
    {'name': 'Bob', 'grade': 92, 'age': 22},
    {'name': 'Charlie', 'grade': 78, 'age': 19},
    {'name': 'Diana', 'grade': 95, 'age': 21},
    {'name': 'Eve', 'grade': 88, 'age': 20}
]

squares = [x * x for x in numbers]
print(f"Квадраты: {squares}")

even_squares = [x * x for x in numbers if x % 2 == 0]
print(f"Квадраты четных: {even_squares}")

student_dict = {student['name']: student['grade'] for student in students}
print(f"Словарь студентов: {student_dict}")

unique_ages = {student['age'] for student in students}
print(f"Уникальные возрасты: {unique_ages}")

def fibonacci_generator(limit):
    """Генератор чисел Фибоначчи"""
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1
        
print("Числа Фибоначчи:")
fib_gen = fibonacci_generator(10)
for num in fib_gen:
    print(num, end=" ")

squares_gen = (x * x for x in numbers)
print(f"Генератор квадратов: {list(squares_gen)}")