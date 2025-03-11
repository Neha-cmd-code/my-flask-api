from flask import Flask, request, jsonify
from functools import wraps
from faker import Faker
import random
import pandas as pd

app = Flask(__name__)

# Initialize Faker
fake = Faker()

# Function to generate a single product entry
def generate_product(product_id):
    return {
        'id': product_id,
        'name': fake.word().capitalize() + ' ' + fake.word().capitalize(),
        'description': fake.sentence(nb_words=10),
        'price': round(random.uniform(5.0, 500.0), 2),
        'category': fake.random_element(elements=('Electronics', 'Clothing', 'Home', 'Toys', 'Sports', 'Automotive')),
        'stock_quantity': random.randint(0, 1000),
        'rating': round(random.uniform(1.0, 5.0), 1),
        'release_date': fake.date_between(start_date='-5y', end_date='today').isoformat()
    }

# Number of products to generate
num_products = 1000  # Adjust this number as needed

# Generate dataset
product_list = [generate_product(i) for i in range(1, num_products + 1)]

# Convert to DataFrame
df = pd.DataFrame(product_list)

# Convert DataFrame to dictionary
products_data = df.to_dict(orient='records')

# Mock database of API keys
API_KEYS = {
    "ef229daa-d058-4dd4-9c93-24761842aec5": "Client A",
    "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6": "Client B"
}

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if api_key and api_key in API_KEYS:
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Invalid or missing API key"}), 403
    return decorated_function

@app.route('/api/products', methods=['GET'])
@require_api_key
def get_products():
    return jsonify(products_data)

if __name__ == '__main__':
    app.run(debug=True)
