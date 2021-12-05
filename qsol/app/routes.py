
from os import error
from flask import render_template, url_for, redirect, flash, request, send_from_directory
import flask_login
from sqlalchemy.orm import session
from werkzeug.utils import validate_arguments
from wtforms.validators import Length, ValidationError
from app import app, db
from app.forms import LoginForm, RegistrationForm, bankform, hospitalform
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Bank, Hospital
from werkzeug.urls import url_parse
import queue


@app.route('/')
@app.route('/index')
def index():
     return render_template('index.html', title='Home Page')

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    # see if user is alreader logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():

        # when login form is submitted, check if the client's credential are authentic else raise errors
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        # creating a variable next page to represent the page user wanted to access before logging in
        next_page = request.args.get('next')

        # if no next page is available, redirect user to index page,
        # also, use url parse to ensure a user does not try to use a malicius site as the next page
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', title = 'Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        client = User(username=form.username.data, email = form.email.data)
        client.set_password(form.password.data)
        db.session.add(client)
        db.session.commit()
        flash('Registration Successful!')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title= 'Register', form=form)

@app.route('/account/<username>')
@login_required
def account(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('account.html', user=user)

@app.route('/banks', methods=['GET', 'POST'])
@login_required
def banks():
    form = bankform()
    if form.validate_on_submit():
        if (bank := request.form.get('bank')) == 'None':
            flash("choose a bank")
            return redirect(request.referrer)

        if (depart := request.form.get('department')) == 'None':
            flash("Choose a department")
            return redirect(request.referrer)
        print(bank)
        print(depart)

        exists = Bank.query.filter_by(username=current_user.username, name=bank, department=depart).first() is not None

        if exists:
            flash("Already in line")
            return redirect(request.referrer)

        booking = Bank(username=current_user.username, name=bank, department=depart)
        db.session.add(booking)
        db.session.commit()

        # Prints

        client_ticket = Bank.query.filter_by(username=current_user.username).all()
        print(client_ticket)

        foo = client_ticket[-1]
        print(foo.department)

        baa=Bank.query.filter_by(name=bank).all()

        print(baa)

        vaar=Bank.query.filter_by(name=bank, department=depart).all()

        print(vaar)

        for item in vaar:
            print(item.id)
            print(item.username)
            print(item.name)
            print(item.department)

    return render_template('banks.html', form = form)

@app.route('/hospital', methods=['GET', 'POST'])
@login_required
def hospital():
    form = hospitalform()
    if form.validate_on_submit():
        data=request.form.get('hospital')
        print(data)
        deta=request.form.get('department')
        print(deta)
    return render_template('hospital.html', form = form)






