square_calc <- function(a) {
  s <- a * a # nolint
  return(s)
}

rect_calc <- function(a, b) {
  s <- a * b
  return(s)
}

circle_calc <- function(a) {
  s <- pi * a * a
  return(s)
}

cat("Введите длину стороны квадрата: ", "\n")
sq_a <- as.numeric(readline())

cat("Введите длины двух сторон прямоугольника через пробел: ", "\n")
re_data <- readline()
re_sides <- strsplit(re_data, " ")[[1]]

re_a <- as.numeric(re_sides[1])
re_b <- as.numeric(re_sides[2])

cat("Введите радиус круга: ", "\n")
ci_a <- as.numeric(readline())

sq_s <- square_calc(sq_a)
re_s <- rect_calc(re_a, re_b)
ci_s <- circle_calc(ci_a)
total <- sq_s + re_s + ci_s

cat("Площадь квадрата:", sq_s, "\n")
cat("Площадь прямоугольника:", re_s, "\n")
cat("Площадь круга:", ci_s, "\n")
cat("Общая площадь всех фигур:", total, "\n")