fetch('http://localhost:5000/Gtotal-fresh-enquiries')
  .then(response => response.json())
  .then(data => {
    document.getElementById('Gtotal-fresh-enquiries').innerHTML = data.total_fresh_enquiries_global;
  })
  .catch(error => {
    console.error('Error fetching Gtotal-fresh-enquiries:', error);
  });
