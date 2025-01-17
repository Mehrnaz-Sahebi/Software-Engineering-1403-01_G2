import { fetchCSRF } from "./csrf";

export async function fetchSuggestions(username: string, past_word: string): Promise<string[]> {
    try {
        const csrfToken = await fetchCSRF()
        
        const response = await fetch('/group10/api/suggest/', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                "credentials": "same-origin",
            },
            body: JSON.stringify({ username, past_word }),
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }

        const data = await response.json();

        console.log(data.suggestions)

        return data.suggestions;
    } catch (error) {
        console.error("Error fetching suggestions:", error);
        return [];
    }
}
