# Restaurant Finder Web App

This web application built with Flask allows users to search for restaurants, filter them by various criteria, and discover new dining options based on location and cuisine preferences.

## Features

- **Search by Location**: Find restaurants near a specified latitude and longitude within a radius.
- **Search by Name**: Look up restaurants by name, with options to filter by cuisine and country.
- **Image Recognition Search**: Upload an image to find restaurants known for specific cuisines (mock implementation).
- **Filtering**: Filter restaurants by name, country, average spending range, and cuisine.
- **Pagination**: Display search results across multiple pages for easier navigation.
- **Dropdown Lists**: Retrieve distinct lists of countries and cuisines available in the database.

## Technologies Used

- **Flask**: Python web framework used for backend development.
- **SQLAlchemy**: ORM for interacting with the database.
- **Bootstrap**: Frontend framework for responsive design.
- **Haversine Formula**: Calculates distances between geographic coordinates for location-based searches.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/restaurant-finder.git
   cd restaurant-finder
