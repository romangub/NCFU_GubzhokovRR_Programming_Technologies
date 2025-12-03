foo <- function(n) {
  if (n <= 0) {
    return(1)
  } else {
    return(n * foo(n - 1))
  }
}

result <- foo(7)
cat("Результат для n = 7:", result, "\n")