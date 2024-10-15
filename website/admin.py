from flask import Blueprint, render_template, flash, send_from_directory, redirect, request
from flask_login import login_required, current_user
from .forms import ShopItemsForm, OrderForm, BookingForm
from werkzeug.utils import secure_filename
from .models import Product, Order, Customer, Booking
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)

@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id == 1:
        form = ShopItemsForm()

        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data

            file_name = secure_filename(file.filename)

            file_path = f'./media/{file_name}'

            file.save(file_path)

            new_shop_item = Product()
            new_shop_item.product_name = product_name
            new_shop_item.current_price = current_price
            new_shop_item.previous_price = previous_price
            new_shop_item.in_stock = in_stock
            new_shop_item.flash_sale = flash_sale

            new_shop_item.product_picture = file_path

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name} added Successfuly')
                print('Product Added')
                return render_template('add-shop-items.html', form=form)
            except Exception as e:
                print(e)
                flash('Product Not Added')


        return render_template('add-shop-items.html', form=form)
    
    return render_template('404.html')

@admin.route('shop_items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1:
        items = Product.query.order_by(Product.date_added).all()
        return render_template('shop_items.html', items=items)
    render_template('404.html')

@admin.route('/update_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.id == 1:
        form = ShopItemsForm()

        item_to_update = Product.query.get(item_id)

        form.product_name.render_kw = {'placeholder': item_to_update.product_name}
        form.previous_price.render_kw = {'placeholder': item_to_update.previous_price}
        form.current_price.render_kw = {'placeholder': item_to_update.current_price}
        form.in_stock.render_kw = {'placeholder': item_to_update.in_stock}
        form.flash_sale.render_kw = {'placeholder': item_to_update.flash_sale}

        if form.validate_on_submit():
            product_name = form.product_name.data
            previous_price = form.previous_price.data
            current_price = form.current_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data

            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'

            file.save(file_path)

            try:
                Product.query.filter_by(id=item_id).update(dict(product_name=product_name,
                                                                previous_price=previous_price,
                                                                current_price=current_price,
                                                                in_stock=in_stock,
                                                                flash_sale=flash_sale,
                                                                product_picture=file_path))
                db.session.commit()
                flash(f'{product_name} updated Successfully')
                print('Product Updated')
                return redirect('/shop_items')
            except Exception as e:
                print('Product Not Updated', e)
                flash('Item Not Updated !!!')

        return render_template('update_item.html', form=form)

    render_template('404.html')

@admin.route('/delete_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 1:
        try:
            item_to_delete = Product.query.get(item_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('One Item deleted')
            return redirect('/shop_items')
        except Exception as e:
            print('Item not deleted', e)
            flash('Item not deleted!!')
        return redirect('/shop_items')

    return render_template('404.html')

@admin.route('/view_orders')
@login_required
def order_view():
    if current_user.id == 1:
        orders = Order.query.all()
        return render_template('view_orders.html', orders=orders)
    return render_template('404.html')


@admin.route('/update_order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.id == 1:
        form = OrderForm()

        order = Order.query.get(order_id)

        if form.validate_on_submit():
            status = form.order_status.data
            order.status = status

            try:
                db.session.commit()
                flash(f'Order {order_id} Updated successfully')
                return redirect('/view_orders')
            except Exception as e:
                print(e)
                flash(f'Order {order_id} not updated')
                return redirect('/view_orders')

        return render_template('update_order.html', form=form)

    return render_template('404.html')


@admin.route('/customers')
@login_required
def display_customers():
    if current_user.id == 1:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')


@admin.route('/admin_page')
@login_required
def admin_page():
    if current_user.id == 1:
        return render_template('admin.html')
    return render_template('404.html')


@admin.route('/view_bookings', methods=['GET'])
@login_required
def view_bookings():
    if current_user.id == 1:  # Ensure only admins can access
        bookings = Booking.query.all()  # Fetch all bookings
        return render_template('view_bookings.html', bookings=bookings)
    return render_template('404.html')


@admin.route('/update_booking/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def update_booking(booking_id):
    if current_user.id == 1:  # Only allow admins
        form = BookingForm()  # Assuming you have a BookingForm defined

        # Retrieve the booking from the database
        booking = Booking.query.get_or_404(booking_id)

        # Populate the form with the current booking data
        if request.method == 'GET':
            form.item_type.data = booking.item_type
            form.item_description.data = booking.item_description
            form.quantity.data = booking.quantity
            form.date_of_appointment.data = booking.date_of_appointment
            form.time_of_appointment.data = booking.time_of_appointment

        # Validate the form on submission
        if form.validate_on_submit():
            booking.item_type = form.item_type.data
            booking.item_description = form.item_description.data
            booking.quantity = form.quantity.data
            booking.date_of_appointment = form.date_of_appointment.data
            booking.time_of_appointment = form.time_of_appointment.data

            try:
                db.session.commit()
                flash(f'Booking {booking_id} updated successfully')
                return redirect('/view-bookings')
            except Exception as e:
                print(e)
                flash(f'Failed to update Booking {booking_id}')
                return redirect('/view-bookings')

        # Pass the booking object to the template
        return render_template('booking_update.html', form=form, booking=booking)

    return render_template('404.html')


@admin.route('/delete_booking/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    if current_user.id == 1:  # Only allow admins
        booking = Booking.query.get_or_404(booking_id)

        try:
            db.session.delete(booking)
            db.session.commit()
            flash(f'Booking {booking_id} deleted successfully')
        except Exception as e:
            print(e)
            flash(f'Failed to delete Booking {booking_id}')

        return redirect('/view_bookings')
    
    return render_template('404.html')


