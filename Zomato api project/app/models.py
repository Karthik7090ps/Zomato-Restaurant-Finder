from app import db

class Restaurant(db.Model):
    __tablename__ = 'zomato'  # This should match your actual table name

    id = db.Column('Restaurant ID', db.Integer, primary_key=True)
    name = db.Column('Restaurant Name', db.String(100), nullable=False)
    country_code = db.Column('Country Code', db.Integer)
    city = db.Column('City', db.String(50))
    address = db.Column('Address', db.String(255))
    locality = db.Column('Locality', db.String(100))
    locality_verbose = db.Column('Locality Verbose', db.String(255))
    longitude = db.Column('Longitude', db.Float)
    latitude = db.Column('Latitude', db.Float)
    cuisines = db.Column('Cuisines', db.String(100))
    avg_spend = db.Column('Average Cost for two', db.Float)
    currency = db.Column('Currency', db.String(10))
    has_table_booking = db.Column('Has Table booking', db.String(5))
    has_online_delivery = db.Column('Has Online delivery', db.String(5))
    is_delivering_now = db.Column('Is delivering now', db.String(5))
    switch_to_order_menu = db.Column('Switch to order menu', db.String(5))
    price_range = db.Column('Price range', db.Integer)
    aggregate_rating = db.Column('Aggregate rating', db.Float)
    rating_color = db.Column('Rating color', db.String(50))
    rating_text = db.Column('Rating text', db.String(50))
    votes = db.Column('Votes', db.Integer)
