from app import app, db
from flask import jsonify, request, render_template
from app.models import Restaurant
from app.utils import haversine
from sqlalchemy import or_  # Add this import at the top of the file

@app.route('/')
def home():
    return render_template('index.html')

# Get restaurant by ID
@app.route('/restaurant/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return render_template('details.html', restaurant=restaurant)
    return jsonify({'message': 'Restaurant not found'}), 404

# Get list of restaurants (with pagination)
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    page = request.args.get('page', 1, type=int)
    per_page = 8
    restaurants = Restaurant.query.paginate(page=page, per_page=per_page, error_out=False)

    results = [{
        'id': r.id,
        'name': r.name,
        'locality_verbose': r.locality_verbose,
        'country_code': r.country_code,
        'city': r.city,
        'address': r.address,
        'longitude': r.longitude,
        'latitude': r.latitude,
        'cuisine': r.cuisines,
        'avg_spend': r.avg_spend,
        'currency': r.currency,
        'has_table_booking': r.has_table_booking,
        'has_online_delivery': r.has_online_delivery,
        'is_delivering_now': r.is_delivering_now,
        'switch_to_order_menu': r.switch_to_order_menu,
        'price_range': r.price_range,
        'aggregate_rating': r.aggregate_rating,
        'rating_color': r.rating_color,
        'rating_text': r.rating_text,
        'votes': r.votes
    } for r in restaurants.items]
    
    return jsonify(results)

# Search restaurants by location
@app.route('/search/location', methods=['GET'])
def search_by_location():
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    radius = request.args.get('radius', 3, type=float)
    
    restaurants = Restaurant.query.all()
    nearby_restaurants = []

    for restaurant in restaurants:
        distance = haversine(latitude, longitude, restaurant.latitude, restaurant.longitude)
        if distance <= radius:
            nearby_restaurants.append({
                'id': restaurant.id,
                'name': restaurant.name,
                'locality_verbose': restaurant.locality_verbose,
                'country_code': restaurant.country_code,
                'city': restaurant.city,
                'address': restaurant.address,
                'longitude': restaurant.longitude,
                'latitude': restaurant.latitude,
                'cuisine': restaurant.cuisines,
                'avg_spend': restaurant.avg_spend,
                'currency': restaurant.currency,
                'has_table_booking': restaurant.has_table_booking,
                'has_online_delivery': restaurant.has_online_delivery,
                'is_delivering_now': restaurant.is_delivering_now,
                'switch_to_order_menu': restaurant.switch_to_order_menu,
                'price_range': restaurant.price_range,
                'aggregate_rating': restaurant.aggregate_rating,
                'rating_color': restaurant.rating_color,
                'rating_text': restaurant.rating_text,
                'votes': restaurant.votes
            })
    
    return jsonify(nearby_restaurants)

# Search restaurants by image
@app.route('/search/image', methods=['POST'])
def search_by_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No image provided'}), 400

    image = request.files['image']
    
    # Mock response for now. You can integrate image recognition logic here.
    mock_response = Restaurant.query.filter(Restaurant.cuisines.like('%bengali%')).all()

    results = [{
        'id': r.id,
        'name': r.name,
        'locality_verbose': r.locality_verbose,
        'country_code': r.country_code,
        'city': r.city,
        'address': r.address,
        'longitude': r.longitude,
        'latitude': r.latitude,
        'cuisine': r.cuisines,
        'avg_spend': r.avg_spend,
        'currency': r.currency,
        'has_table_booking': r.has_table_booking,
        'has_online_delivery': r.has_online_delivery,
        'is_delivering_now': r.is_delivering_now,
        'switch_to_order_menu': r.switch_to_order_menu,
        'price_range': r.price_range,
        'aggregate_rating': r.aggregate_rating,
        'rating_color': r.rating_color,
        'rating_text': r.rating_text,
        'votes': r.votes
    } for r in mock_response]

    return jsonify(results)

# Search restaurants by name
@app.route('/search/name', methods=['GET'])
def search_by_name():
    name = request.args.get('name', '').lower()

    # Fetch all restaurants that match the name (case-insensitive)
    results = Restaurant.query.filter(Restaurant.name.ilike(f'%{name}%')).all()

    # Convert results to a dictionary
    response = [{
        'id': r.id,
        'name': r.name,
        'cuisine': r.cuisines,
        'avg_spend': r.avg_spend,
        'locality_verbose': r.locality_verbose,
        'city': r.city,
        'address': r.address,
        'country_code': r.country_code,
        'longitude': r.longitude,
        'latitude': r.latitude,
        'currency': r.currency,
        'has_table_booking': r.has_table_booking,
        'has_online_delivery': r.has_online_delivery,
        'is_delivering_now': r.is_delivering_now,
        'switch_to_order_menu': r.switch_to_order_menu,
        'price_range': r.price_range,
        'aggregate_rating': r.aggregate_rating,
        'rating_color': r.rating_color,
        'rating_text': r.rating_text,
        'votes': r.votes
    } for r in results]

    # Sort based on how close the name matches the input:
    # 1. Exact match first
    # 2. Name starts with the search string
    # 3. Name contains the search string anywhere
    # 4. Fallback to alphabetical sort
    sorted_response = sorted(response, key=lambda r: (
        r['name'].lower() == name,      # Exact match
        r['name'].lower().startswith(name),  # Starts with name
        name in r['name'].lower(),      # Contains name anywhere
        r['name'].lower()               # Fallback: alphabetical
    ), reverse=True)

    return jsonify(sorted_response)

# Filter restaurants by criteria
@app.route('/search/filter', methods=['GET'])
def filter_restaurants():
    name = request.args.get('name', '').strip()
    country_code = request.args.get('country_code', '').strip()
    min_spend = request.args.get('min_spend', 0, type=float)
    max_spend = request.args.get('max_spend', 10000, type=float)
    cuisine = request.args.get('cuisine', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 8, type=int)

    query = Restaurant.query

    # Apply name filter
    if name:
        query = query.filter(Restaurant.name.ilike(f'%{name}%'))

    # Apply country code filter
    if country_code:
        query = query.filter(Restaurant.country_code == country_code)

    # Apply spending filters
    query = query.filter(Restaurant.avg_spend >= min_spend, Restaurant.avg_spend <= max_spend)

    # Apply cuisine filters
    if cuisine:
        cuisine_list = [c.strip() for c in cuisine.split(',') if c.strip()]
        if cuisine_list:
            cuisine_filters = [Restaurant.cuisines.ilike(f'%{cuisine}%') for cuisine in cuisine_list]
            query = query.filter(or_(*cuisine_filters))

    # Pagination
    results = query.paginate(page=page, per_page=per_page, error_out=False)  # Removed extra argument

    # Serialize results
    serialized_results = [{
        'id': r.id,
        'name': r.name,
        'locality_verbose': r.locality_verbose,
        'city': r.city,
        'address': r.address,
        'country_code': r.country_code,
        'longitude': r.longitude,
        'latitude': r.latitude,
        'avg_spend': r.avg_spend,
        'currency': r.currency,
        'has_table_booking': r.has_table_booking,
        'has_online_delivery': r.has_online_delivery,
        'is_delivering_now': r.is_delivering_now,
        'switch_to_order_menu': r.switch_to_order_menu,
        'price_range': r.price_range,
        'aggregate_rating': r.aggregate_rating,
        'rating_color': r.rating_color,
        'rating_text': r.rating_text,
        'votes': r.votes
    } for r in results.items]
    
    return jsonify(serialized_results)

# Get distinct list of countries
@app.route('/dropdowns/countries', methods=['GET'])
def get_countries():
    countries = db.session.query(Restaurant.country_code).distinct().all()
    print(countries)
    return jsonify([country[0] for country in countries])

# Get distinct list of cuisines
@app.route('/dropdowns/cuisines', methods=['GET'])
def get_cuisines():
    # Fetch distinct cuisine strings from the database
    cuisine_strings = db.session.query(Restaurant.cuisines).distinct().all()

    # Initialize a set to store individual cuisines
    cuisine_set = set()

    # Loop through each distinct cuisine string
    for cuisine_str in cuisine_strings:
        if cuisine_str[0]:
            # Split the string by commas and add each cuisine to the set after stripping
            for cuisine in cuisine_str[0].split(','):
                cuisine_set.add(cuisine.strip())

    # Convert the set to a sorted list
    sorted_cuisines = sorted(list(cuisine_set))

    return jsonify(sorted_cuisines)

