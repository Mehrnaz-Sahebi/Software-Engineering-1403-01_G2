package main

import "sort"

func (t *Trie) FuzzySearch(word string, maxDistance int) []string {
	var results []string
	t.fuzzySearchHelper(t.Root, []rune(word), []rune{}, maxDistance, &results)
	if len(results) == 0 {
		return results
	}
	sort.Strings(results)
	finalResult := []string{results[0]} // Start with the first element
	for i := 1; i < len(results); i++ {
		if results[i] != results[i-1] { // Skip duplicates
			finalResult = append(finalResult, results[i])
		}
	}
	return finalResult
}

func (t *Trie) fuzzySearchHelper(node *TrieNode, remainingWord, currentWord []rune, maxDistance int, results *[]string) {
	// Base case: if the remaining word is empty, check if the current node is the end of a word
	if len(remainingWord) == 0 {
		if node.IsEndOfWord {
			*results = append(*results, string(currentWord))
		}
		return
	}

	// If we've exhausted the allowed edit distance, stop searching
	if maxDistance < 0 {
		return
	}

	// Try matching the current character
	char := remainingWord[0]
	if child, exists := node.Children[char]; exists {
		t.fuzzySearchHelper(child, remainingWord[1:], append(currentWord, char), maxDistance, results)
	}

	// Try all possible edits if we still have edit distance left
	if maxDistance > 0 {
		// Deletion: skip the current character in the remaining word
		t.fuzzySearchHelper(node, remainingWord[1:], currentWord, maxDistance-1, results)

		// Insertion: try all possible characters in the trie
		for char, child := range node.Children {
			t.fuzzySearchHelper(child, remainingWord, append(currentWord, char), maxDistance-1, results)
		}

		// Substitution: replace the current character with any character in the trie
		for char, child := range node.Children {
			if char != remainingWord[0] { // Avoid redundant substitutions
				t.fuzzySearchHelper(child, remainingWord[1:], append(currentWord, char), maxDistance-1, results)
			}
		}

		// Transposition: swap the current and next character in the remaining word
		if len(remainingWord) > 1 {
			swapped := []rune{remainingWord[1], remainingWord[0]}
			if len(remainingWord) > 2 {
				swapped = append(swapped, remainingWord[2:]...)
			}
			t.fuzzySearchHelper(node, swapped, currentWord, maxDistance-1, results)
		}
	}
}
