package main

import (
	"log"
	"math"
	"time"
)

func worker(id int) {
	// defer wg2.Done()

	for job := range jobQueue {
		log.Printf("Worker %d processing job: %s", id, job)
		resultQueue <- processText(job)
	}
}

func adjustWorkers() {
	for {
		time.Sleep(adjustmentPeriod)

		// Check queue length to determine the number of workers needed
		queueLength := len(jobQueue)

		// Calculate the desired number of workers
		desiredWorkers := calculateWorkerCount(queueLength)
		if desiredWorkers != currentWorkers {
			if desiredWorkers > currentWorkers {
				// Add more workers
				diff := desiredWorkers - currentWorkers
				for i := 0; i < diff; i++ {
					go worker(currentWorkers + i)
				}
			} else if desiredWorkers < currentWorkers {
				// Reduce workers (this requires signaling workers to stop gracefully)
				diff := currentWorkers - desiredWorkers
				for i := 0; i < diff; i++ {
					log.Printf("Stopping worker %d", currentWorkers-i-1)
				}
			}
			currentWorkers = desiredWorkers
			log.Printf("Adjusted worker pool to %d workers", currentWorkers)
		}
	}
}

func calculateWorkerCount(queueLength int) int {
	// Scale workers based on queue length
	desiredWorkers := int(math.Ceil(float64(queueLength) / 10.0)) // Example scaling logic
	if desiredWorkers < minWorkers {
		desiredWorkers = minWorkers
	} else if desiredWorkers > maxWorkers {
		desiredWorkers = maxWorkers
	}
	return desiredWorkers
}

func startWorkerPool() {

}
