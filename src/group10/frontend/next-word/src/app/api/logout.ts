import { MessageType, toastifyMessage } from "@/components/Toastify";

export const logout = async (): Promise<boolean> => {
    const response = await fetch("/group10/api/logout/", {
        method: "GET"
    });

    if (!response.ok) {
        const result = JSON.parse(await response.text())
        toastifyMessage(result, MessageType.Error);
        return false;
    }

    return true;
};
