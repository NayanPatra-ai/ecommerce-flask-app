from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = "secret123"

# Sample Products
products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 50000,
        "image": "images/laptop.jpg"
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 20000,
        "image": "images/phone.jpg"
    },
    {
        "id": 3,
        "name": "Headphones",
        "price": 2000,
        "image": "images/headphone.jpg"
    }
]

# Fake user database
users = {}

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html', products=products)

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['user'] = username
            session['cart'] = []
            return redirect(url_for('home'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('cart', None)
    return redirect(url_for('home'))

# ---------------- ADD TO CART ----------------
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):

    if 'cart' not in session:
        session['cart'] = []

    for product in products:
        if product['id'] == product_id:
            session['cart'].append(product)

    session.modified = True   # VERY IMPORTANT 

    return redirect(url_for('view_cart'))

# ---------------- VIEW CART ----------------
@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

# ---------------- REMOVE ITEM ----------------
@app.route('/remove/<int:index>')
def remove(index):
    if 'cart' in session:
        session['cart'].pop(index)
    return redirect(url_for('view_cart'))

# ---------------- CHECKOUT ----------------
@app.route('/checkout')
def checkout():
    if 'cart' not in session:
        return "Cart is empty!"

    total = sum(item['price'] for item in session['cart'])
    session['cart'] = []
    return f"Payment Successful! Total Paid: ₹{total}"

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)