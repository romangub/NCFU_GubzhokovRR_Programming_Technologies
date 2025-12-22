// Main.scala
object Main {

  def main(args: Array[String]): Unit = {
    println("=== Scala Функциональное Программирование ===")
    println()

    // Базовые операции
    println("1. Базовый синтаксис Scala:")
    BasicScala.main(Array())
    println()

    // Коллекции
    println("2. Работа с коллекциями:")
    Collections.demonstrateCollections()
    println()

    // Обработка ошибок
    println("3. Обработка ошибок:")
    ErrorHandling.demonstrateErrorHandling()
    println()

    // Pattern matching
    println("4. Pattern Matching:")
    PatternMatching.demonstratePatternMatching()
    println()

    // Практические задания
    println("5. Практические задания:")
    PracticalTasks.demonstratePracticalTasks()
    println()

    // Spark (требует установленного Spark)
    // Раскомментируйте, если Spark установлен
    // println("6. Apache Spark:")
    // SparkExample.main(Array())
  }
}


