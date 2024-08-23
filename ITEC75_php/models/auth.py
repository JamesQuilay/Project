from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash
from . import db  
from flask_login import login_user, login_required, logout_user, current_user
import random
import string

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember' in request.form  # Check if 'remember' is in the form data

        user = User.query.filter_by(email=email).first()

        if user and not user.is_admin:
            if user.check_password(password):
                login_user(user, remember=remember)  # Pass the remember parameter
                return redirect(url_for('views.featured_watch'))
            else:
                flash('Incorrect password. Please try again.', category='error')
        else:
            flash('Email not found. Please check your credentials.', category='error')

    return render_template('login.html', user=current_user)
@auth.route('/adminLogin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        admin_user = User.query.filter_by(email=email, is_admin=True).first()

        if admin_user:
            if admin_user.check_password(password):
                login_user(admin_user)
                flash('Admin login successful!', category='success')
                return redirect(url_for('views.admin_overview'))
            else:
                flash('Incorrect password. Please try again.', category='error')
        else:
            flash('Admin email not found. Please check your credentials.', category='error')

    return render_template('admin_login.html', user=current_user)

from sqlalchemy.exc import IntegrityError


def generate_unique_id(length=6):
    """Generate a unique identifier of specified length."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        unique_id = generate_unique_id()
        username = f"{first_name.lower()}.{last_name.lower()}@{unique_id}"

        # Ensure fields are not None
        email = email or ''
        username = username or ''
        password1 = password1 or ''
        password2 = password2 or ''

        user_with_email = User.query.filter_by(email=email).first()
        if user_with_email:
            flash('Email already exists.', category='error')
            return render_template('sign_up.html', user=current_user)


        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')

        elif len(first_name) < 2:
            flash('first name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, username=username, first_name=first_name, last_name=last_name, password_hash=generate_password_hash(password1))
            db.session.add(new_user)
            try:
                db.session.commit()
                return redirect(url_for('auth.login'))
            except IntegrityError:
                db.session.rollback()
                flash('Email or Username already exists. Please choose a different one.', category='error')

    return render_template('sign_up.html', user=current_user)



@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))
