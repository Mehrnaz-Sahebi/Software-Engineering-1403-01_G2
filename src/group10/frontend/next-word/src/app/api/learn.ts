import { fetchCSRF } from "./csrf";

export const sendWordsToLearn = async ({username ,words} : {username: string, words: string[]}): Promise<void> => {
    try {
        const csrfToken = await fetchCSRF()

        const response = await fetch('/group10/learn/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ username, words }),
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }
    } catch (error) {
        console.error('Failed to send words to learn:', error);
    }
};
