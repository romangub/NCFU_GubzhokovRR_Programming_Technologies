library(parallel)

mean_of_rnorm <- function(n) {
  random_numbers <- rnorm(n)
  mean(random_numbers)
}

cl <- makeCluster(detectCores() - 1) 

clusterExport(cl, "mean_of_rnorm")

result <- parSapply(cl, rep(10000, 50), mean_of_rnorm)

stopCluster(cl)

print(summary(result))