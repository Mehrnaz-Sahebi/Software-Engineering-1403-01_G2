package main


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


type Token struct {
	Start int
	End   int
	Word  string
}

func Tokenize(text string) []Token {
	if len(text) == 0 {
		return nil
	}

	runes := []rune(text)
	var tokens []Token

	length := len(runes)
	i := 0

	for i < length {

		for i < length {
			if _, isSplitter := splitters[runes[i]]; !isSplitter {
				break
			}
			i++
		}
		if i >= length {
			break
		}


		start := i


		for i < length {
			if _, isSplitter := splitters[runes[i]]; isSplitter {
				break
			}
			i++
		}


		word := string(runes[start:i])
		end := i



		if word == "می" && i < length {

			if runes[i] == ' ' || runes[i] == '\u200c' {
				i++


				subStart := i
				for i < length {
					if _, isSplitter := splitters[runes[i]]; isSplitter {
						break
					}
					i++
				}
				subEnd := i


				nextWord := string(runes[subStart:subEnd])
				word = word + " " + nextWord // e.g. "می" + " " + "کنم"
				end = subEnd
			}
		}

		tokens = append(tokens, Token{
			Start: start,
			End:   end - 1,
			Word:  word,
		})
	}

	return tokens
}


func FilterUnnecessary(tokens []Token) []Token {
	var filtered []Token
	for _, token := range tokens {
		if _, isUnnecessary := unnecessary[token.Word]; !isUnnecessary {
			filtered = append(filtered, token)
		}
	}
	return filtered
}
