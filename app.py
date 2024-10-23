from flask import Flask, render_template, request, redirect, session, url_for
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar sesiones

# Inicializar la sesión si no existe
@app.before_request
def init_session():
    if 'products' not in session:
        session['products'] = []

# Página principal: Mostrar productos
@app.route('/')
def index():
    products = session.get('products', [])
    return render_template('index.html', products=products)

# Agregar un nuevo producto
@app.route('/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        new_product = {
            'id': str(uuid.uuid4()),  
            'name': request.form['name'],
            'quantity': int(request.form['quantity']),
            'price': float(request.form['price']),
            'expiration_date': request.form['expiration_date'],
            'category': request.form['category']
        }
        products = session.get('products', [])
        products.append(new_product)
        session['products'] = products
        return redirect(url_for('index'))

# Editar un producto existente
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_product(id):
    products = session.get('products', [])
    product = next((p for p in products if p['id'] == id), None)

    if request.method == 'POST':
        if product:
            product['name'] = request.form['name']
            product['quantity'] = int(request.form['quantity'])
            product['price'] = float(request.form['price'])
            product['expiration_date'] = request.form['expiration_date']
            product['category'] = request.form['category']
            session['products'] = products
        return redirect(url_for('index'))

    return render_template('edit.html', product=product)

# Eliminar un producto
@app.route('/delete/<id>')
def delete_product(id):
    products = session.get('products', [])
    session['products'] = [p for p in products if p['id'] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
