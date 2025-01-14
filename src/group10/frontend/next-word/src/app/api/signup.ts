import { MessageType, toastifyMessage } from "@/components/Toastify";
import { fetchCSRF } from "./csrf";

export async function performSignup(body: string): Promise<boolean> {
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
        const result = JSON.parse(await response.text())
        toastifyMessage(result.error, MessageType.Error);
        return false;
    }

    return true;
}
