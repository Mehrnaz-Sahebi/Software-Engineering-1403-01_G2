export async function fetchSuggestions(lastWord: string): Promise<string[]> {
    try {
        const response = await fetch(`/group10/api/suggest/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ past_word: lastWord }),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch suggestions");
        }

        const data = await response.json();
        return data.words; // Assuming the response has a structure { words: [] }
    } catch (error) {
        console.error("Error fetching suggestions:", error);
        return [];
    }
}
