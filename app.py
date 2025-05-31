from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

# Sample product list
dummy_products = [
    {
        "id": 1,
        "name": "Premium T-Shirt - Sky Blue",
        "price": 649,
        "old_price": 850,
        "image": "images/sky_blue_tshirt.jpg",
        "description": "Smooth and comfortable premium t-shirt."
    },
    {
        "id": 2,
        "name": "Designer Polo - Navy",
        "price": 1140,
        "old_price": 1490,
        "image": "images/navy_polo.jpg",
        "description": "Stylish designer polo shirt."
    },
    {
        "id": 3,
        "name": "Streetwear Cap",
        "price": 490,
        "old_price": 590,
        "image": "images/streetwear_cap.jpg",
        "description": "Bold streetwear cap for daily style."
    }
]

@app.route('/')
def home():
    return render_template('index.html', products=dummy_products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((item for item in dummy_products if item["id"] == product_id), None)
    return render_template('product.html', product=product)

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        product = request.form['product']

        # Save to orders.csv
        file_exists = os.path.isfile('orders.csv')
        with open('orders.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Name', 'Phone', 'Address', 'Product'])
            writer.writerow([name, phone, address, product])

        return render_template('success.html', name=name, phone=phone, address=address, product=product)

    product_name = request.args.get('product')
    return render_template('order.html', product_name=product_name)

if __name__ == '__main__':
    app.run(debug=True)
