library(R6)

Microwave <- R6Class(
  "Microwave",
  public = list(
    power = 800,
    door_open = FALSE,
    
    initialize = function(power = 800, door_open = FALSE) {
      stopifnot(is.numeric(power), power > 0)
      stopifnot(is.logical(door_open))
      self$power <- power
      self$door_open <- door_open
    },
    
    open_door = function() {
      self$door_open <- TRUE
      cat("Дверь открыта\n")
      invisible(self)
    },
    
    close_door = function() {
      self$door_open <- FALSE
      cat("Дверь закрыта\n")
      invisible(self)
    },
    
    cook = function() {
      if (self$door_open) {
        cat("Ошибка: дверь открыта!\n")
        return(invisible(self))
      }
      
      t <- 60 / (self$power / 1000)
      cat("Приготовление...\n")
      Sys.sleep(1)
      cat(sprintf("Готово! Время: %.1f сек\n", t))
      invisible(self)
    }
  )
)

m1 <- Microwave$new()
m2 <- Microwave$new(1200, TRUE)

cat("Печь 1:\n")
m1$close_door()$cook()

cat("\nПечь 2:\n")
m2$cook()$close_door()$cook()