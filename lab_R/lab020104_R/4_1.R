my_vector <- c(21, 18, 21, 19, 25, 20, 17, 17, 18, 22, 17, 18, 18, 19, 19, 27, 21, 20, 24, 17, 15, 24, 24, 29, 19, 14, 21, 17, 19, 18, 18, 20, 21, 21, 19, 17, 21, 13, 17, 13, 23, 15, 23, 24, 16, 17, 25, 24, 22)
mean_value <- mean(my_vector)
sd_value <- sd(my_vector)

my_vector2 <- my_vector[abs(my_vector - mean_value) < sd_value]

cat("Исходный вектор my_vector:\n")
print(my_vector)
cat("\nСреднее значение:", mean_value, "\n")
cat("Стандартное отклонение:", sd_value, "\n")
cat("\nНовый вектор my_vector2:\n")
print(my_vector2)
cat("\nКоличество элементов в my_vector:", length(my_vector))
cat("\nКоличество элементов в my_vector2:", length(my_vector2), "\n")