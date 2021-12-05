
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, widgets
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from markupsafe import Markup
from wtforms.widgets.core import html_params

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[ DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # check if username is already in use
    def validate_username(self, username):
        client = User.query.filter_by(username=username.data).first()
        if client is not None:
            raise ValidationError('Username already in use, please use a different username')

    # check if email is already in use
    def validate_email(self, email):
        client = User.query.filter_by(email = email.data).first()
        if client is not None:
            raise ValidationError('Email already in use, please use a different email')



class bankform(FlaskForm):
    bank = SelectField(u'Bank', choices=[('None', 'Which Bank are You Visiting...'), ('Bank of America','Bank of America'), ('chase', 'Chase Bank')])
    department = SelectField(u'Department', choices=[('None', 'Which Department are You Visiting...'),('checking_and_savings','Checking and Savings'), ('credit_and_debit_cards', 'Credit and Debit Cards'), ('home_loans', 'Home Loans'), ('investments', 'Investments')])
    submit=SubmitField('Confirm Booking')


class hospitalform(FlaskForm):
    hospital = SelectField(u'Hospital', choices=[('None', 'Which Hospital are You Visiting...'), ('Yale Health','Yale Health'), ('Yale New haven Hospital', 'Yale New haven Hospital')])
    department = SelectField(u'Department', choices=[('None', 'Which Department are You Visiting...'),('Inquiry','Inquiry'), ('Admissions', 'Admissions'), ('Consultaion', 'Consultaion'), ('Laboratory', 'Laboratory'), ('Pharmacy', 'Pharmacy')])
    submit=SubmitField('Confirm Booking')