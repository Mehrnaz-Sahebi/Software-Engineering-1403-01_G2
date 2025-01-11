package main

import (
	"encoding/json"
	"fmt"
	"log"
	"time"

	"github.com/streadway/amqp"
)

func sendResultsToRabbitMQ(ch *amqp.Channel, results []TokenMeaning) {
	body, err := json.Marshal(results)
	fmt.Printf("kire body mn: %s", body)
	if err != nil {
		log.Printf("Failed to marshal results: %v", err)
		return
	}

	err = ch.Publish(
		"",               // exchange
		"meanings_queue", // routing key
		false,            // mandatory
		false,            // immediate
		amqp.Publishing{
			ContentType: "application/json",
			Body:        body,
		},
	)
	if err != nil {
		log.Printf("Failed to publish results: %v", err)
	}
}

func waitForQueue(ch *amqp.Channel) {
	attempts := 0

	for {
		_, err := ch.QueueDeclarePassive(
			queueName, // Queue name
			true,      // Durable
			false,     // Delete when unused
			false,     // Exclusive
			false,     // No-wait
			nil,       // Arguments
		)
		if err == nil {
			log.Printf("Queue '%s' is available!", queueName)
			return
		}

		attempts++
		log.Printf("Queue '%s' not available (attempt %d): %v", queueName, attempts, err)

		// Check if max retries are defined and exceeded
		if maxRetryAttempts > 0 && attempts >= maxRetryAttempts {
			log.Fatalf("Failed to declare queue '%s' after %d attempts: %v", queueName, attempts, err)
		}

		time.Sleep(retryInterval)
	}
}
func rabbitMQConnenction() *amqp.Connection {
	conn, err := amqp.Dial("amqp://guest@rabbitmq:5672/")
	if err != nil {
		log.Fatalf("Failed to connect to RabbitMQ: %v", err)
	}
	return conn
}
