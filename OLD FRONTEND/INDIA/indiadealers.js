async function fetchUniqueDealersIndia() {
    const dealersCountElement = document.getElementById("IndiadealersCount");
    if (!dealersCountElement) {
        console.error("Element with ID 'IndiadealersCount' not found.");
        return;
    }

    dealersCountElement.textContent = "Loading...";

    try {
        const response = await fetch('http://127.0.0.1:5000/Idealers'); // Replace with actual backend URL if needed

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Invalid JSON response from server");
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to fetch unique dealers");
        }

        console.log("Unique Dealers (India):", data.unique_dealers_india);
        dealersCountElement.textContent = data.unique_dealers_india;
    } catch (error) {
        console.error("Error fetching unique dealers (India):", error);
        dealersCountElement.textContent = `Error: ${error.message}`;
    }
}

// Call the function when the page loads
document.addEventListener("DOMContentLoaded", fetchUniqueDealersIndia);
