from flask import Blueprint, render_template

login = Blueprint("login", __name__, url_prefix="/login")

@login.route('/')
def login_home():
    return render_template('login.html')
