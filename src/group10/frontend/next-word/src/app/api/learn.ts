import { fetchCSRF } from "./csrf";

export  async function sendWordsToLearn(username: string, tokens: string[]): Promise<void> {
    try {
        const csrfToken = await fetchCSRF()

        const response = await fetch("/group10/api/learn/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                "credentials": "same-origin",
            },
            body: JSON.stringify({ username, tokens }),
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }
    } catch (error) {
        console.error("Failed to send words to learn:", error);
    }
};
