async function fetchTotalFreshEnquiriesIndia() {
    const freshEnquiriesIndiaElement = document.getElementById("freshEnquiriesIndiaCount");
    if (!freshEnquiriesIndiaElement) {
        console.error("Element with ID 'freshEnquiriesIndiaCount' not found.");
        return;
    }

    freshEnquiriesIndiaElement.textContent = "Loading...";

    try {
        const response = await fetch('http://127.0.0.1:5000/Itotal-fresh-enquiries');

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Invalid JSON response from server");
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to fetch total fresh enquiries (India)");
        }

        console.log("Total Fresh Enquiries (India):", data.total_fresh_enquiries_india);
        freshEnquiriesIndiaElement.textContent = data.total_fresh_enquiries_india;
    } catch (error) {
        console.error("Error fetching total fresh enquiries (India):", error);
        freshEnquiriesIndiaElement.textContent = `Error: ${error.message}`;
    }
}

// Call the function when the page loads
document.addEventListener("DOMContentLoaded", fetchTotalFreshEnquiriesIndia);
