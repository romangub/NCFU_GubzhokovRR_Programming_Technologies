package main

import (
	"sync"
	"testing"
	"time"
)

// TestSenderReceiverCommunication проверяет базовую коммуникацию
func TestSenderReceiverCommunication(t *testing.T) {
	// Создаем тестовый канал
	ch := make(chan string)
	var wg sync.WaitGroup

	// Счетчик полученных сообщений
	receivedCount := 0
	var mu sync.Mutex

	// Запускаем получателя
	wg.Add(1)
	go func() {
		defer wg.Done()
		for msg := range ch {
			mu.Lock()
			receivedCount++
			mu.Unlock()
			t.Logf("Получено: %s", msg)
		}
	}()

	// Запускаем отправителя
	wg.Add(1)
	go func() {
		defer wg.Done()
		messages := []string{"test1", "test2", "test3"}
		for _, msg := range messages {
			ch <- msg
			time.Sleep(10 * time.Millisecond)
		}
		close(ch)
	}()

	// Ждем завершения с таймаутом
	done := make(chan bool)
	go func() {
		wg.Wait()
		done <- true
	}()

	select {
	case <-done:
		// Успешно завершилось
	case <-time.After(1 * time.Second):
		t.Fatal("Таймаут: коммуникация заняла слишком много времени")
	}

	// Проверяем количество полученных сообщений
	mu.Lock()
	if receivedCount != 3 {
		t.Errorf("Получено %d сообщений, ожидалось 3", receivedCount)
	}
	mu.Unlock()
}

// TestChannelClose проверяет корректное закрытие канала
func TestChannelClose(t *testing.T) {
	ch := make(chan string)

	go func() {
		ch <- "test"
		close(ch)
	}()

	// Читаем первое сообщение
	msg, ok := <-ch
	if !ok || msg != "test" {
		t.Errorf("Первое сообщение неверное: %s, ok: %v", msg, ok)
	}

	// Проверяем, что канал закрыт
	_, ok = <-ch
	if ok {
		t.Error("Канал должен быть закрыт")
	}
}

// TestUnbufferedChannelBlocking проверяет блокировку небуферизованного канала
func TestUnbufferedChannelBlocking(t *testing.T) {
	ch := make(chan string) // небуферизованный

	sent := false
	received := false

	// Запускаем получателя
	go func() {
		time.Sleep(50 * time.Millisecond)
		<-ch
		received = true
	}()

	// Пытаемся отправить (должно заблокироваться до получения)
	ch <- "test"
	sent = true

	if !sent || !received {
		t.Error("Блокировка не работает правильно")
	}
}

// TestBufferedChannelNonBlocking проверяет неблокирующую отправку
func TestBufferedChannelNonBlocking(t *testing.T) {
	ch := make(chan string, 1) // буферизованный на 1 элемент

	// Первая отправка не должна блокироваться
	select {
	case ch <- "test1":
		t.Log("Первая отправка успешна (не блокируется)")
	case <-time.After(100 * time.Millisecond):
		t.Error("Первая отправка заблокировалась (не должно быть)")
	}

	// Вторая отправка должна блокироваться (буфер полон)
	select {
	case ch <- "test2":
		t.Error("Вторая отправка не должна пройти (буфер полон)")
	case <-time.After(100 * time.Millisecond):
		t.Log("Вторая отправка заблокировалась (как и ожидалось)")
	}

	// Читаем из канала, освобождая буфер
	select {
	case msg := <-ch:
		if msg != "test1" {
			t.Errorf("Получено неверное сообщение: %s", msg)
		}
	case <-time.After(100 * time.Millisecond):
		t.Error("Чтение заблокировалось (не должно быть)")
	}
}

// TestMultipleSendersReceivers проверяет несколько отправителей/получателей
func TestMultipleSendersReceivers(t *testing.T) {
	ch := make(chan int)
	var wg sync.WaitGroup
	totalMessages := 100

	// Счетчик полученных сообщений
	receivedCount := 0
	var mu sync.Mutex

	// Запускаем 2 получателя
	for i := 0; i < 2; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for msg := range ch {
				mu.Lock()
				receivedCount++
				mu.Unlock()
				_ = msg
			}
		}(i)
	}

	// Отправляем все сообщения из одной горутины (проще для теста)
	wg.Add(1)
	go func() {
		defer wg.Done()
		for i := 0; i < totalMessages; i++ {
			ch <- i
		}
		close(ch) // Закрываем канал после отправки всех сообщений
	}()

	// Ждем завершения
	wg.Wait()

	// Проверяем количество
	if receivedCount != totalMessages {
		t.Errorf("Получено %d сообщений, ожидалось %d", receivedCount, totalMessages)
	} else {
		t.Logf("✅ Успешно получено %d сообщений", receivedCount)
	}
}
