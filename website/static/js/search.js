const searchInput = document.getElementById('searchInput');
const searchResults = document.querySelector('.search-results ul');

searchInput.addEventListener('input', () => {
  const query = searchInput.value.trim();

  if (query !== '') {
    fetch(`/search?query=${query}`)
      .then(response => response.text())
      .then(data => {
        // Update the search results area with the HTML content received
        searchResults.innerHTML = data;
      })
      .catch(error => {
        console.error('Error fetching search results:', error);
      });
  } else {
    searchResults.innerHTML = ''; // Clear results if the query is empty
  }
});
