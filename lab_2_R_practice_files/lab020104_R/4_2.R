get_negative_values <- function(df) {
  negative_list <- list()
  for (col_name in names(df)) {
    column <- df[[col_name]]
    negative_vals <- column[column < 0 & !is.na(column)]
    if (length(negative_vals) > 0) {
      negative_list[[col_name]] <- negative_vals
    }
  }
  if (length(negative_list) > 0) {
    lengths <- sapply(negative_list, length)
    if (length(unique(lengths)) == 1) {
      result_matrix <- matrix(unlist(negative_list), 
                             nrow = lengths[1], 
                             byrow = FALSE)
      colnames(result_matrix) <- names(negative_list)
      return(result_matrix)
    } else {
      return(negative_list)
    }
  } else {
    return(NULL)
  }
}

test_data1 <- as.data.frame(list(V1 = c(-9.7, -10, -10.5, -7.8, -8.9), 
                                V2 = c(NA, -10.2, -10.1, -9.3, -12.2), 
                                V3 = c(NA, NA, -9.3, -10.9, -9.8)))

test_data2 <- as.data.frame(list(V1 = c(NA, 0.5, 0.7, 8), 
                                V2 = c(-0.3, NA, 2, 1.2), 
                                V3 = c(2, -1, -5, -1.2)))

test_data3 <- as.data.frame(list(V1 = c(NA, -0.5, -0.7, -8), 
                                V2 = c(-0.3, NA, -2, -1.2), 
                                V3 = c(1, 2, 3, NA)))

cat("Тест 1:\n")
print(get_negative_values(test_data1))

cat("\nТест 2:\n")
print(get_negative_values(test_data2))

cat("\nТест 3:\n")
print(get_negative_values(test_data3))