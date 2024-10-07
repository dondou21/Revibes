from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'Login Page'


@auth.route('/sign-up')
def sign_up():
    return 'Siggn Up  Page'