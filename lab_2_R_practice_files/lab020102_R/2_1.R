calc <- function(shape, params) {
  if (shape == "квадрат") {
    a <- as.numeric(params[1])
    return(list(area = a * a, solution = paste("Площадь квадрата = сторона × сторона =", a, "×", a, "=", a * a)))
  } else if (shape == "прямоугольник") {
    a <- as.numeric(params[1])
    b <- as.numeric(params[2])
    return(list(area = a * b, solution = paste("Площадь прямоугольника = длина × ширина =", a, "×", b, "=", a * b)))
  } else if (shape == "круг") {
    r <- as.numeric(params[1])
    area <- pi * r * r
    return(list(area = area, solution = paste("Площадь круга = π × радиус² = 3.14159 ×", r, "×", r, "=", round(area, 2))))
  } else if (shape == "треугольник") {
    a <- as.numeric(params[1])
    h <- as.numeric(params[2])
    area <- 0.5 * a * h
    return(list(area = area, solution = paste("Площадь треугольника = ½ × основание × высота = 0.5 ×", a, "×", h, "=", area)))
  }
}

shapes <- c("квадрат", "прямоугольник", "круг", "треугольник")
attempts <- 0

while (attempts < 3) {
  cat("Введите название фигуры (квадрат, прямоугольник, круг, треугольник):\n ")
  shape <- tolower(readline())
  
  if (shape %in% shapes) {
    if (shape == "квадрат") {
      cat("Введите длину стороны:\n ")
      a <- as.numeric(readline())
      result <- calc(shape, c(a))
    } 
    else if (shape == "прямоугольник") {
      cat("Введите длину и ширину через пробел:\n ")
      sides <- as.numeric(strsplit(readline(), " ")[[1]])
      result <- calc(shape, sides)
    } 
    else if (shape == "круг") {
      cat("Введите радиус:\n ")
      r <- as.numeric(readline())
      result <- calc(shape, c(r))
    } 
    else if (shape == "треугольник") {
      cat("Введите основание и высоту через пробел:\n ")
      params <- as.numeric(strsplit(readline(), " ")[[1]])
      result <- calc(shape, params)
    }
    
    cat("\nРезультат:\n")
    cat(result$solution, "\n")
    cat("Площадь:", result$area, "\n")
    break  # Выход из цикла после успешного расчета
    
  } else {
    attempts <- attempts + 1
    cat("Некорректное название фигуры. Попыток осталось:", 3 - attempts, "\n\n")
  }
}

if (attempts == 3) {
  cat("Превышено количество некорректных попыток. Программа завершена.\n")
}