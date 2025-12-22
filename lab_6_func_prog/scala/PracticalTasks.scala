import org.apache.spark.sql.DataFrame

object PracticalTasks {

  // Практическое задание 1: Анализ продаж
  case class SalesRecord(product: String, category: String, amount: Double, date: String)

  def analyzeSales(sales: List[SalesRecord]): Map[String, (Double, Int)] = {
    sales
      .groupBy(_.category)
      .mapValues { records =>
        val totalAmount = records.map(_.amount).sum
        val count = records.length
        (totalAmount, count)
      }
  }

  // Практическое задание 2: Обработка цепочки операций с ошибками
  case class User(id: Int, name: String, email: String)
  case class PaymentMethod(method: String, valid: Boolean)
  case class Order(userId: Int, amount: Double, payment: PaymentMethod)

  val users = Map(
    1 -> User(1, "John Doe", "john@example.com"),
    2 -> User(2, "Jane Smith", "jane@example.com")
  )

  def findUser(userId: Int): Either[String, User] = {
    users.get(userId).toRight(s"User $userId not found")
  }

  def validatePayment(payment: PaymentMethod): Either[String, PaymentMethod] = {
    if (payment.valid) Right(payment)
    else Left(s"Invalid payment method: ${payment.method}")
  }

  def calculateDiscount(amount: Double, user: User): Either[String, Double] = {
    if (amount < 0) Left("Amount cannot be negative")
    else {
      val discount = if (amount > 100) amount * 0.1 else 0.0
      Right(discount)
    }
  }

  def processOrderPipeline(order: Order): Either[String, Double] = {
    for {
      user <- findUser(order.userId)
      validatedPayment <- validatePayment(order.payment)
      discount <- calculateDiscount(order.amount, user)
      finalAmount = order.amount - discount
    } yield finalAmount
  }

  // Практическое задание 3: Spark job для анализа данных
  def createSalesReport(df: DataFrame): DataFrame = {
    import df.sparkSession.implicits._
    import org.apache.spark.sql.functions._

    // Общая выручка по дням
    val dailyRevenue = df
      .groupBy("date")
      .agg(sum("amount").as("daily_revenue"))
      .orderBy("date")

    // Популярные товары (топ-5 по количеству продаж)
    val popularProducts = df
      .groupBy("product")
      .agg(
        count("*").as("sales_count"),
        sum("amount").as("total_revenue")
      )
      .orderBy(desc("sales_count"))
      .limit(5)

    // Средняя цена по категориям
    val avgPriceByCategory = df
      .groupBy("category")
      .agg(
        avg("amount").as("avg_price"),
        sum("amount").as("total_revenue"),
        count("*").as("product_count")
      )
      .orderBy(desc("total_revenue"))

    // Возвращаем комбинированный отчет
    // В реальном сценарии можно объединить через join или вернуть отдельные отчеты
    avgPriceByCategory
  }

  def demonstratePracticalTasks(): Unit = {
    println("=== Практические задания ===")

    // Задание 1: Анализ продаж
    val sales = List(
      SalesRecord("iPhone", "electronics", 999.99, "2024-01-15"),
      SalesRecord("MacBook", "electronics", 1999.99, "2024-01-15"),
      SalesRecord("T-shirt", "clothing", 29.99, "2024-01-16"),
      SalesRecord("Jeans", "clothing", 79.99, "2024-01-16"),
      SalesRecord("Book", "education", 15.99, "2024-01-17")
    )

    val salesAnalysis = analyzeSales(sales)
    println("Анализ продаж по категориям:")
    salesAnalysis.foreach {
      case (category, (total, count)) =>
        println(s"  $category: общая сумма = $total, количество = $count")
    }

    // Задание 2: Обработка цепочки операций
    println("\nОбработка заказов:")
    val orders = List(
      Order(1, 150.0, PaymentMethod("credit_card", true)),
      Order(2, 50.0, PaymentMethod("paypal", true)),
      Order(3, 100.0, PaymentMethod("credit_card", false)), // Невалидный платеж
      Order(999, 200.0, PaymentMethod("credit_card", true)) // Несуществующий пользователь
    )

    orders.foreach { order =>
      val result = processOrderPipeline(order)
      result match {
        case Right(finalAmount) =>
          println(s"  Заказ для пользователя ${order.userId}: финальная сумма = $finalAmount")
        case Left(error) =>
          println(s"  Ошибка обработки заказа ${order.userId}: $error")
      }
    }
  }

  def main(args: Array[String]): Unit = {
    demonstratePracticalTasks()
  }
}


