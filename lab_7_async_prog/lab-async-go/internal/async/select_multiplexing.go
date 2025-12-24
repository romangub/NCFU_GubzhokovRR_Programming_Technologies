// task_2_2_select_multiplexing.go
package main

import (
	"fmt"
	"math/rand"
	"time"
)

// Генератор сообщений с случайными интервалами
func messageGenerator(name string, ch chan<- string) {
	for i := 1; i <= 5; i++ {
		delay := time.Duration(rand.Intn(1000)) * time.Millisecond
		time.Sleep(delay)

		msg := fmt.Sprintf("Сообщение %d от %s", i, name)
		ch <- msg
	}
	close(ch)
}

// Обработчик сообщений с таймаутом и мультиплексированием
func messageProcessor(ch1, ch2 <-chan string) {
	timeout := time.After(3 * time.Second)
	processedCount := 0

	fmt.Println("=== Начало обработки сообщений ===")
	fmt.Println("Таймаут установлен на 3 секунды")

	for {
		select {
		case msg, ok := <-ch1:
			if !ok {
				fmt.Println("Канал 1 закрыт")
				ch1 = nil // Устанавливаем в nil, чтобы этот case больше не выполнялся
			} else {
				fmt.Printf("📨 Из канала 1: %s\n", msg)
				processedCount++
			}

		case msg, ok := <-ch2:
			if !ok {
				fmt.Println("Канал 2 закрыт")
				ch2 = nil // Устанавливаем в nil, чтобы этот case больше не выполнялся
			} else {
				fmt.Printf("📨 Из канала 2: %s\n", msg)
				processedCount++
			}

		case <-timeout:
			fmt.Println("⏰ Таймаут! Прерываем обработку")
			fmt.Printf("Всего обработано сообщений: %d\n", processedCount)
			return

		case <-time.After(500 * time.Millisecond):
			// Периодическая проверка состояния
			fmt.Println("⏳ Ожидание сообщений...")

		default:
			// Если оба канала закрыты, завершаем работу
			if ch1 == nil && ch2 == nil {
				fmt.Println("✅ Оба канала закрыты, обработка завершена")
				fmt.Printf("Итог: обработано %d сообщений\n", processedCount)
				return
			}
		}
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())

	// Создаем два канала для сообщений
	channelA := make(chan string)
	channelB := make(chan string)

	// Запускаем генераторы сообщений
	go messageGenerator("Генератор-A", channelA)
	go messageGenerator("Генератор-B", channelB)

	// Запускаем обработчик
	messageProcessor(channelA, channelB)

	fmt.Println("=== Программа завершена ===")
}
