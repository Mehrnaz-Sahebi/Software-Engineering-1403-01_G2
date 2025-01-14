import { fetchCSRF } from "./csrf";

export async function fetchSuggestions(lastWord: string): Promise<string[]> {
    try {
        const csrfToken = await fetchCSRF()
        
        const response = await fetch(`/group10/api/suggest/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ last_word: lastWord }),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch suggestions");
        }

        const data = await response.json();

        console.log(data.words)

        return data.words;
    } catch (error) {
        console.error("Error fetching suggestions:", error);
        return [];
    }
}
