import json
from flask import Flask, render_template, request, session, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "osc2026"


@app.route("/")
def home():
    cart = session.get('cart', {})
    selected_addons = session.get('selected_addons', {})
    flowers, addons = load_data()
    total = calculate_total(cart)
    return render_template("index.html", flowers=flowers, addons=addons, cart=cart, total=total, selected_addons=selected_addons)


def load_data():
    with open('data/flowers.json') as file:
        flowers = json.load(file)
        
    with open('data/addons.json') as file:
        addons = json.load(file)

    return flowers, addons


@app.route('/add', methods=['POST'])
def add_flower():
    flower = request.form['flower']
    quantity = int(request.form['quantity'])
    flowers = load_data()
    cart = session.get('cart', {})
    

    if flower not in flowers:
        flash("Invalid flower selected.")
        return redirect(url_for('index'))

    if flower in cart:
        cart[flower]['quantity'] += quantity
    else:
        cart[flower] = {
            'price': flowers[flower]['price'],
            'quantity': quantity
        }

    session['cart'] = cart
    session.modified = True
    flash(f"{quantity} {flower}(s) added to cart.")
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<item>')
def remove_from_cart(item):
    cart = session.get('cart', {})
    if item in cart:
        del cart[item]
        session['cart'] = cart
        session.modified = True
        flash(f"{item} removed from cart.")
    
        
    else:
        flash("Item not found in cart.")
        return redirect(url_for('index'))
    
def calculate_total(cart):
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return total
    

@app.route('/select_addon', methods=['POST'])
def select_addon():
    selected_addons = {}
    _, addons = load_data()  # we only need addons

    selected_keys = request.form.getlist('addons')

    for addon in selected_keys:
        if addon in addons:
            selected_addons[addon] = float(addons[addon]['price'])

    session['selected_addons'] = selected_addons
    session.modified = True
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
    