package main

import (
	"fmt"
	"sync"
	"time"
)

// Функция отправителя (пишет в канал)
func sender(ch chan<- string, wg *sync.WaitGroup) {
	defer wg.Done()

	messages := []string{"Привет", "из", "горутины", "отправителя", "!"}

	for _, msg := range messages {
		fmt.Printf("Отправка: %s\n", msg)
		ch <- msg                          // Блокирующая операция - ждет, пока получатель прочитает
		time.Sleep(300 * time.Millisecond) // Имитация обработки
	}

	close(ch) // Закрываем канал после отправки всех сообщений
	fmt.Println("Канал закрыт отправителем")
}

// Функция получателя (читает из канала)
func receiver(ch <-chan string, wg *sync.WaitGroup) {
	defer wg.Done()

	for {
		msg, ok := <-ch // Блокирующая операция - ждет, пока отправитель напишет
		if !ok {
			fmt.Println("Получатель: канал закрыт")
			return
		}
		fmt.Printf("Получено: %s (обработка...)\n", msg)
		time.Sleep(500 * time.Millisecond) // Имитация обработки
	}
}

func main() {
	// Создаем небуферизованный канал (емкость 0)
	messageChannel := make(chan string)

	var wg sync.WaitGroup

	// Запускаем отправителя и получателя
	wg.Add(2)

	go sender(messageChannel, &wg)
	go receiver(messageChannel, &wg)

	fmt.Println("=== Синхронная коммуникация через небуферизованный канал ===")
	fmt.Println("Отправитель и получатель работают синхронно")
	fmt.Println("Каждая отправка блокируется до получения сообщения")

	wg.Wait()

	fmt.Println("=== Все сообщения успешно отправлены и получены ===")
}
