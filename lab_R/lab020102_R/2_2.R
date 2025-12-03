calc_polygon_area <- function(x, y, n) {
  area <- 0
  j <- n
  for (i in 1:n) {
    area <- area + (x[j] + x[i]) * (y[j] - y[i])
    j <- i
  }
  return(abs(area / 2))
}
main <- function() {
  cat("Введите количество вершин многоугольника:\n ")
  n <- as.integer(readline())
  x <- numeric(n)
  y <- numeric(n)
  cat("Введите координаты вершин (против часовой стрелки):\n")
  for (i in 1:n) {
    cat("Вершина", i, "(x y):\n ")
    coords <- as.numeric(strsplit(readline(), " ")[[1]])
    x[i] <- coords[1]
    y[i] <- coords[2]
  }
  area <- calc_polygon_area(x, y, n)
  cat("Площадь многоугольника:", area, "\n")
}
main()