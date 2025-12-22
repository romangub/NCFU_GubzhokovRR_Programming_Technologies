object Comparison {

  // Модель данных
  case class User(id: Int, name: String, email: String)
  case class Product(id: Int, name: String, price: Double, category: String)
  case class OrderItem(product: Product, quantity: Int)
  case class Order(id: Int, user: User, items: List[OrderItem], status: String)

  // Пример данных
  val users = List(
    User(1, "John Doe", "john@example.com"),
    User(2, "Jane Smith", "jane@example.com")
  )

  val products = List(
    Product(1, "iPhone", 999.99, "electronics"),
    Product(2, "MacBook", 1999.99, "electronics"),
    Product(3, "T-shirt", 29.99, "clothing")
  )

  val orders = List(
    Order(1, users(0), List(OrderItem(products(0), 1), OrderItem(products(2), 2)), "completed"),
    Order(2, users(1), List(OrderItem(products(1), 1)), "pending")
  )

  // Функции обработки
  def calculateOrderTotal(order: Order): Double = 
    order.items.map(item => item.product.price * item.quantity).sum

  def filterOrdersByStatus(orders: List[Order], status: String): List[Order] = 
    orders.filter(_.status == status)

  def getTopExpensiveOrders(orders: List[Order], n: Int): List[Order] = 
    orders.sortBy(calculateOrderTotal)(Ordering[Double].reverse).take(n)

  def applyDiscount(order: Order, discount: Double): Order = {
    val discountedItems = order.items.map { item =>
      item.copy(product = item.product.copy(price = item.product.price * (1 - discount)))
    }
    order.copy(items = discountedItems)
  }

  def groupOrdersByUser(orders: List[Order]): Map[User, List[Order]] = 
    orders.groupBy(_.user)

  def main(args: Array[String]): Unit = {
    println("=== Обработка заказов на Scala ===")
    
    val completedOrders = filterOrdersByStatus(orders, "completed")
    val totalRevenue = completedOrders.map(calculateOrderTotal).sum
    val topOrders = getTopExpensiveOrders(orders, 2)
    val groupedOrders = groupOrdersByUser(orders)
    
    println(s"Общая выручка: $totalRevenue")
    println(s"Топ заказы: ${topOrders.map(calculateOrderTotal)}")
    println(s"Заказы по пользователям: ${groupedOrders.map { case (user, orders) => (user.name, orders.length) }}")
  }
}

