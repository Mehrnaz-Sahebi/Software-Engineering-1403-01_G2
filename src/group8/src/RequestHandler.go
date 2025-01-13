package main

import (
	"encoding/json"
	"fmt"
	"log"

	"github.com/streadway/amqp"
)

func search(word string) (map[string][]string, bool) {
	meanings, found := globalTrie.Search(word)
	if found == true {
		meanings = SortStringMap(meanings, nil)
		return meanings, true
	}
	str, tranlated := finglishTranslator(word)
	if tranlated == false {
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

	// Start worker pool with the initial number of workers
	for i := 0; i < currentWorkers; i++ {
		go worker(i)
	}

	// Adjust workers dynamically based on queue load
	go adjustWorkers()

	go func() {
		// Collect results and publish them back to RabbitMQ
		for result := range resultQueue {
			sendResultsToRabbitMQ(ch, result)
		}
	}()

	// Collect messages and add them to the job queue
	for d := range msgs {
		wg.Add(1)
		// wg2.Add(1)
		go func() {
			var message map[string]interface{}
			err := json.Unmarshal(d.Body, &message)
			if err != nil {
				fmt.Println("Error unmarshaling JSON:", err)
				wg.Done()
				return
			}
			if text, ok := message["text"].(string); ok {
				jobQueue <- text
			} else {
				fmt.Println("Key 'text' not found or not a string")
			}
			wg.Done()
		}()
	}
	wg.Wait()
	close(jobQueue)
}
