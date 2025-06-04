async function fetchUniqueDealersold() {
    const dealerCountElement = document.getElementById("dealerCountOLD");
    if (!dealerCountElement) {
        console.error("Element with ID 'dealerCountOLD' not found.");
        return;
    }

    dealerCountElement.textContent = "Loading...";

    try {
        const response = await fetch('http://127.0.0.1:5000/dealers_old');

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || "Failed to fetch data");
        }

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Invalid JSON response from server");
        }

        const data = await response.json();

        console.log("Unique Dealers:", data.unique_dealers);
        dealerCountElement.textContent = data.unique_dealers;
    } catch (error) {
        console.error("Error fetching unique dealers:", error);
        dealerCountElement.textContent = `Error: ${error.message}`;
    }
}

document.addEventListener("DOMContentLoaded", fetchUniqueDealersold);
