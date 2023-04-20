from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!',category='success')
                login_user(user, remember=True)
                return redirect(url_for('todos.home'))
            else:
                flash('Incorrect Password, Try Again!',category='danger')
        else:
            flash('Email does not exists!',category='danger')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sigin_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('eMail must be greater than 4 characters.',category='danger')
        elif len(name) < 2:
            flash('Name must be greater than 2 characters.',category='danger')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters.',category='danger')
        elif password1 != password2:
            flash('Password don\'t match.',category='danger')
        else:
            # add user to database
            new_user = User(
                email=email,
                password=generate_password_hash(password1,method='sha256'),
                name=name
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!',category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)