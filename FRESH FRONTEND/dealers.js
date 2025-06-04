async function fetchUniqueDealers() {
    const dealerCountElement = document.getElementById("dealerCount");
    if (!dealerCountElement) {
        console.error("Element with ID 'dealerCount' not found.");
        return;
    }

    dealerCountElement.textContent = "Loading...";

    try {
        const response = await fetch('http://127.0.0.1:5000/dealers'); // Replace with your actual backend URL
        
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Invalid JSON response from server");
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to fetch data");
        }

        console.log("Unique Dealers:", data.unique_dealers);
        dealerCountElement.textContent = data.unique_dealers;
    } catch (error) {
        console.error("Error fetching unique dealers:", error);
        dealerCountElement.textContent = `Error: ${error.message}`;
    }
}

// Call the function when the page loads
document.addEventListener("DOMContentLoaded", fetchUniqueDealers);
