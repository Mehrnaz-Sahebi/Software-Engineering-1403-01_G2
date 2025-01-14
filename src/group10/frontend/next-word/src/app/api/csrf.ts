export async function fetchCSRF(): Promise<string> {
    try {
        const response = await fetch("/group10/api/csrf/", {
            method: "GET",
        });

        if (!response.ok) {
            throw new Error("Failed to fetch csrf-token");
        }

        const data = await response.json();

        return data.csrf;
    } catch (error) {
        console.error("Error fetching csrf-token:", error);
        return "";
    }
}
