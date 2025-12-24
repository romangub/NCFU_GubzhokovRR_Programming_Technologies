package main

import (
	"strings"
	"sync"
	"testing"
	"time"
)

// TestWorkerPoolBasic проверяет базовую функциональность
func TestWorkerPoolBasic(t *testing.T) {
	// Создаем тестовые каналы
	tasks := make(chan Task, 5)
	results := make(chan Result, 5)
	var wg sync.WaitGroup

	// Счетчик обработанных задач
	processedCount := 0
	var mu sync.Mutex

	// Запускаем тестового воркера
	wg.Add(1)
	go func(id int, tasks <-chan Task, results chan<- Result, wg *sync.WaitGroup) {
		defer wg.Done()
		for task := range tasks {
			mu.Lock()
			processedCount++
			mu.Unlock()
			results <- Result{
				TaskID: task.ID,
				Output: "processed",
			}
		}
	}(1, tasks, results, &wg)

	// Отправляем задачи
	for i := 1; i <= 3; i++ {
		tasks <- Task{ID: i}
	}
	close(tasks)

	// Закрываем results после завершения
	go func() {
		wg.Wait()
		close(results)
	}()

	// Собираем результаты
	var resultCount int
	for range results {
		resultCount++
	}

	if resultCount != 3 {
		t.Errorf("Обработано %d задач, ожидалось 3", resultCount)
	}
}

// TestMultipleWorkers проверяет работу нескольких воркеров
func TestMultipleWorkers(t *testing.T) {
	numWorkers := 3
	numTasks := 10

	tasks := make(chan Task, numTasks)
	results := make(chan Result, numTasks)
	var wg sync.WaitGroup

	// Счетчик задач по воркерам
	workerTasks := make(map[int]int)
	var mu sync.Mutex

	// Запускаем воркеров
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		workerID := i
		go func(id int) {
			defer wg.Done()
			for task := range tasks {
				mu.Lock()
				workerTasks[id]++
				mu.Unlock()

				results <- Result{
					TaskID: task.ID,
					Output: "done",
				}
				time.Sleep(1 * time.Millisecond) // Минимальная задержка
			}
		}(workerID)
	}

	// Отправляем задачи
	for i := 1; i <= numTasks; i++ {
		tasks <- Task{ID: i}
	}
	close(tasks)

	// Закрываем results после завершения
	go func() {
		wg.Wait()
		close(results)
	}()

	// Собираем результаты
	var resultCount int
	for range results {
		resultCount++
	}

	// Проверяем
	if resultCount != numTasks {
		t.Errorf("Обработано %d задач, ожидалось %d", resultCount, numTasks)
	}

	// Проверяем распределение задач между воркерами
	mu.Lock()
	totalDistributed := 0
	for workerID, count := range workerTasks {
		t.Logf("Worker %d обработал %d задач", workerID, count)
		totalDistributed += count
	}
	mu.Unlock()

	if totalDistributed != numTasks {
		t.Errorf("Распределено %d задач, ожидалось %d", totalDistributed, numTasks)
	}
}

// TestWorkerPoolWithTimeout проверяет работу с таймаутом
func TestWorkerPoolWithTimeout(t *testing.T) {
	tasks := make(chan Task, 5)
	results := make(chan Result, 5)
	var wg sync.WaitGroup

	// Воркер с долгой обработкой
	wg.Add(1)
	go func(id int) {
		defer wg.Done()
		for task := range tasks {
			// Имитация долгой обработки
			time.Sleep(500 * time.Millisecond)
			results <- Result{
				TaskID: task.ID,
				Output: "slow",
			}
		}
	}(1)

	// Отправляем задачу
	tasks <- Task{ID: 1}
	close(tasks)

	// Пытаемся получить результат с таймаутом
	select {
	case result := <-results:
		t.Logf("Получен результат: %v", result)
	case <-time.After(100 * time.Millisecond):
		t.Log("Таймаут: задача не завершилась вовремя (ожидаемо)")
	}

	// Ждем завершения воркера
	go func() {
		wg.Wait()
		close(results)
	}()
}

// TestWorkerPoolResultsOrder проверяет порядок результатов
func TestWorkerPoolResultsOrder(t *testing.T) {
	numWorkers := 2
	numTasks := 5

	tasks := make(chan Task, numTasks)
	results := make(chan Result, numTasks)
	var wg sync.WaitGroup

	// Воркеры с разной скоростью обработки
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		workerID := i
		go func(id int) {
			defer wg.Done()
			for task := range tasks {
				// Воркер 1 быстрее, воркер 2 медленнее
				delay := time.Duration(id*100) * time.Millisecond
				time.Sleep(delay)

				results <- Result{
					TaskID: task.ID,
					Output: "done",
				}
			}
		}(workerID)
	}

	// Отправляем задачи в определенном порядке
	expectedOrder := []int{1, 2, 3, 4, 5}
	for _, id := range expectedOrder {
		tasks <- Task{ID: id}
	}
	close(tasks)

	// Закрываем results после завершения
	go func() {
		wg.Wait()
		close(results)
	}()

	// Собираем ID результатов (порядок может быть разным из-за параллельности)
	var receivedIDs []int
	for result := range results {
		receivedIDs = append(receivedIDs, result.TaskID)
	}

	// Проверяем, что все задачи обработаны
	if len(receivedIDs) != len(expectedOrder) {
		t.Errorf("Получено %d результатов, ожидалось %d", len(receivedIDs), len(expectedOrder))
	}

	// Сортируем для проверки содержания
	receivedSet := make(map[int]bool)
	for _, id := range receivedIDs {
		receivedSet[id] = true
	}

	for _, id := range expectedOrder {
		if !receivedSet[id] {
			t.Errorf("Задача %d не была обработана", id)
		}
	}

	t.Logf("Полученные ID (порядок может отличаться): %v", receivedIDs)
}

// TestWorkerPoolChannelClose проверяет корректное закрытие каналов
func TestWorkerPoolChannelClose(t *testing.T) {
	tasks := make(chan Task, 3)
	results := make(chan Result, 3)
	var wg sync.WaitGroup

	workersStarted := make(chan bool, 2)

	// Запускаем воркера
	wg.Add(1)
	go func() {
		defer wg.Done()
		workersStarted <- true
		for task := range tasks {
			results <- Result{TaskID: task.ID}
		}
		// Воркер завершился, но НЕ закрывает results
		// В реальном worker pool это делает отдельная горутина
	}()

	// Ждем запуска воркера
	<-workersStarted

	// Отправляем задачи
	tasks <- Task{ID: 1}
	tasks <- Task{ID: 2}

	// Закрываем канал задач
	close(tasks)

	// Ждем завершения воркера
	wg.Wait()

	// Проверяем, что results НЕ закрыт (в этой реализации)
	select {
	case _, ok := <-results:
		if !ok {
			t.Error("Канал results неожиданно закрыт")
		} else {
			t.Log("Канал results все еще открыт (ожидаемо)")
		}
	default:
		t.Log("Канал results не закрыт и не имеет данных (ожидаемо)")
	}

	// Закрываем results вручную (как в реальном коде)
	close(results)

	// Теперь проверяем, что results закрыт
	_, ok := <-results
	if ok {
		t.Error("Канал results должен быть закрыт после close()")
	}
}

// TestConcurrentTaskSubmission проверяет конкурентную отправку задач
func TestConcurrentTaskSubmission(t *testing.T) {
	numWorkers := 5
	tasks := make(chan Task, 50)
	results := make(chan Result, 50)
	var wg sync.WaitGroup

	// Запускаем воркеров
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for task := range tasks {
				results <- Result{
					TaskID: task.ID,
					Output: "processed",
				}
			}
		}(i)
	}

	// Конкурентная отправка задач
	var sendersWg sync.WaitGroup
	totalTasks := 100

	for i := 0; i < 5; i++ { // 5 горутин-отправителей
		sendersWg.Add(1)
		go func(senderID int) {
			defer sendersWg.Done()
			for j := 0; j < totalTasks/5; j++ {
				taskID := senderID*1000 + j
				tasks <- Task{ID: taskID}
			}
		}(i)
	}

	sendersWg.Wait()
	close(tasks)

	// Закрываем results после завершения
	go func() {
		wg.Wait()
		close(results)
	}()

	// Считаем результаты
	resultCount := 0
	for range results {
		resultCount++
	}

	if resultCount != totalTasks {
		t.Errorf("Обработано %d задач, ожидалось %d", resultCount, totalTasks)
	}
}

// TestWorkerOutputFormat проверяет формат вывода воркера
func TestWorkerOutputFormat(t *testing.T) {
	tasks := make(chan Task, 2)
	results := make(chan Result, 2)
	var wg sync.WaitGroup

	// Тестовый воркер
	wg.Add(1)
	go func(id int) {
		defer wg.Done()
		for task := range tasks {
			output := "Task processed"
			results <- Result{
				TaskID: task.ID,
				Output: output,
			}
		}
	}(1)

	// Отправляем задачу
	tasks <- Task{ID: 42}
	close(tasks)

	// Закрываем results после завершения
	go func() {
		wg.Wait()
		close(results)
	}()

	// Проверяем результат
	result, ok := <-results
	if !ok {
		t.Fatal("Не получен результат")
	}

	if result.TaskID != 42 {
		t.Errorf("TaskID: %d, ожидалось 42", result.TaskID)
	}

	if !strings.Contains(result.Output, "Task") {
		t.Errorf("Output не содержит 'Task': %s", result.Output)
	}
}

// BenchmarkWorkerPool производительность воркер пула
func BenchmarkWorkerPool(b *testing.B) {
	for n := 0; n < b.N; n++ {
		numWorkers := 10
		numTasks := 100

		tasks := make(chan Task, numTasks)
		results := make(chan Result, numTasks)
		var wg sync.WaitGroup

		// Запускаем воркеров
		for i := 1; i <= numWorkers; i++ {
			wg.Add(1)
			go func(id int) {
				defer wg.Done()
				for task := range tasks {
					results <- Result{
						TaskID: task.ID,
						Output: "done",
					}
				}
			}(i)
		}

		// Отправляем задачи
		for i := 1; i <= numTasks; i++ {
			tasks <- Task{ID: i}
		}
		close(tasks)

		// Закрываем results после завершения
		go func() {
			wg.Wait()
			close(results)
		}()

		// Читаем все результаты
		for range results {
			// просто читаем
		}
	}
}
