from flask import Blueprint, render_template, flash, redirect
from .models import Product
from flask_login import login_required, current_user
from .forms import BookingForm
from werkzeug.utils import secure_filename
from .models import Booking
from . import db
from datetime import date, time, datetime

views = Blueprint('views', __name__)

@views.route('/')
def home():

    items = Product.query.filter_by(flash_sale=True)

    return render_template('home.html', items=items)

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

        
