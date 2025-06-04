async function fetchOpenEnquiries() {
    const openEnquiriesElement = document.getElementById("openEnquiriesCountOLD");
    if (!openEnquiriesElement) {
        console.error("Element with ID 'openEnquiriesCountOLD' not found.");
        return;
    }

    openEnquiriesElement.textContent = "Loading...";

    try {
        const response = await fetch('http://127.0.0.1:5000/open-enquiries_old'); // Replace with your actual backend URL
        
        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Invalid JSON response from server");
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to fetch data");
        }

        console.log("Total Open Enquiries:", data.total_open_enquiries);
        openEnquiriesElement.textContent = data.total_open_enquiries;
    } catch (error) {
        console.error("Error fetching open enquiries:", error);
        openEnquiriesElement.textContent = `Error: ${error.message}`;
    }
}

// Call the function when the page loads
document.addEventListener("DOMContentLoaded", fetchOpenEnquiries);
