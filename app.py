from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

# Sample product list
products = [
    {"name": "Premium T shirt", "price": "430 BDT", "image": "/static/tshirt1.png"},
    {"name": "Minimal Hoodie", "price": "1490 BDT", "image": "/static/hoodie1.jpg"},
    {"name": "Streetwear Cap", "price": "490 BDT", "image": "/static/cap1.jpg"}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def product_page():
    return render_template('products.html', products=products)

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
