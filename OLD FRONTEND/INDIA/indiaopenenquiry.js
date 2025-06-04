async function fetchOpenEnquiriesIndia() {
    const openEnquiriesIndiaElement = document.getElementById("openEnquiriesIndiaCount");
    if (!openEnquiriesIndiaElement) {
        console.error("Element with ID 'openEnquiriesIndiaCount' not found.");
        return;
    }

    openEnquiriesIndiaElement.textContent = "Loading...";

    try {
        const response = await fetch('http://127.0.0.1:5000/Iopen-enquiries');

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Invalid JSON response from server");
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to fetch open enquiries (India)");
        }

        console.log("Open Enquiries (India):", data.total_open_enquiries_india);
        openEnquiriesIndiaElement.textContent = data.total_open_enquiries_india;
    } catch (error) {
        console.error("Error fetching open enquiries (India):", error);
        openEnquiriesIndiaElement.textContent = `Error: ${error.message}`;
    }
}

// Call the function when the page loads
document.addEventListener("DOMContentLoaded", fetchOpenEnquiriesIndia);
