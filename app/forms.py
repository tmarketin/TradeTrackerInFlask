from flask_wtf import FlaskForm, Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FormField, FieldList
from wtforms.fields.html5 import DateField, IntegerField, DecimalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Optional
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('E-mail', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField('Repeat password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Please select a different username')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')

class TradeLegForm(FlaskForm):
    opened = SelectField('Opened', choices = ['bought', 'sold'])
    size = IntegerField('Size', validators = [Optional()])
    contract_type = SelectField('Contract type', choices = ['call', 'put'])
    strike = DecimalField('Strike', validators = [Optional()], places = 2)
    expiry = DateField('Expiry date', validators = [Optional()])

class TradeForm(FlaskForm):
    ticker = StringField('Ticker', validators = [DataRequired()])
    playid = StringField('Trade ID', validators = [Optional()])
    strategy = StringField('Strategy', validators = [DataRequired()])
    no_contracts = IntegerField('Number of contracts', validators = [DataRequired()])
    no_legs = IntegerField('Number of legs', validators = [DataRequired()])
    comment = TextAreaField('Comment', validators = [Optional()])
    open_date = DateField('Date opened', validators = [DataRequired()])
    open_premium = DecimalField('Opening premium', validators = [DataRequired()], places = 2)
    open_underlying = DecimalField('Underlying at open', validators = [Optional()], places = 2)
    close_date = DateField('Date closed', validators = [Optional()])
    close_premium = DecimalField('Closing premium', validators = [Optional()], places = 2)
    close_underlying = DecimalField('Underlying at close', validators = [Optional()], places = 2)
    pnl = DecimalField('P/L', validators = [Optional()], places = 2)
    dailypnl = DecimalField('Daily average P/L', validators = [Optional()], places = 2)
    legs = FieldList(FormField(TradeLegForm), min_entries = 4, max_entries = 4)
    submit = SubmitField('Submit')
""" should validate close_premium based on if close_date is known"""

class RollForm(FlaskForm):
    ticker = StringField('Ticker', validators = [Optional()])
    playid = StringField('Trade ID', validators = [Optional()])
    strategy = StringField('Strategy', validators = [Optional()])
    no_contracts = IntegerField('Number of contracts', validators = [Optional()])
    no_legs = IntegerField('Number of legs', validators = [Optional()])
    comment = TextAreaField('Comment', validators = [Optional()])
    open_date = DateField('Date opened', validators = [Optional()])
    open_premium = DecimalField('Opening premium', validators = [Optional()], places = 2)
    roll_premium = DecimalField('Opening premium', validators = [DataRequired()], places = 2)
    legs = FieldList(FormField(TradeLegForm), min_entries = 4, max_entries = 4)
    submit = SubmitField('Submit')
