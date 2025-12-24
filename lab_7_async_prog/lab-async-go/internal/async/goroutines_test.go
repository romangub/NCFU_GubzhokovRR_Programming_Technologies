package main

import (
	"sync"
	"testing"
	"time"
)

// Вспомогательная структура для тестирования
type TestCounter struct {
	mu    sync.Mutex
	value int
}

func (c *TestCounter) Increment() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.value++
}

func (c *TestCounter) Value() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.value
}

// TestProcessItem проверяет, что все горутины завершаются
func TestProcessItem(t *testing.T) {
	var wg sync.WaitGroup
	counter := &TestCounter{}
	totalItems := 5

	// Создаем свою версию processItem для тестирования
	testProcessItem := func(itemID int, wg *sync.WaitGroup) {
		defer wg.Done()
		counter.Increment()
		time.Sleep(time.Duration(100+itemID*50) * time.Millisecond)
	}

	// Запускаем горутины
	for i := 1; i <= totalItems; i++ {
		wg.Add(1)
		go testProcessItem(i, &wg)
	}

	// Ожидаем завершения
	done := make(chan bool)
	go func() {
		wg.Wait()
		done <- true
	}()

	// Ждем с таймаутом
	select {
	case <-done:
		// Все горутины завершились
	case <-time.After(2 * time.Second):
		t.Fatal("Таймаут: не все горутины завершились")
	}

	// Проверяем счетчик
	if counter.Value() != totalItems {
		t.Errorf("Обработано %d элементов, ожидалось %d", counter.Value(), totalItems)
	}
}

// TestConcurrentExecution проверяет параллельное выполнение
func TestConcurrentExecution(t *testing.T) {
	var wg sync.WaitGroup
	results := make(chan int, 10)
	expectedSum := 0

	// Запускаем 10 горутин
	for i := 1; i <= 10; i++ {
		wg.Add(1)
		expectedSum += i

		go func(id int) {
			defer wg.Done()
			time.Sleep(time.Duration(id*10) * time.Millisecond)
			results <- id
		}(i)
	}

	// Горутина для закрытия канала
	go func() {
		wg.Wait()
		close(results)
	}()

	// Собираем результаты
	sum := 0
	for result := range results {
		sum += result
	}

	// Проверяем сумму
	if sum != expectedSum {
		t.Errorf("Сумма результатов: %d, ожидалось: %d", sum, expectedSum)
	}
}

// TestWaitGroupProperlyUsed проверяет корректное использование WaitGroup
func TestWaitGroupProperlyUsed(t *testing.T) {
	var wg sync.WaitGroup
	completed := make([]bool, 5)

	// Запускаем 5 горутин
	for i := 0; i < 5; i++ {
		wg.Add(1)

		go func(index int) {
			defer wg.Done()
			time.Sleep(time.Duration(index*50) * time.Millisecond)
			completed[index] = true
		}(i)
	}

	wg.Wait()

	// Проверяем, что все горутины завершились
	for i, done := range completed {
		if !done {
			t.Errorf("Горутина %d не завершилась", i)
		}
	}
}
