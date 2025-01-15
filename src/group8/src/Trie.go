package main

import (
	"encoding/json"
)

type TrieNode struct {
	Children    map[rune]*TrieNode  `json:"children"`
	IsEndOfWord bool                `json:"is_end_of_word"`
	Metadata    map[string][]string `json:"metadata"`
}

type Trie struct {
	Root *TrieNode
}

func NewTrie() *Trie {
	return &Trie{
		Root: &TrieNode{
			Children: make(map[rune]*TrieNode),
			Metadata: map[string][]string{
				"meanings": {},
				"antonyms": {},
			},
		},
	}
}

func (t *Trie) Insert(word string, metadata map[string][]string) {
	node := t.Root
	for _, char := range word {
		if node.Children[char] == nil {
			node.Children[char] = &TrieNode{
				Children: make(map[rune]*TrieNode),
				Metadata: map[string][]string{
					"meanings": {},
					"antonyms": {},
				},
			}
		}
		node = node.Children[char]
	}
	node.IsEndOfWord = true
	node.Metadata = metadata
}

func (t *Trie) Search(word string) (map[string][]string, bool) {
	node := t.Root
	for _, char := range word {
	  if node.Children[char] == nil {
		return  nil,false
	  }
	  node = node.Children[char]
	}
	if node.IsEndOfWord {
	  return node.Metadata, true
	}
	return nil, false
  }

func (t *Trie) StartsWith(prefix string) []map[string]interface{} {
	node := t.Root
	for _, char := range prefix {
		if node.Children[char] == nil {
			return nil
		}
		node = node.Children[char]
	}

	return collectWords(node, prefix)
}

func collectWords(node *TrieNode, prefix string) []map[string]interface{} {
	var results []map[string]interface{}

	if node.IsEndOfWord {
		results = append(results, map[string]interface{}{
			"word":     prefix,
			"metadata": node.Metadata,
		})
	}

	for char, child := range node.Children {
		results = append(results, collectWords(child, prefix+string(char))...)
	}
	return results
}

func (t *Trie) Serialize() ([]byte, error) {
	return json.Marshal(t.Root)
}

func DeserializeTrie(data []byte) (*Trie, error) {
	rootNode := &TrieNode{}
	err := json.Unmarshal(data, rootNode)
	if err != nil {
		return nil, err
	}
	return &Trie{Root: rootNode}, nil
}

