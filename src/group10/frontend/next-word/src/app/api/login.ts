import { MessageType, toastifyMessage } from "@/components/Toastify";
import { fetchCSRF } from "./csrf";

export async function performLogin(username: string, pass: string): Promise<boolean> {
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
        const result = JSON.parse(await response.text())
        toastifyMessage(result.error, MessageType.Error);
        return false;
    }

    return true;
}
