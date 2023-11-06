from flask import Blueprint, render_template, request,redirect,url_for
from flask_login import login_required, current_user
from . import db
from .models import Product, Cart, CartItem
views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        products = Product.query.all()
        return render_template("index.html", user=current_user, products=products)
    
    else:
        if not Cart.query.filter_by(user_id=current_user.id).first():
            new_cart = Cart(user_id=current_user.id)
            db.session.add(new_cart)
            db.session.commit()
            
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        cartid = cart.id
        itemid = request.form.get('itemid')
        print(cartid)
        newcartitem = CartItem(cart_id=cartid, product_id=itemid)
        db.session.add(newcartitem)
        db.session.commit()
        return redirect(url_for('views.home'))



def cart():
    return render_template("index.html", user=current_user)
