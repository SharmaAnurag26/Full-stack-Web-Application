fetch('http://localhost:5000/Gdealers')
  .then(response => response.json())
  .then(data => {
    document.getElementById('Gdealers').innerHTML = data.unique_dealers_global;
  })
  .catch(error => {
    console.error('Error fetching Gdealers:', error);
  });
