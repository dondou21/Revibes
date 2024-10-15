from flask import Blueprint, render_template, flash, redirect, request, jsonify
from .models import Product, Cart, Order, Booking
from flask_login import login_required, current_user
from .forms import BookingForm
from werkzeug.utils import secure_filename
from . import db
from datetime import date, time, datetime
from intasend import APIService # type: ignore


views = Blueprint('views', __name__)

API_PUBLISHABLE_KEY = 'ISPubKey_test_19c6e0b1-0653-46d8-a2aa-0ef12c308bca'

API_TOKEN = 'ISSecretKey_test_27ec2426-c632-4342-8c5f-9adb1a2a0325'

@views.route('/')
def home():

    items = Product.query.filter_by(flash_sale=True)

    return render_template('home.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else [])

@views.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    form = BookingForm()

    if form.validate_on_submit():
        item_type = form.item_type.data
        item_description = form.item_description.data
        quantity = form.quantity.data
        date_of_appointment = form.date_of_appointment.data
        time_of_appointment = form.time_of_appointment.data
        latitude = form.latitude.data
        longitude = form.latitude.data

        file = form.item_picture.data

        if date_of_appointment < datetime.today().date():
            flash('Date of appointment cannot be in the pass!!!')
            print('Booking Failed')
            return render_template('booking.html', form=form)
        
        if not (time_of_appointment >= time(6, 0) and time_of_appointment <= time(21, 0)):
            flash('Time of appointment must be between 6:00 AM and 9:00 PM !!!')
            print('Booking Failed')
            return render_template('booking.html', form=form)


        if file:
            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            file.save(file_path)
        else:
            file_path = None

        customer_link =current_user.id

        new_booking = Booking()
        new_booking.item_type = item_type 
        new_booking.item_description = item_description 
        new_booking.quantity = quantity 
        new_booking.date_of_appointment = date_of_appointment
        new_booking.time_of_appointment = time_of_appointment 
        new_booking.latitude = latitude 
        new_booking.longitude = longitude 

        new_booking.item_picture = file_path

        new_booking.Customer_link = customer_link

        try:
            db.session.add(new_booking)
            db.session.commit()
            flash('Appointment Submitted')
            print('Booking Added')
            return redirect('/', form=form)
        except Exception as e:
            print(e)
            flash('Booking not Added !!!')

    return render_template('booking.html', form=form)


@views.route('/add_to_cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    if item_exists:
        try:
            item_exists.quantity = item_exists.quantity +1
            db.session.commit()
            flash(f'Quantity of { item_exists.product.productname } has been updated')
            return redirect(request.referrer)
        except Exception as e:
            print('Quantity not updated',e)
            flash(f'Quantity of { item_exists.product.product_name } not updated')
            return redirect(request.referrer)
        
    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_link = item_to_add.id
    new_cart_item.customer_link = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.product.product_name} added to cart')
    except Exception as e:
        print('Item not added to cart', e)
        flash(f'{new_cart_item.product.product_name} has not been added to cart')
    
    return redirect(request.referrer)


@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = 0
    for item in cart:
        amount += item.product.current_price * item.quantity

    return render_template('cart.html', cart=cart, amount=amount, total=amount + 1000)


@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity + 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 1000
        }

        return jsonify(data)
    

@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity - 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount +100
        }

        return jsonify(data)
    

@views.route('removecart')
@login_required
def remove_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount
        }

        return jsonify(data)
    


@views.route('/place_order')
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(customer_link=current_user.id)
    if customer_cart:
        try:
            total = 0
            for item in customer_cart:
                total += item.product.current_price * item.quantity

            service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)
            create_order_response = service.collect.mpesa_stk_push(phone_number='254791591966', email=current_user.email,
                                                                   amount=total + 1000, narrative='Purchase of goods')
            
            for item in customer_cart:
                new_order = Order()
                new_order.quantity = item.quantity
                new_order.price = item.product.current_price
                new_order.status = create_order_response['invoice']['state'].capitalize()
                # new_order.payment_id = create_order_response['id']

                new_order.product_link = item.product_link
                new_order.customer_link = item.customer_link

                db.session.add(new_order)

                product = Product.query.get(item.product_link)

                product.in_stock -= item.quantity

                db.session.delete(item)

                db.session.commit()

            flash('Order Placed Successfully')

            return redirect('/orders')
        except Exception as e:
            print(e)
            flash('Order not placed')
            return redirect('/')
    else:
        flash('Your cart is Empty')
        return redirect('/')

    

@views.route('/orders')
@login_required
def order():
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)
    

@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
        return render_template('search.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

    return render_template('search.html')

        
