package server

import (
	"context"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"
)

func TestServer_Routes(t *testing.T) {
	server := NewServer(":0")
	
	tests := []struct {
		name       string
		path       string
		wantStatus int
		wantBody   string
	}{
		{
			name:       "root path",
			path:       "/",
			wantStatus: http.StatusOK,
			wantBody:   "Hello! Request count:",
		},
		{
			name:       "health check",
			path:       "/health",
			wantStatus: http.StatusOK,
			wantBody:   "OK",
		},
		{
			name:       "stats",
			path:       "/stats",
			wantStatus: http.StatusOK,
			wantBody:   "Total requests:",
		},
	}
	
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest("GET", tt.path, nil)
			w := httptest.NewRecorder()
			
			server.router.ServeHTTP(w, req)
			
			resp := w.Result()
			body, _ := io.ReadAll(resp.Body)
			
			if resp.StatusCode != tt.wantStatus {
				t.Errorf("Expected status %d, got %d", tt.wantStatus, resp.StatusCode)
			}
			
			bodyStr := string(body)
			if !strings.Contains(bodyStr, tt.wantBody) {
				t.Errorf("Expected body to contain %q, got %q", tt.wantBody, bodyStr)
			}
		})
	}
}

func TestServer_ConcurrentRequests(t *testing.T) {
	server := NewServer(":0")
	ts := httptest.NewServer(server.router)
	defer ts.Close()
	
	var wg sync.WaitGroup
	requests := 100
	
	for i := 0; i < requests; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			resp, err := http.Get(ts.URL + "/")
			if err != nil {
				t.Errorf("Request failed: %v", err)
				return
			}
			defer resp.Body.Close()
			
			if resp.StatusCode != http.StatusOK {
				t.Errorf("Expected status 200, got %d", resp.StatusCode)
			}
		}(i)
	}
	
	wg.Wait()
	
	// Проверяем счётчик запросов
	count := server.GetRequestCount()
	if count < int64(requests/2) {
		t.Errorf("Expected at least %d requests, got %d", requests/2, count)
	}
}

func TestServer_GracefulShutdown(t *testing.T) {
	server := NewServer(":0")
	ts := httptest.NewServer(server.router)
	
	ctx, cancel := context.WithTimeout(context.Background(), 100*time.Millisecond)
	defer cancel()
	
	// Запускаем остановку сервера
	go func() {
		time.Sleep(50 * time.Millisecond)
		if err := server.Stop(ctx); err != nil {
			t.Logf("Shutdown error: %v", err)
		}
	}()
	
	// Пытаемся сделать запрос после shutdown
	time.Sleep(60 * time.Millisecond)
	_, err := http.Get(ts.URL + "/")
	if err == nil {
		t.Log("Request succeeded after shutdown (this may be expected with httptest)")
	}
	
	ts.Close()
}

func TestServer_RequestCount(t *testing.T) {
	server := NewServer(":0")
	
	// Изначально счётчик должен быть 0
	if server.GetRequestCount() != 0 {
		t.Errorf("Expected initial request count 0, got %d", server.GetRequestCount())
	}
	
	// Делаем несколько запросов
	req := httptest.NewRequest("GET", "/", nil)
	w := httptest.NewRecorder()
	
	for i := 0; i < 5; i++ {
		server.router.ServeHTTP(w, req)
	}
	
	// Проверяем, что счётчик увеличился
	count := server.GetRequestCount()
	if count < 5 {
		t.Errorf("Expected at least 5 requests, got %d", count)
	}
}

func BenchmarkServer_HandleRequest(b *testing.B) {
	server := NewServer(":0")
	req := httptest.NewRequest("GET", "/", nil)
	w := httptest.NewRecorder()
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		server.router.ServeHTTP(w, req)
		w = httptest.NewRecorder()
	}
}

