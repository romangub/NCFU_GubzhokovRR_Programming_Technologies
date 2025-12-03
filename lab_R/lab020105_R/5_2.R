library(repurrrsive)
library(purrr)

result_map <- map(1:3, ~ .x * 2)
print("map():")
print(result_map)

result_dbl <- map_dbl(1:3, ~ .x * 2)
print("map_dbl():")
print(result_dbl)

cat("\n")

result_chr <- map_chr(1:3, ~ paste0("Number_", .x))
print("map_chr():")
print(result_chr)

cat("\n")

result_int <- map_int(1:3, ~ as.integer(.x * 2))
print("map_int():")
print(result_int)

cat("\n")

result_lgl <- map_lgl(1:3, ~ .x > 1)
print("map_lgl():")
print(result_lgl)

cat("\n")

result_dfr <- map_dfr(1:3, ~ data.frame(number = .x, square = .x^2))
print("map_dfr():")
print(result_dfr)

cat("\n")

print("walk() - вывод квадратов чисел:")
walk(1:3, ~ print(.x^2))