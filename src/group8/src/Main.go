package main

import (
	"sync"
	"time"
)

const (
	rabbitMQURL      = "amqp://guest:guest@rabbitmq:5672/"
	queueName        = "text_queue"
	workerPoolSize   = 5
	retryInterval    = 5 * time.Second // Wait 5 seconds between retries
	maxRetryAttempts = 0               // Set to 0 for infinite retries
)

var (
	globalTrie = NewTrie()
)

var (
	minWorkers       = 2
	maxWorkers       = 50
	currentWorkers   = minWorkers
	jobQueue         = make(chan string, 100)
	resultQueue      = make(chan []TokenMeaning, 100)
	adjustmentPeriod = 5 * time.Second
	wg               sync.WaitGroup
	// wg2              sync.WaitGroup
)

type TokenMeaning struct {
	Token   string   `json:"token"`
	Meaning []string `json:"meaning"`
}

func main() {
	loadData()
	modifyMaps()
	// Setup RabbitMQ connection
	conn := rabbitMQConnenction()
	defer conn.Close()

	runServer(conn)
}
