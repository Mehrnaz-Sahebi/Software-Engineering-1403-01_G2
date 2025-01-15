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


		queueLength := len(jobQueue)


		desiredWorkers := calculateWorkerCount(queueLength)
		if desiredWorkers != currentWorkers {
			if desiredWorkers > currentWorkers {

				diff := desiredWorkers - currentWorkers
				for i := 0; i < diff; i++ {
					go worker(currentWorkers + i)
				}
			} else if desiredWorkers < currentWorkers {

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
