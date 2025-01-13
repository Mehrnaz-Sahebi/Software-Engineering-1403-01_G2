import { fetchCSRF } from "./csrf";

export async function fetchSignup(body: string): Promise<boolean> {
    try {
        const csrfToken = await fetchCSRF()

        const response = await fetch("/group10/api/signup/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: body,
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }

        return true;
    } catch (error) {
        console.error("Failed to register:", error);
    }

    return false;
}
