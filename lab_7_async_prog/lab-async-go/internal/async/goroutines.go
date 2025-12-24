package main

import (
	"fmt"
	"sync"
	"time"
)

// Горутина с передачей параметра и использованием WaitGroup
func processItem(itemID int, wg *sync.WaitGroup) {
	defer wg.Done() // Уменьшаем счетчик при завершении

	fmt.Printf("Горутина начала обработку элемента %d\n", itemID)

	// Имитация работы с разным временем выполнения
	processingTime := time.Duration(100+itemID*50) * time.Millisecond
	time.Sleep(processingTime)

	fmt.Printf("Горутина завершила обработку элемента %d за %v\n",
		itemID, processingTime)
}

func main() {
	var wg sync.WaitGroup
	totalItems := 5

	fmt.Println("=== Запуск 5 горутин для параллельной обработки ===")

	// Запускаем горутины с передачей параметра (ID элемента)
	for i := 1; i <= totalItems; i++ {
		wg.Add(1) // Увеличиваем счетчик перед запуском каждой горутины
		go processItem(i, &wg)
	}

	fmt.Println("Все горутины запущены, ожидаем завершения...")

	wg.Wait() // Ожидаем завершения всех горутин

	fmt.Println("=== Все горутины успешно завершили работу ===")
}
