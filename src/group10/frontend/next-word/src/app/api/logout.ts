export const logout = async (): Promise<void> => {
    try {
        const response = await fetch("/group10/logout/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
    } catch (error) {
        console.error("Failed to logout:", error);
        throw error;
    }
};
