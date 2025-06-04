async function fetchTotalSalesIndia() {
    const salesIndiaElement = document.getElementById("salesIndiaCount");
    if (!salesIndiaElement) {
        console.error("Element with ID 'salesIndiaCount' not found.");
        return;
    }

    salesIndiaElement.textContent = "Loading...";

    try {
        const response = await fetch('http://127.0.0.1:5000/Isales'); // Update URL if needed

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Invalid JSON response from server");
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to fetch total sales (India)");
        }

        console.log("Total Sales (India):", data.total_sales_india);
        salesIndiaElement.textContent = data.total_sales_india;
    } catch (error) {
        console.error("Error fetching total sales (India):", error);
        salesIndiaElement.textContent = `Error: ${error.message}`;
    }
}

// Call the function when the page loads
document.addEventListener("DOMContentLoaded", fetchTotalSalesIndia);
