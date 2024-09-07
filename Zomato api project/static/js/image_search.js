document.getElementById('image-search-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const formData = new FormData();
    formData.append('image', document.getElementById('image').files[0]);

    const response = await fetch('/search/image', {
        method: 'POST',
        body: formData
    });
    
    const data = await response.json();
    const resultContainer = document.getElementById('image-search-results');
    resultContainer.innerHTML = '';
    data.forEach(restaurant => {
        const div = document.createElement('div');
        div.classList.add('restaurant');
        div.innerHTML = `
            <h2>${restaurant.name}</h2>
            <p>${restaurant.locality_verbose}</p>  <!-- Changed from 'description' -->
            <p>Average Spend: $${restaurant.avg_spend}</p>
            <p>Cuisines: ${restaurant.cuisines}</p>  <!-- Changed from 'cuisine' -->
            <img src="${restaurant.image_url}" alt="${restaurant.name}">
            <button onclick="window.location.href='/restaurant/${restaurant.id}'">View Details</button>
        `;
        resultContainer.appendChild(div);
    });
});
