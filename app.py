import json

from flask import Flask, render_template, request, session, flash, redirect, url_for

app = Flask(__name__)

app.secret_key = "osc2026"

@app.route ('/')
def index():
    flowers,addons = load_data()
    cart = session.get('cart', {})
    total = 111
    return render_template('index.html', flowers=flowers, addons=addons, cart=cart, total= total)

@app.route ('/test')
def test():
    flowers, addons = load_data()
    return render_template("index1.html", flowers=flowers, addons=addons)


def load_data():
    with open ('data/flowers.json') as file: 
        flowers = json.load (file)
        
    with open ('data/addons.json') as file: 
        addons = json.load (file)
       
    return flowers, addons

# Add selected flower to the shopping cart 
@app.route('/add_to_cart', methods=['POST'])  
def add_to_cart():
    flower = request.form['flower'] # get selected flower name 
    quantity= int(request.form['quantity']) # convert quantity to a number
    flowers, addons = load_data() # get flower data from file, ignore addon data 
    cart = session.get('cart', {}) # get cart from session to start fresh
    
    if flower not in flowers: 
        flash("Invalid flower selection.")
        return redirect(url_for('index'))
    
    if flower in cart:
     cart[flower]['quantity'] += quantity # add wxisting quantity
    else: 
        cart[flower] = {
            'price': flowers[flower]['price'],
            'quantity': quantity
        }   
        
    session['cart'] = cart #update session.
    session.modified = True # mark session as modified to ensure it is saved 
    flash(f"{quantity} {flower}(s) have been added to the cart.")
    return redirect(url_for('index'))
    
# Remove an item from the shopping cart
@app.route('/remove_from_cart/<item>')
def remove_from_cart(item):
    cart = session.get('cart', {})
    if item in cart:
        del cart[item]
        session['cart'] = cart
        session.modified = True
        flash(f"{item} has been removed from the cart.")
    else:
        flash(f"{item} is not in the cart.")
    return redirect(url_for('home'))

# @app.route ('/cart')
# def remove_from_cart():
#     cart = session

# Calculate total cost based on cart contents and selected addons
def calculate_total(cart, selected_addons):
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    total = sum(total, sum(selected_addons.values()))
    return total 


if __name__ == '__main__': 
  app.run(debug=True)
