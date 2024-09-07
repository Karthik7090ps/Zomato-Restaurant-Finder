// Debounce function to prevent excessive calls
function debounce(func, delay) {
    let debounceTimer;
    return function () {
        const context = this;
        const args = arguments;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => func.apply(context, args), delay);
    };
}

// Function to create restaurant cards
function createRestaurantCard(restaurant) {
    const col = document.createElement('div');
    col.classList.add('col-md-4');

    col.innerHTML = `
        <div class="card restaurant-card">
            <img src="${restaurant.image_url || '/static/images/placeholder.png'}" class="card-img-top" alt="${restaurant.name}">
            <div class="card-body">
                <h5 class="card-title">${restaurant.name}</h5>
                <p class="card-text">${restaurant.locality_verbose}</p>
                <p>Average Spend: $${restaurant.avg_spend}</p>
                <p>Rating: ${restaurant.aggregate_rating} (${restaurant.rating_text})</p>
                <button class="btn btn-info" onclick="window.location.href='/restaurant/${restaurant.id}'">View Details</button>
            </div>
        </div>
    `;
    return col;
}


// Fetch and display restaurants
async function fetchRestaurants(filters = {}, page = 1, per_page = 8) {
    let queryString = Object.keys(filters)
        .map(key => `${key}=${encodeURIComponent(filters[key])}`)
        .join('&');
    queryString += `&page=${page}&per_page=${per_page}`;

    try {
        const response = await fetch(`/search/filter?${queryString}`);
        const data = await response.json();

        const restaurantList = document.getElementById('restaurant-list');
        restaurantList.innerHTML = '';

        if (data.length === 0) {
            restaurantList.innerHTML = '<p class="text-center">No restaurants found.</p>';
            return false;  // Indicate that no results were found
        }

        data.forEach(restaurant => {
            const col = createRestaurantCard(restaurant);
            restaurantList.appendChild(col);
        });

        return true;  // Indicate that results were found
    } catch (error) {
        console.error('Error fetching restaurants:', error);
        return false;  // Indicate an error occurred
    }
}

// Fetch restaurants by name
async function fetchRestaurantsByName(name, page = 1) {
    try {
        const response = await fetch(`/search/name?name=${encodeURIComponent(name)}&page=${page}`);
        const data = await response.json();

        const restaurantList = document.getElementById('restaurant-list');
        restaurantList.innerHTML = '';

        if (data.length === 0) {
            restaurantList.innerHTML = '<p class="text-center">No restaurants found with that name.</p>';
            return;
        }

        data.forEach(restaurant => {
            const col = createRestaurantCard(restaurant);
            restaurantList.appendChild(col);
        });
    } catch (error) {
        console.error('Error fetching restaurants by name:', error);
    }
}

// Initial fetch on page load
let currentPage = 1;
let currentFilters = {};
fetchRestaurants({}, currentPage);

// Search by ID
document.getElementById('search-id-btn').addEventListener('click', async () => {
    const id = document.getElementById('search-id').value;
    if (!id) return;

    try {
        const response = await fetch(`/restaurant/${id}`);
        if (response.ok) {
            window.location.href = `/restaurant/${id}`;
        } else {
            alert('Restaurant not found.');
        }
    } catch (error) {
        console.error('Error searching by ID:', error);
    }
});

// Search by Name with Debounce
document.getElementById('search-name').addEventListener('input', debounce(async () => {
    const name = document.getElementById('search-name').value;
    if (!name) {
        currentFilters = {};
        fetchRestaurants({}, currentPage);
        return;
    }
    currentFilters = { name };
    fetchRestaurantsByName(name, currentPage);
}, 300));

// Search by Location
document.getElementById('search-location-btn').addEventListener('click', async () => {
    const latitude = document.getElementById('latitude').value;
    const longitude = document.getElementById('longitude').value;
    const radius = document.getElementById('radius').value;

    if (!latitude || !longitude || !radius) {
        alert('Please enter latitude, longitude, and radius.');
        return;
    }

    currentFilters = {
        latitude,
        longitude,
        radius,
    };

    try {
        const response = await fetch(`/search/location?latitude=${latitude}&longitude=${longitude}&radius=${radius}`);
        const data = await response.json();

        const restaurantList = document.getElementById('restaurant-list');
        restaurantList.innerHTML = '';

        if (data.length === 0) {
            restaurantList.innerHTML = '<p class="text-center">No restaurants found in this area.</p>';
            return;
        }

        data.forEach(restaurant => {
            const col = createRestaurantCard(restaurant);
            restaurantList.appendChild(col);
        });
    } catch (error) {
        console.error('Error searching by location:', error);
    }
});

// Search by Image
document.getElementById('search-image-btn').addEventListener('click', async () => {
    const imageInput = document.getElementById('search-image');
    if (imageInput.files.length === 0) {
        alert('Please select an image.');
        return;
    }

    const formData = new FormData();
    formData.append('image', imageInput.files[0]);

    try {
        const response = await fetch('/search/image', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();

        const restaurantList = document.getElementById('restaurant-list');
        restaurantList.innerHTML = '';

        if (data.length === 0) {
            restaurantList.innerHTML = '<p class="text-center">No restaurants found for this image.</p>';
            return;
        }

        data.forEach(restaurant => {
            const col = createRestaurantCard(restaurant);
            restaurantList.appendChild(col);
        });
    } catch (error) {
        console.error('Error searching by image:', error);
    }
});

// Apply Filters
document.getElementById('filter-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    currentFilters = {
        country_code: document.getElementById('country').value,
        min_spend: document.getElementById('min-spend').value,
        max_spend: document.getElementById('max-spend').value,
        cuisine: document.getElementById('cuisine').value.replace(/\s+/g, ''),
    };
    

    const resultsFound = await fetchRestaurants(currentFilters, 1);
    if (!resultsFound) {
        alert('No restaurants found with the applied filters.');
    }
});


// Pagination
document.getElementById('prev-page').addEventListener('click', (event) => {
    event.preventDefault();
    if (currentPage > 1) {
        currentPage--;
        fetchRestaurants(currentFilters, currentPage);
    }
});

document.getElementById('next-page').addEventListener('click', (event) => {
    event.preventDefault();
    currentPage++;
    fetchRestaurants(currentFilters, currentPage);
});

// Fetch countries and cuisines for dropdowns
async function populateDropdowns() {
    try {
        const countryResponse = await fetch('/dropdowns/countries');
        const countries = await countryResponse.json();
        const countryDropdown = document.getElementById('country');
        countries.forEach(country => {
            const option = document.createElement('option');
            option.value = country;
            option.text = country;
            countryDropdown.appendChild(option);
        });

        const cuisineResponse = await fetch('/dropdowns/cuisines');
        const cuisines = await cuisineResponse.json();
        const cuisineDropdown = document.getElementById('cuisine');
        cuisines.forEach(cuisine => {
            const option = document.createElement('option');
            option.value = cuisine;
            option.text = cuisine;
            cuisineDropdown.appendChild(option);
        });
    } catch (error) {
        console.error('Error fetching dropdowns:', error);
    }
}

populateDropdowns();
