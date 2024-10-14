from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(150))
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('Password is not a readable')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password=password)
    
    def __str__(self):
        return '<Customer %r>' % Customer.id


class Product(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    previous_price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    product_picture = db.Column(db.String(1000), nullable=False)
    flash_sale = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    carts = db.relationship('Cart', backref=db.backref('product', lazy=True))
    orders = db.relationship('Order', backref=db.backref('product', lazy=True))

    def __str__(self):
         return '<Product> %r' % self.product_name
    

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __str__(self):
        return '<Cart %r>' % self.id


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    # payment_id = db.column(db.String(1000), nullable=False)

    Customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __str__(self):
        return '<Order %r>'  % self.id
    
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.Enum('Plastic', 'Metal', 'Cloths', 'Furniture', 'Oders', name='Item_type_range'), nullable=False)
    item_description = db.Column(db.String(1000), nullable=False)
    quantity = db.Column(db.Enum('0-5kg', '5kg-10kg', '10kg-20kg', ' > 20kg', name='quantity_range'), nullable=False)
    date_of_appointment = db.Column(db.Date, nullable=False)
    time_of_appointment = db.Column(db.Time, nullable=False)
    item_picture = db.Column(db.String(1000), nullable=True)
    latitude =db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    Customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def __str__(self):
        return '<Booking %r>' % self.id


    
    
