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

func SortStringMap(words map[string][]string, frequenciess map[string]int) map[string][]string {
	if len(frequenciess) != 0 {
		frequencies = frequenciess
	}
	keys := make([]string, 0, len(words))
	for key := range words {
		keys = append(keys, key)
	}
	sort.Slice(keys, func(i, j int) bool {
		freqI, existsI := frequencies[keys[i]]
		freqJ, existsJ := frequencies[keys[j]]
		if !existsI {
			freqI = 1
		}
		if !existsJ {
			freqJ = 1
		}
		return freqI > freqJ
	})
	sortedWords := make(map[string][]string)
	for _, key := range keys {
		sortedWords[key] = words[key]
	}
	return sortedWords
}


func SortStrings(stringsToSort []string, frequenciess map[string]int) []string {
	if len(frequenciess) != 0 {
		frequencies = frequenciess
	}
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

		err = SaveMapToJSON(frequencies, jsonFilePath)
		if err != nil {
			fmt.Printf("Error saving frequencies to JSON: %v\n", err)
			return
		}

	} else {
		var err error
		frequencies, err = LoadMapFromJSON(jsonFilePath)

		if err != nil {
			fmt.Printf("Error loading frequencies from JSON: %v\n", err)
			return
		}
	}
}
