calc_area <- function(p) {
  UseMethod("calc_area")
}
calc_area.default <- function(p) {
  warning("Невозможно обработать данные")
  return(NA)
}
calc_area.circle <- function(p) {
  return(pi * p[1]^2)
}
calc_area.rect <- function(p) {
  return(p[1] * p[2])
}
calc_area.tri <- function(p) {
  return(0.5 * p[1] * p[2])
}

c1 <- structure(5, class = "circle")
r1 <- structure(c(4, 6), class = "rect")
t1 <- structure(c(3, 4), class = "tri")

cat("Круг:", calc_area(c1), "\n")
cat("Прямоугольник:", calc_area(r1), "\n")
cat("Треугольник:", calc_area(t1), "\n")