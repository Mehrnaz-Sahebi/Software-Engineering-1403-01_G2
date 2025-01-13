package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

var (
	originalFilePath = "persian-word-freq.txt"
	jsonFilePath     = "frequencies.json"
	frequencies      map[string]int
)

func SaveMapToJSON(frequencies map[string]int, filePath string) error {
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	return encoder.Encode(frequencies)
}

func LoadMapFromJSON(filePath string) (map[string]int, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var frequencies map[string]int
	decoder := json.NewDecoder(file)
	err = decoder.Decode(&frequencies)
	return frequencies, err
}

// LoadFrequencies parses the file and returns a map of word frequencies
func LoadFrequencies(filePath string) (map[string]int, error) {
	frequencies := make(map[string]int)
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Fields(line)
		if len(parts) < 2 {
			continue
		}
		word := parts[0]
		frequency, err := strconv.Atoi(parts[1])
		if err != nil {
			continue
		}
		frequencies[word] = frequency
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return frequencies, nil
}

// SortStrings sorts strings by their frequency in ascending order
func SortStrings(stringsToSort []string, frequencies map[string]int) []string {
	sort.Slice(stringsToSort, func(i, j int) bool {
		freqI, existsI := frequencies[stringsToSort[i]]
		freqJ, existsJ := frequencies[stringsToSort[j]]
		if !existsI {
			freqI = 1
		}
		if !existsJ {
			freqJ = 1
		}
		// Use < for strict ascending order
		return freqI < freqJ
	})
	return stringsToSort
}

func modifyMaps() {
	if _, err := os.Stat(jsonFilePath); os.IsNotExist(err) {
		// JSON file does not exist, build the map from the original file
		fmt.Println("JSON file not found. Building from the original file...")
		frequencies, err = LoadFrequencies(originalFilePath)
		if err != nil {
			fmt.Printf("Error loading frequencies from original file: %v\n", err)
			return
		}

		// Save the map as a JSON file for future use
		fmt.Printf("Saving frequencies to JSON: %v\n", frequencies)
		err = SaveMapToJSON(frequencies, jsonFilePath)
		if err != nil {
			fmt.Printf("Error saving frequencies to JSON: %v\n", err)
			return
		}
		fmt.Println("Frequencies saved to JSON.")
	} else {
		// JSON file exists, load the map from it
		fmt.Println("Loading frequencies from JSON file...")
		var err error
		frequencies, err = LoadMapFromJSON(jsonFilePath)
		fmt.Print(frequencies)
		if err != nil {
			fmt.Printf("Error loading frequencies from JSON: %v\n", err)
			return
		}
		fmt.Printf("Loaded frequencies from JSON: %v\n", frequencies)
	}
}
