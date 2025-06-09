# Step 1: main.py

```python
from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load product data
def load_products():
    if os.path.exists('products.json'):
        with open('products.json') as f:
            return json.load(f)
    return []

# Save product data
def save_products(products):
    with open('products.json', 'w') as f:
        json.dump(products, f)

# Load settings
def load_settings():
    if os.path.exists('settings.json'):
        with open('settings.json') as f:
            return json.load(f)
    return {"logo": "", "brand_name": "My Shop"}

# Save settings
def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

@app.route('/')
def home():
    return redirect(url_for('shop'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))
    settings = load_settings()
    return render_template('dashboard.html', settings=settings)

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if 'admin' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        category = request.form['category']

        image = request.files['image']
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        products = load_products()
        products.append({"name": name, "price": price, "description": description, "image": image_path, "category": category})
        save_products(products)

        return redirect(url_for('dashboard'))

    return render_template('add_product.html')

@app.route('/shop')
def shop():
    products = load_products()
    settings = load_settings()
    return render_template('shop.html', products=products, settings=settings)

@app.route('/product/<int:index>')
def product_detail(index):
    products = load_products()
    settings = load_settings()
    if 0 <= index < len(products):
        return render_template('product_detail.html', product=products[index], settings=settings)
    return redirect(url_for('shop'))

@app.route('/settings', methods=['POST'])
def update_settings():
    if 'admin' not in session:
        return redirect(url_for('login'))
    brand_name = request.form['brand_name']
    logo_file = request.files['logo']

    filename = secure_filename(logo_file.filename)
    logo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    logo_file.save(logo_path)

    settings = {"brand_name": brand_name, "logo": logo_path}
    save_settings(settings)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Step 2: requirements.txt

flask
werkzeug

# Step 3: products.json (ফাঁকা অবস্থায় রাখো)
json
[]

# Step 4: settings.json
json
{
  "logo": "",
  "brand_name": "My Shop"
}

# Step 5: Folder Structure

/templates
    login.html
    dashboard.html
    add_product.html
    shop.html
    product_detail.html

/static/uploads
/static/css (যদি CSS লাগে)

# Step 6: login.html

html
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Admin Login</h2>
    <form method="POST">
        <label>Username:</label>
        <input type="text" name="username" required><br><br>
        <label>Password:</label>
        <input type="password" name="password" required><br><br>
        <input type="submit" value="Login">
    </form>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
</body>
</html>
