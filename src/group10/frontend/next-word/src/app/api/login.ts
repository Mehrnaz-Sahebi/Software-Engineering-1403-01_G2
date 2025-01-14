import { fetchCSRF } from "./csrf";

export async function performLogin(username: string, pass: string): Promise<boolean> {
    try {
        const csrfToken = await fetchCSRF()

        const response = await fetch("/group10/api/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                "credentials": "same-origin",
            },
            body: JSON.stringify({ username, pass })
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }

        return true;
    } catch (error) {
        console.error("Failed to login:", error);
    }

    return false;
}
