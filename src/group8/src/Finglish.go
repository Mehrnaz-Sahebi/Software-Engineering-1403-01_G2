package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"
)

func translateGoogle(text, sourceLang, targetLang string) (string, error) {
	baseURL := "https://translate.googleapis.com/translate_a/single"
	params := url.Values{}
	params.Add("client", "gtx")
	params.Add("sl", sourceLang)
	params.Add("tl", targetLang)
	params.Add("dt", "t")
	params.Add("q", text)

	req, err := http.NewRequest("GET", baseURL+"?"+params.Encode(), nil)
	if err != nil {
		return "", err
	}

	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	var result []interface{}
	err = json.Unmarshal(body, &result)
	if err != nil {
		return "", fmt.Errorf("failed to parse response: %v. Raw response: %s", err, string(body))
	}

	if len(result) > 0 {
		translations, ok := result[0].([]interface{})
		if ok && len(translations) > 0 {
			translatedText, ok := translations[0].([]interface{})
			if ok && len(translatedText) > 0 {
				if text, ok := translatedText[0].(string); ok {
					return text, nil
				}
			}
		}
	}

	return "", fmt.Errorf("translation failed")
}

func finglishTranslator(word string) (string, bool) {
	translated, err := translateGoogle(strings.TrimSpace(word), "fa", "en")
	if err != nil {
		fmt.Println("Error translating text:", err)
		return "", false
	}
	translated2, err := translateGoogle(strings.TrimSpace(strings.ToLower(translated)), "en", "fa")
	if err != nil {
		fmt.Println("Error translating text:", err)
		return "", false
	}
	return translated2, true
}
