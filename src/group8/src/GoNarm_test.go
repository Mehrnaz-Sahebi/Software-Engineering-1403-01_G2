package main

import (
	"os"
	"reflect"
	"sort"
	"testing"
)

func TestTokenize(t *testing.T) {
	got := Tokenize("تست توکنایزر")
	want := []Token{
		{0, 5, "تست"},
		{7, 23, "توکنایزر"},
	}

	if len(got) != len(want) {
		t.Errorf("got %d, want %d", len(got), len(want))
	}
	for i, q := range got {
		if q.Start != want[i].Start && q.End != want[i].End && q.Word != want[i].Word {
			t.Errorf("got %+v, wanted %+v", got, want)
		}
	}
}

func TestFilterUnnecessary(t *testing.T) {
	got := FilterUnnecessary(Tokenize("سلام از ما است"))
	want := []Token{
		{0, 7, "سلام"},
		{14, 17, "ما"},
	}

	if len(got) != len(want) {
		t.Errorf("got %d, want %d", len(got), len(want))
	}
	for i, q := range got {
		if q.Start != want[i].Start && q.End != want[i].End && q.Word != want[i].Word {
			t.Errorf("got %+v, wanted %+v", got, want)
		}
	}
}
func TestNewTrie(t *testing.T) {
	trie := NewTrie()
	if trie.Root == nil {
		t.Error("Expected root node to be initialized, got nil")
	}
	if len(trie.Root.Children) != 0 {
		t.Error("Expected root node to have no children, got some")
	}
	if trie.Root.IsEndOfWord {
		t.Error("Expected root node to not be the end of a word")
	}
	if len(trie.Root.Metadata["meanings"]) != 0 || len(trie.Root.Metadata["antonyms"]) != 0 {
		t.Error("Expected root node metadata to be empty")
	}
}

func TestInsert(t *testing.T) {
	trie := NewTrie()
	metadata := map[string][]string{
		"meanings": {"تستدرست"},
		"antonyms": {"تستغلط"},
	}
	trie.Insert("تستتست", metadata)

	node := trie.Root
	for _, char := range "تستتست" {
		if node.Children[char] == nil {
			t.Errorf("Expected child node for character %c, got nil", char)
		}
		node = node.Children[char]
	}
	if !node.IsEndOfWord {
		t.Error("Expected last node to be the end of a word")
	}
	if node.Metadata["meanings"][0] != "تستدرست" {
		t.Error("Expected metadata to be set correctly")
	}
}

func TestSearch(t *testing.T) {
	trie := NewTrie()
	metadata := map[string][]string{
		"meanings": {"تستدرست"},
		"antonyms": {"تستغلط"},
	}
	trie.Insert("تستتست", metadata)

	foundMetadata, found := trie.Search("تستتست")
	if !found {
		t.Error("Expected word 'joy' to be found")
	}
	if foundMetadata["meanings"][0] != "تستدرست" {
		t.Error("Expected metadata to match")
	}

	_, found = trie.Search("تستتس")
	if found {
		t.Error("Expected word 'jo' not to be found")
	}
}

func TestStartsWith(t *testing.T) {
	trie := NewTrie()
	metadata1 := map[string][]string{
		"meanings": {"تستدرست"},
		"antonyms": {"تستغلط"},
	}
	metadata2 := map[string][]string{
		"meanings": {"تستدرستی"},
		"antonyms": {"تستغلطی"},
	}
	trie.Insert("تستتست", metadata1)
	trie.Insert("تستتستی", metadata2)

	results := trie.StartsWith("تستتست")
	if len(results) != 2 {
		t.Errorf("Expected 2 results, got %d", len(results))
	}

	for _, result := range results {
		word := result["word"].(string)
		if word != "تستتست" && word != "تستتستی" {
			t.Errorf("Unexpected word in results: %s", word)
		}
	}
}

func TestSerializeDeserialize(t *testing.T) {
	trie := NewTrie()
	metadata := map[string][]string{
		"meanings": {"تستدرست"},
		"antonyms": {"تستغلط"},
	}
	trie.Insert("تستتست", metadata)

	data, err := trie.Serialize()
	if err != nil {
		t.Fatalf("Serialization failed: %v", err)
	}

	newTrie, err := DeserializeTrie(data)
	if err != nil {
		t.Fatalf("Deserialization failed: %v", err)
	}

	foundMetadata, found := newTrie.Search("تستتست")
	if !found {
		t.Error("Expected word 'تستتست' to be found after deserialization")
	}
	if foundMetadata["meanings"][0] != "تستدرست" {
		t.Error("Expected metadata to match after deserialization")
	}
}

func TestFuzzySearch(t *testing.T) {
	loadData()
	//trie := globalTrie
	trie := NewTrie()
	trie.Insert("تستتست", map[string][]string{
		"meanings": {"تستدرست"},
		"antonyms": {"تستغلط"},
	})
	trie.Insert("تستتسخ", map[string][]string{
		"meanings": {"تستدرستخ"},
		"antonyms": {"تستغلطخ"},
	})
	trie.Insert("تستتستر", map[string][]string{
		"meanings": {"تستتستردرست"},
		"antonyms": {"تستتسترغلط"},
	})
	trie.Insert("تستسلامتست", map[string][]string{
		"meanings": {"تستدرستتست"},
		"antonyms": {"تستغلطتست"},
	})

	// Test cases
	tests := []struct {
		name        string
		word        string
		maxDistance int
		expected    []string
	}{
		{
			name:        "Exact match",
			word:        "تستتست",
			maxDistance: 0,
			expected:    []string{"تستتست"},
		},
		{
			name:        "Substitution (1 edit)",
			word:        "تستخست",
			maxDistance: 1,
			expected:    []string{"تستتست"},
		},
		{
			name:        "Deletion (1 edit)",
			word:        "تستتسخت",
			maxDistance: 1,
			expected:    []string{"تستتست", "تستتسخ"},
		},
		{
			name:        "Insertion (1 edit)",
			word:        "تستتستت",
			maxDistance: 1,
			expected:    []string{"تستتست", "تستتستر"},
		},
		{
			name:        "Transposition (1 edit)",
			word:        "تستتست",
			maxDistance: 1,
			expected:    []string{"تستتست", "تستتسخ"},
		},
		{
			name:        "No match (too many edits)",
			word:        "تخاییسبحثصج",
			maxDistance: 1,
			expected:    []string{},
		},
		{
			name:        "Multiple matches (2 edits)",
			word:        "تستسلامتس",
			maxDistance: 2,
			expected:    []string{"تستسلامتست"},
		},
		{
			name:        "Empty input",
			word:        "",
			maxDistance: 1,
			expected:    []string{},
		},
		//{
		//	name:        "final test",
		//	word:        "کتاخ",
		//	maxDistance: 1,
		//	expected:    []string{"کتاب"},
		//},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			results := trie.FuzzySearch(tt.word, tt.maxDistance)
			if !equal(results, tt.expected) {
				t.Errorf("FuzzySearch(%q, %d) = %v, expected %v", tt.word, tt.maxDistance, results, tt.expected)
			}
		})
	}
}

// Helper function to compare two string slices
func equal(a, b []string) bool {
	if len(a) != len(b) {
		return false
	}
	if len(a) == 0 {
		return true
	}
	sort.Strings(b)
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func setupTestFiles(t *testing.T) (string, string) {
	t.Helper()

	// Create a temporary frequency file
	tempFreqFile, err := os.CreateTemp("", "freq-*.txt")
	if err != nil {
		t.Fatalf("Failed to create temp frequency file: %v", err)
	}
	defer tempFreqFile.Close()

	freqData := "word1 5\nword2 3\nword3 7\n"
	if _, err := tempFreqFile.WriteString(freqData); err != nil {
		t.Fatalf("Failed to write to temp frequency file: %v", err)
	}

	// Create a temporary JSON file
	tempJSONFile, err := os.CreateTemp("", "freq-*.json")
	if err != nil {
		t.Fatalf("Failed to create temp JSON file: %v", err)
	}
	tempJSONFile.Close()

	return tempFreqFile.Name(), tempJSONFile.Name()
}

func TestSaveMapToJSON(t *testing.T) {
	tempFreqFile, tempJSONFile := setupTestFiles(t)
	defer os.Remove(tempFreqFile)
	defer os.Remove(tempJSONFile)

	frequencies := map[string]int{"word1": 5, "word2": 3, "word3": 7}

	err := SaveMapToJSON(frequencies, tempJSONFile)
	if err != nil {
		t.Fatalf("SaveMapToJSON failed: %v", err)
	}

	// Validate the file exists and is not empty
	info, err := os.Stat(tempJSONFile)
	if err != nil || info.Size() == 0 {
		t.Fatalf("JSON file was not created correctly")
	}
}

func TestLoadMapFromJSON(t *testing.T) {
	tempFreqFile, tempJSONFile := setupTestFiles(t)
	defer os.Remove(tempFreqFile)
	defer os.Remove(tempJSONFile)

	frequencies := map[string]int{"word1": 5, "word2": 3, "word3": 7}
	err := SaveMapToJSON(frequencies, tempJSONFile)
	if err != nil {
		t.Fatalf("SaveMapToJSON failed: %v", err)
	}

	loadedFrequencies, err := LoadMapFromJSON(tempJSONFile)
	if err != nil {
		t.Fatalf("LoadMapFromJSON failed: %v", err)
	}

	if !reflect.DeepEqual(frequencies, loadedFrequencies) {
		t.Errorf("Expected %v, got %v", frequencies, loadedFrequencies)
	}
}

func TestLoadFrequencies(t *testing.T) {
	tempFreqFile, tempJSONFile := setupTestFiles(t)
	defer os.Remove(tempFreqFile)
	defer os.Remove(tempJSONFile)

	frequencies, err := LoadFrequencies(tempFreqFile)
	if err != nil {
		t.Fatalf("LoadFrequencies failed: %v", err)
	}

	expected := map[string]int{"word1": 5, "word2": 3, "word3": 7}
	if !reflect.DeepEqual(frequencies, expected) {
		t.Errorf("Expected %v, got %v", expected, frequencies)
	}
}

func TestSortStrings(t *testing.T) {
	frequencies := map[string]int{"word1": 5, "word2": 3, "word3": 7}
	stringsToSort := []string{"word3", "word1", "word2", "word4"}

	sortedStrings := SortStrings(stringsToSort, frequencies)
	expected := []string{"word4", "word2", "word1", "word3"}

	if !reflect.DeepEqual(sortedStrings, expected) {
		t.Errorf("Expected %v, got %v", expected, sortedStrings)
	}
}

func TestModifyMaps(t *testing.T) {
	tempFreqFile, _ := setupTestFiles(t)
	//fmt.Printf("kire man : %s\n", tempJSONFile)
	defer os.Remove(tempFreqFile)
	//defer os.Remove(tempJSONFile)

	originalFilePath = tempFreqFile
	//jsonFilePath = tempJSONFile
	// Step 1: Build frequencies from the original file and save to JSON
	modifyMaps() // Correct argument order

	// Verify frequencies after first run
	expected := map[string]int{"word1": 5, "word2": 3, "word3": 7}
	if !reflect.DeepEqual(frequencies, expected) {
		t.Errorf("Step 1: Expected %v, got %v", expected, frequencies)
	}

	// Step 2: Clear frequencies and reload from JSON
	frequencies = nil // Clear the global variable
	modifyMaps()      // Correct argument order again

	if !reflect.DeepEqual(frequencies, expected) {
		t.Errorf("Step 2: Expected %v, got %v", expected, frequencies)
	}
}

func TestSortWordsByFrequency(t *testing.T) {
	tests := []struct {
		name        string
		words       map[string][]string
		frequencies map[string]int
		expected    map[string][]string
	}{
		{
			name: "Sort by frequency in descending order",
			words: map[string][]string{
				"apple":  {"fruit", "red"},
				"banana": {"fruit", "yellow"},
				"carrot": {"vegetable", "orange"},
			},
			frequencies: map[string]int{
				"apple":  5,
				"carrot": 8,
			},
			expected: map[string][]string{
				"carrot": {"vegetable", "orange"},
				"apple":  {"fruit", "red"},
				"banana": {"fruit", "yellow"},
			},
		},
		{
			name:        "Empty input maps",
			words:       map[string][]string{},
			frequencies: map[string]int{},
			expected:    map[string][]string{},
		},
		{
			name: "Single word",
			words: map[string][]string{
				"apple": {"fruit", "red"},
			},
			frequencies: map[string]int{
				"apple": 10,
			},
			expected: map[string][]string{
				"apple": {"fruit", "red"},
			},
		},
		{
			name: "Same frequency for all words",
			words: map[string][]string{
				"apple":  {"fruit", "red"},
				"banana": {"fruit", "yellow"},
				"carrot": {"vegetable", "orange"},
			},
			frequencies: map[string]int{
				"apple":  5,
				"banana": 5,
				"carrot": 5,
			},
			expected: map[string][]string{
				"apple":  {"fruit", "red"},
				"banana": {"fruit", "yellow"},
				"carrot": {"vegetable", "orange"},
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := SortStringMap(tt.words, tt.frequencies)

			// Check if the result matches the expected output
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("Test case '%s' failed: expected %v, got %v", tt.name, tt.expected, result)
			}
		})
	}
}
