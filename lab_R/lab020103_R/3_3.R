library(R6)

PiggyBank <- R6Class(
  "PiggyBank",
  public = list(
    volume = 1000,
    coins = list(),
    broken = FALSE,
    initialize = function(volume = 1000) {
      stopifnot(is.numeric(volume), volume > 0)
      self$volume <- volume
    },
    add_coin = function(value, volume) {
      if (self$broken) {
        cat("Копилка разбита!\n")
        return(invisible(self))
      }
      current_volume <- self$get_current_volume()
      if (current_volume + volume > self$volume) {
        cat("Недостаточно места в копилке!\n")
        return(invisible(self))
      }
      self$coins <- append(self$coins, list(list(value = value, volume = volume)))
      cat(sprintf("Монета %.0f руб (объем %.0f) добавлена\n", value, volume))
      invisible(self)
    },
    break_bank = function() {
      if (self$broken) {
        cat("Копилка уже разбита!\n")
        return(invisible(self))
      }
      total <- self$get_total_value()
      cat(sprintf("Копилка разбита! Сумма: %.0f руб\n", total))
      self$broken <- TRUE
      q("no", status = 0)
    },
    get_status = function() {
      current_volume <- self$get_current_volume()
      total_value <- self$get_total_value()
      cat(sprintf("Объем: %.0f/%.0f, Сумма: %.0f руб, Состояние: %s\n",
                  current_volume, self$volume, total_value,
                  ifelse(self$broken, "разбита", "цела")))
      invisible(self)
    },
    get_current_volume = function() {
      if (length(self$coins) == 0) return(0)
      sum(vapply(self$coins, function(coin) coin$volume, numeric(1)))
    },
    get_total_value = function() {
      if (length(self$coins) == 0) return(0)
      sum(vapply(self$coins, function(coin) coin$value, numeric(1)))
    }
  )
)

bank <- PiggyBank$new(500)

bank$get_status()
bank$add_coin(10, 50)$add_coin(5, 30)$add_coin(2, 20)
bank$get_status()
bank$add_coin(1, 10)$add_coin(50, 100)
bank$get_status()

bank$add_coin(100, 400)
bank$break_bank()

cat("Этот текст не появится\n")