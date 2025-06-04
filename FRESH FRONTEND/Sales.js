async function fetchTotalSales() {
    const salesCountElement = document.getElementById("salesCount");
    if (!salesCountElement) {
        console.error("Element with ID 'salesCount' not found.");
        return;
    }

    salesCountElement.textContent = "Loading...";

    try {
        const response = await fetch('http://127.0.0.1:5000/sales'); // Replace with actual backend URL if needed

        const contentType = response.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Invalid JSON response from server");
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Failed to fetch total sales");
        }

        console.log("Total Sales:", data.total_sales);
        salesCountElement.textContent = data.total_sales;
    } catch (error) {
        console.error("Error fetching total sales:", error);
        salesCountElement.textContent = `Error: ${error.message}`;
    }
}

// Call the function when the page loads
document.addEventListener("DOMContentLoaded", fetchTotalSales);
