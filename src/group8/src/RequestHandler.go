package main

import (
	"encoding/json"
	"fmt"
	"log"

	"github.com/streadway/amqp"
)

// Job holds both the text and the correlation ID.
type Job struct {
	Text          string
	CorrelationID string
}

// Replace these with your chosen buffer sizes.
var jobQueueWithID = make(chan Job, 100)
var resultQueueWithID = make(chan []map[string]interface{}, 100)

func search(word string) (map[string][]string, bool) {
	meanings, found := globalTrie.Search(word)
	if found == true {
		meanings = SortStringMap(meanings, nil)
		return meanings, true
	}
	//str, translated := finglishTranslator(word)
	translated := false
	str := word
	if translated == false {
		return nil, false
	}
	return map[string][]string{
		"meanings": {str},
		"antonyms": {},
	}, true
}

func processText(text string) []TokenMeaning {
	// Tokenize the text
	tokens := Tokenize(text)
	//fmt.Print(text)
	// Filter out Persian prepositions
	tokens = FilterUnnecessary(tokens)
	//fmt.Printf("Tokens: %s", tokens[0].Word)
	// Prepare the result
	var tokenMeanings []TokenMeaning
	for _, token := range tokens {
		// Use the token.Word field for Trie search
		if meanings, found := search(token.Word); found {
			tokenMeanings = append(tokenMeanings, TokenMeaning{
				Token:   token.Word,
				Meaning: meanings["meanings"],
			})
		}
	}
	return tokenMeanings
}

func runServer(conn *amqp.Connection) {
	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Failed to open a channel: %v", err)
	}
	defer ch.Close()

	waitForQueue(ch)

	msgs, err := ch.Consume(
		"text_queue", // queue name
		"",           // consumer tag
		true,         // auto-ack
		false,        // exclusive
		false,        // no-local
		false,        // no-wait
		nil,          // arguments
	)
	if err != nil {
		log.Fatalf("Failed to register a consumer: %v", err)
	}

	for i := 0; i < currentWorkers; i++ {
		go workerWithID(i)
	}

	go adjustWorkers()

	// Listen for processed results, publish them with correlation_id
	go func() {
		for results := range resultQueueWithID {
			body, err := json.Marshal(results)
			if err != nil {
				log.Printf("Failed to marshal results: %v", err)
				continue
			}
			corrID, _ := results[0]["correlation_id"].(string)
			err = ch.Publish(
				"",
				"meanings_queue",
				false,
				false,
				amqp.Publishing{
					ContentType:   "application/json",
					Body:          body,
					CorrelationId: corrID,
				},
			)
			if err != nil {
				log.Printf("Failed to publish results: %v", err)
			}
		}
	}()

	for d := range msgs {
		wg.Add(1)
		go func(d amqp.Delivery) {
			defer wg.Done()
			var message map[string]interface{}
			if err := json.Unmarshal(d.Body, &message); err != nil {
				fmt.Println("Error unmarshaling JSON:", err)
				return
			}
			text, ok := message["text"].(string)
			if !ok {
				fmt.Println("Key 'text' not found or not a string")
				return
			}
			jobQueueWithID <- Job{
				Text:          text,
				CorrelationID: d.CorrelationId, // capture the AMQP correlation ID
			}
		}(d)
	}

	wg.Wait()
	close(jobQueueWithID)
}

// workerWithID consumes from jobQueueWithID, processes the text,
// and sends back JSON that includes the same correlation_id.
func workerWithID(id int) {
	for job := range jobQueueWithID {
		tokenMeanings := processText(job.Text)
		response := []map[string]interface{}{
			{
				"correlation_id": job.CorrelationID,
				"results":        tokenMeanings,
			},
		}
		resultQueueWithID <- response
	}
}
