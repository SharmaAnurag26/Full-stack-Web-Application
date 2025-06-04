async function fetchTotalFreshEnquiries() {
    const freshEnquiriesElement = document.getElementById("freshEnquiriesCount");
    if (!freshEnquiriesElement) {
        console.error("Element with ID 'freshEnquiriesCount' not found.");
        return;
    }

    freshEnquiriesElement.textContent = "Loading...";

    try {
        const response = await fetch('http://127.0.0.1:5000/total-fresh-enquiries'); // Replace with your actual backend URL
        
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Invalid JSON response from server");
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to fetch total fresh enquiries");
        }

        console.log("Total Fresh Enquiries:", data.total_fresh_enquiries);
        freshEnquiriesElement.textContent = data.total_fresh_enquiries;
    } catch (error) {
        console.error("Error fetching total fresh enquiries:", error);
        freshEnquiriesElement.textContent = `Error: ${error.message}`;
    }
}

// Call the function when the page loads
document.addEventListener("DOMContentLoaded", fetchTotalFreshEnquiries);
