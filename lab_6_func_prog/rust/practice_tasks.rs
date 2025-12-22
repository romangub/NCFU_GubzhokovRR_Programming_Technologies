use std::error::Error;
use std::fmt;

// Структуры данных для заданий
#[derive(Debug, Clone)]
struct Product {
    name: String,
    price: f64,
    available: bool,
}

#[derive(Debug, Clone)]
struct Order {
    id: u32,
    amount: f64,
    customer_id: u32,
    status: OrderStatus,
}

#[derive(Debug, Clone)]
enum OrderStatus {
    Pending,
    Processing,
    Completed,
    Cancelled,
}

#[derive(Debug)]
enum OrderError {
    InvalidAmount(f64),
    InvalidCustomer(u32),
    InvalidStatus(String),
}

impl fmt::Display for OrderError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            OrderError::InvalidAmount(amount) => write!(f, "Invalid order amount: {}", amount),
            OrderError::InvalidCustomer(customer_id) => write!(f, "Invalid customer ID: {}", customer_id),
            OrderError::InvalidStatus(status) => write!(f, "Invalid order status: {}", status),
        }
    }
}

impl Error for OrderError {}

// Задание 1: Анализ продуктов
fn analyze_products(products: &[Product]) -> (f64, usize, Vec<&Product>) {
    let mut total_price = 0.0;
    let mut available_count = 0;
    let mut expensive_products = Vec::new();
    
    for product in products {
        total_price += product.price;
        
        if product.available {
            available_count += 1;
        }
        
        if product.price > 100.0 {
            expensive_products.push(product);
        }
    }
    
    let average_price = if !products.is_empty() {
        total_price / products.len() as f64
    } else {
        0.0
    };
    
    (average_price, available_count, expensive_products)
}

// Задание 2: Валидация заказов
fn validate_orders(orders: &[Order]) -> Result<Vec<&Order>, OrderError> {
    let mut valid_orders = Vec::new();
    
    for order in orders {
        // Проверка суммы заказа
        if order.amount <= 0.0 {
            return Err(OrderError::InvalidAmount(order.amount));
        }
        
        // Проверка ID клиента
        if order.customer_id == 0 {
            return Err(OrderError::InvalidCustomer(order.customer_id));
        }
        
        // Проверка статуса заказа
        match &order.status {
            OrderStatus::Cancelled if order.amount > 1000.0 => {
                return Err(OrderError::InvalidStatus(
                    format!("Cannot cancel large order (ID: {}, amount: {})", 
                           order.id, order.amount)
                ));
            }
            _ => {}
        }
        
        valid_orders.push(order);
    }
    
    Ok(valid_orders)
}

// Задание 3: Итератор Фибоначчи
struct Fibonacci {
    current: u64,
    next: u64,
}

impl Fibonacci {
    fn new() -> Self {
        Fibonacci { current: 0, next: 1 }
    }
}

impl Iterator for Fibonacci {
    type Item = u64;
    
    fn next(&mut self) -> Option<Self::Item> {
        let current = self.current;
        
        // Вычисляем следующее число
        let next = self.current.checked_add(self.next)?;
        self.current = self.next;
        self.next = next;
        
        Some(current)
    }
}

// Дополнительные полезные методы для Фибоначчи
impl Fibonacci {
    fn iter_until(max: u64) -> FibonacciUntil {
        FibonacciUntil {
            fib: Fibonacci::new(),
            max,
        }
    }
    
    fn take_safe(n: usize) -> FibonacciTake {
        FibonacciTake {
            fib: Fibonacci::new(),
            remaining: n,
        }
    }
}

// Итератор Фибоначчи с ограничением по максимальному значению
struct FibonacciUntil {
    fib: Fibonacci,
    max: u64,
}

impl Iterator for FibonacciUntil {
    type Item = u64;
    
    fn next(&mut self) -> Option<Self::Item> {
        let value = self.fib.next()?;
        if value > self.max {
            None
        } else {
            Some(value)
        }
    }
}

// Итератор Фибоначчи с ограничением по количеству
struct FibonacciTake {
    fib: Fibonacci,
    remaining: usize,
}

impl Iterator for FibonacciTake {
    type Item = u64;
    
    fn next(&mut self) -> Option<Self::Item> {
        if self.remaining == 0 {
            None
        } else {
            self.remaining -= 1;
            self.fib.next()
        }
    }
}

// Пример использования
fn main() {
    println!("=== Задание 1: Анализ продуктов ===");
    
    let products = vec![
        Product { name: "Laptop".to_string(), price: 999.99, available: true },
        Product { name: "Mouse".to_string(), price: 29.99, available: true },
        Product { name: "Keyboard".to_string(), price: 89.99, available: false },
        Product { name: "Monitor".to_string(), price: 299.99, available: true },
        Product { name: "USB Cable".to_string(), price: 9.99, available: true },
    ];
    
    let (avg_price, available_count, expensive) = analyze_products(&products);
    
    println!("Средняя цена: ${:.2}", avg_price);
    println!("Доступно продуктов: {}", available_count);
    println!("Дорогие продукты (>$100):");
    for product in expensive {
        println!("  - {}: ${:.2}", product.name, product.price);
    }
    
    println!("\n=== Задание 2: Валидация заказов ===");
    
    let orders = vec![
        Order { id: 1, amount: 99.99, customer_id: 101, status: OrderStatus::Pending },
        Order { id: 2, amount: 0.0, customer_id: 102, status: OrderStatus::Processing }, // Ошибка: неверная сумма
        Order { id: 3, amount: 1500.0, customer_id: 103, status: OrderStatus::Cancelled }, // Ошибка: нельзя отменить крупный заказ
        Order { id: 4, amount: 49.99, customer_id: 0, status: OrderStatus::Completed }, // Ошибка: неверный ID клиента
    ];
    
    match validate_orders(&orders) {
        Ok(valid_orders) => {
            println!("Все заказы валидны:");
            for order in valid_orders {
                println!("  - Заказ #{}: ${:.2}", order.id, order.amount);
            }
        }
        Err(error) => {
            println!("Ошибка валидации: {}", error);
        }
    }
    
    // Пример успешной валидации
    let valid_orders = vec![
        Order { id: 1, amount: 99.99, customer_id: 101, status: OrderStatus::Pending },
        Order { id: 2, amount: 49.99, customer_id: 102, status: OrderStatus::Completed },
    ];
    
    match validate_orders(&valid_orders) {
        Ok(valid) => {
            println!("Успешная валидация: {} заказа(ов)", valid.len());
        }
        Err(error) => {
            println!("Ошибка: {}", error);
        }
    }
    
    println!("\n=== Задание 3: Числа Фибоначчи ===");
    
    println!("Первые 10 чисел Фибоначчи:");
    for (i, num) in Fibonacci::new().take(10).enumerate() {
        println!("  F({}) = {}", i, num);
    }
    
    println!("\nЧисла Фибоначчи до 100:");
    for num in Fibonacci::iter_until(100) {
        print!("{} ", num);
    }
    println!();
    
    println!("\nПервые 5 чисел Фибоначчи (безопасный метод):");
    for num in Fibonacci::take_safe(5) {
        print!("{} ", num);
    }
    println!();
    
    // Тестирование переполнения
    println!("\nТестирование переполнения (автоматическая остановка):");
    let mut count = 0;
    for num in Fibonacci::new() {
        print!("{} ", num);
        count += 1;
        if count >= 20 {
            println!("\n(остановлено после 20 чисел)");
            break;
        }
    }
}

