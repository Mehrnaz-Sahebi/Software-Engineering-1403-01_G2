export const sendWordsToLearn = async ({username ,words} : {username: string, words: string[]}): Promise<void> => {
    try {
        const response = await fetch('/group10/learn/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, words }),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Failed to send words to learn API:', error);
    }
};
