fetch('http://localhost:5000/Gopen-enquiries')
  .then(response => response.json())
  .then(data => {
    document.getElementById('Gopen-enquiries').innerHTML = data.total_open_enquiries_global;
  })
  .catch(error => {
    console.error('Error fetching Gopen-enquiries:', error);
  });
