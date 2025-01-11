package main

var splitters = map[rune]struct{}{
	' ': {}, '\u200c': {}, '\u2009': {}, '\n': {}, '\t': {}, '.': {}, ',': {}, ';': {}, '?': {}, '!': {}, '،': {},
	'؛': {}, '؟': {}, '(': {}, ')': {}, '0': {}, '1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {},
	'8': {}, '9': {}, '۰': {}, '۱': {}, '۲': {}, '۳': {}, '۴': {}, '۵': {}, '۶': {}, '۷': {}, '۸': {}, '۹': {},
	'#': {}, '-': {}, '_': {},
}

// List of Persian prepositions to filter out.
// You can expand this set with additional common prepositions.
var unnecessary = map[string]struct{}{
	"از":     {},
	"به":     {},
	"در":     {},
	"با":     {},
	"برای":   {},
	"تا":     {},
	"بود":    {},
	"شد":     {},
	"هست":    {},
	"بدون":   {},
	"کرد":    {},
	"نزد":    {},
	"بجز":    {},
	"علیرغم": {},
	"است":    {},
}

// Token holds positional information about a tokenized word.
type Token struct {
	Start int
	End   int
	Word  string
}

// Tokenize splits text into tokens, ignoring defined splitters.
func Tokenize(text string) []Token {
	if len(text) == 0 {
		return nil
	}
	var result []Token
	var start *int
	for i, r := range text {
		if _, ok := splitters[r]; ok {
			if start != nil {
				word := text[*start:i]
				result = append(result, Token{*start, i - 1, word})
				start = nil
			}
		} else {
			if start == nil {
				temp := i
				start = &temp
			}
		}
	}
	if start != nil {
		word := text[*start:len(text)]
		result = append(result, Token{*start, len(text), word})
	}
	return result
}

// Filterunnecessary removes tokens that match known Persian prepositions.
func FilterUnnecessary(tokens []Token) []Token {
	var filtered []Token
	for _, token := range tokens {
		if _, isUnnecessary := unnecessary[token.Word]; !isUnnecessary {
			filtered = append(filtered, token)
		}
	}
	return filtered
}
