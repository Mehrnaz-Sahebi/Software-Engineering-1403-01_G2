package main

import (
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
