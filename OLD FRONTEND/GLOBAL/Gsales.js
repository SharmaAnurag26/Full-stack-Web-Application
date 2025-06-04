fetch('http://localhost:5000/Gsales')
  .then(response => response.json())
  .then(data => {
    document.getElementById('Gsales').innerHTML = data.total_sales_global;
  })
  .catch(error => {
    console.error('Error fetching Gsales:', error);
  });
