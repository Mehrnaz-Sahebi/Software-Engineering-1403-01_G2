export const logout = async (): Promise<void> => {
    try {
        const response = await fetch("/group10/api/logout/", {
            method: "GET"
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }
    } catch (error) {
        console.error("Failed to logout:", error);
        throw error;
    }
};
