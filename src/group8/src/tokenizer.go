package main

// splitters holds runes that normally break tokens.
var splitters = map[rune]struct{}{
	' ': {}, '\u200c': {}, '\u2009': {}, '\n': {}, '\t': {}, '.': {}, ',': {}, ';': {}, '?': {}, '!': {}, '،': {},
	'؛': {}, '؟': {}, '(': {}, ')': {}, '0': {}, '1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {},
	'8': {}, '9': {}, '۰': {}, '۱': {}, '۲': {}, '۳': {}, '۴': {}, '۵': {}, '۶': {}, '۷': {}, '۸': {}, '۹': {},
	'#': {}, '-': {}, '_': {},
}

// unnecessary holds words (e.g. common Persian prepositions) that you’d like to filter out later.
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

// Tokenize scans through the text and returns a slice of Tokens.
// If it detects the word "می" followed by a space or half-space,
// it merges them into a single token (e.g., "می کنم" instead of "می", "کنم").
func Tokenize(text string) []Token {
	if len(text) == 0 {
		return nil
	}

	runes := []rune(text)
	var tokens []Token

	length := len(runes)
	i := 0

	for i < length {
		// 1) Skip leading splitters
		for i < length {
			if _, isSplitter := splitters[runes[i]]; !isSplitter {
				break
			}
			i++
		}
		if i >= length {
			break
		}

		// 2) Now i is at the start of a token
		start := i

		// move i forward until next splitter or end-of-text
		for i < length {
			if _, isSplitter := splitters[runes[i]]; isSplitter {
				break
			}
			i++
		}

		// end is i (exclusive), the token is runes[start:i]
		word := string(runes[start:i])
		end := i // this is the first splitter after the token

		// 3) Special handling for "می" + space/half-space
		// If the word is exactly "می" and we haven't reached the end of text
		if word == "می" && i < length {
			// Check if the next rune is a space or half-space
			if runes[i] == ' ' || runes[i] == '\u200c' {
				// skip this splitter (so we effectively merge with next chunk)
				i++

				// now read the subsequent characters (the next word) until next splitter
				subStart := i
				for i < length {
					if _, isSplitter := splitters[runes[i]]; isSplitter {
						break
					}
					i++
				}
				subEnd := i

				// merge "می" with whatever came after
				nextWord := string(runes[subStart:subEnd])
				word = word + " " + nextWord // e.g. "می" + " " + "کنم"
				end = subEnd
			}
		}

		// 4) Create the token [start, end)
		// end-1 is the last rune index of this token
		tokens = append(tokens, Token{
			Start: start,
			End:   end - 1,
			Word:  word,
		})
	}

	return tokens
}

// FilterUnnecessary removes tokens that match known Persian prepositions.
func FilterUnnecessary(tokens []Token) []Token {
	var filtered []Token
	for _, token := range tokens {
		if _, isUnnecessary := unnecessary[token.Word]; !isUnnecessary {
			filtered = append(filtered, token)
		}
	}
	return filtered
}
