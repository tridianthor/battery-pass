const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
let timeoutId;

searchInput.addEventListener('input', () => {
    clearTimeout(timeoutId);

    timeoutId = setTimeout(() => {
        performSearch(searchInput.value);
    }, 1500);
});

function performSearch(query) {
    searchResults.innerHTML = `Searching for: "${query}"...`;

    // Simulate search delay (replace with actual search)
    setTimeout(() => {
        fetchSearchResults(query); // Call function to fetch data
    }, 500);
}

function fetchSearchResults(query) {
    // Create a URL with the search query
    const url = `?search=${encodeURIComponent(query)}`;

    setTimeout(() => {
        window.location.href = url;
    }, 500);
}