named_sw_films <- sw_films %>%
  set_names(map_chr(sw_films, "title"))

str(named_sw_films, max.level = 1)

print("Доступ по имени:")
print(named_sw_films[["A New Hope"]]$director)

print("Доступ по индексу:")
print(named_sw_films[[1]]$director)

print("Названия фильмов:")
print(names(named_sw_films))