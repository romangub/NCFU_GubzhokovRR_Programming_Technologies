package main

import (
	"fmt"
	"time"
)

// Функция генератора задач
func taskGenerator(tasks chan<- string) {
	taskTypes := []string{"Анализ данных", "Обработка изображения",
		"Расчет статистики", "Валидация данных", "Генерация отчета"}

	for i := 1; i <= 15; i++ {
		task := fmt.Sprintf("%s #%d", taskTypes[i%len(taskTypes)], i)

		select {
		case tasks <- task: // Неблокирующая отправка (если есть место в буфере)
			fmt.Printf("Задача добавлена в очередь: %s\n", task)
		default:
			fmt.Printf("Очередь переполнена, пропускаем задачу: %s\n", task)
		}

		time.Sleep(200 * time.Millisecond)
	}

	close(tasks)
	fmt.Println("Генератор задач завершил работу")
}

// Функция обработчика задач
func taskProcessor(tasks <-chan string, workerID int) {
	for task := range tasks {
		fmt.Printf("Worker %d начал: %s\n", workerID, task)

		// Имитация обработки с разным временем
		processingTime := time.Duration(300+workerID*100) * time.Millisecond
		time.Sleep(processingTime)

		fmt.Printf("Worker %d завершил: %s за %v\n",
			workerID, task, processingTime)
	}

	fmt.Printf("Worker %d завершил работу (канал закрыт)\n", workerID)
}

func main() {
	// Создаем буферизованный канал на 10 элементов
	taskQueue := make(chan string, 10)

	fmt.Println("=== Асинхронная очередь задач с буферизованным каналом ===")
	fmt.Println("Размер буфера: 10 задач")
	fmt.Println("Генератор создает задачи быстрее, чем обрабатываются")

	// Запускаем генератор задач
	go taskGenerator(taskQueue)

	// Запускаем 3 воркера для обработки задач
	for i := 1; i <= 3; i++ {
		go taskProcessor(taskQueue, i)
	}

	// Даем время на выполнение
	time.Sleep(5 * time.Second)

	fmt.Println("=== Программа завершена ===")
}
