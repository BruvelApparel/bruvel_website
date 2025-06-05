from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React front-end

# Initialize SQLite database
def init_db():
    if not os.path.exists('bruvel.db'):
        conn = sqlite3.connect('bruvel.db')
        c = conn.cursor()
        # Create products table
        c.execute('''CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT NOT NULL
        )''')
        # Create orders table for cart/custom designs
        c.execute('''CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            custom_text TEXT,
            custom_color TEXT,
            quantity INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        # Insert sample products
        sample_products = [
            ('Custom T-Shirt', 19.99, 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60'),
            ('Hoodie', 39.99, 'https://images.unsplash.com/photo-1556821840-3a8f956330af?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60'),
            ('Jeans', 49.99, 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60')
        ]
        c.executemany('INSERT INTO products (name, price, image) VALUES (?, ?, ?)', sample_products)
        conn.commit()
        conn.close()

# Get database connection
def get_db():
    conn = sqlite3.connect('bruvel.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database on startup
init_db()

# API Endpoints
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    products = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(products)

@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    custom_text = data.get('custom_text', '')
    custom_color = data.get('custom_color', '')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO orders (product_id, custom_text, custom_color, quantity) VALUES (?, ?, ?, ?)',
              (product_id, custom_text, custom_color, quantity))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item added to cart'}), 201

@app.route('/api/cart', methods=['GET'])
def get_cart():
    conn = get_db()
    c = conn.cursor()
    c.execute('''SELECT o.id, o.product_id, p.name, p.price, p.image, o.custom_text, o.custom_color, o.quantity
                 FROM orders o JOIN products p ON o.product_id = p.id''')
    cart_items = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(cart_items)

@app.route('/api/cart/<int:order_id>', methods=['DELETE'])
def remove_from_cart(order_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item removed from cart'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
