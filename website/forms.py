from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired

class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), length(min=2)])
    password1 = PasswordField('Enter Your Password', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Confirm Your Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Login')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Change Password')

class ShopItemsForm(FlaskForm):
    product_name = StringField('Name of Product', validators=[DataRequired()])
    current_price = FloatField('Current Price', validators=[DataRequired()])
    previous_price = FloatField('Previous Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Product Picture', validators=[DataRequired()])
    flash_sale = BooleanField('Flash Sale')

    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update') 

class BookingForm(FlaskForm):
    item_type = SelectField('Item Type', choices=[('Plastic', 'Plastic'), ('Metal', 'Metal'), ('Cloths', 'Cloths'), ('Furniture', 'Furniture'), ('Others', 'Others')], validators=[DataRequired()])
    item_description = TextAreaField('Item Description', validators=[DataRequired(), length(max=1000)])
    quantity = SelectField('Quantity', choices=[('0-5kg', '0-5kg'), ('5kg-10kg', '5kg-10kg'), ('10kg-20kg', '10kg-20kg'), (' > 20kg', ' > 20kg')], validators=[DataRequired()])
    date_of_appointment = DateField('Date of Appointment', format='%Y-%m-%d', validators=[DataRequired()])
    time_of_appointment = TimeField('Time of Appointment', format='%H:%M', validators=[DataRequired()])
    item_picture = FileField('Item Picture', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    submit = SubmitField('Submit')
