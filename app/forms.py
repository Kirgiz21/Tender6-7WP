from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, DateTimeField, SubmitField, SelectField, \
    PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


class TenderForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateTimeField('Start Date format: (Y-m-d H:M:S)', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    end_date = DateTimeField('End Date format: (Y-m-d H:M:S)', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Save')


class TenderItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired()])
    submit = SubmitField('Save')


class BidderForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contact_info = StringField('Contact Info', validators=[DataRequired()])
    submit = SubmitField('Save')


class BidForm(FlaskForm):
    price = FloatField('Price', validators=[DataRequired()])
    terms = TextAreaField('Terms', validators=[DataRequired()])
    bidder = SelectField('Bidder', validators=[DataRequired()])
    submit = SubmitField('Save')


class AwardForm(FlaskForm):
    price = FloatField('Price', validators=[DataRequired()])
    terms = TextAreaField('Terms', validators=[DataRequired()])
    submit = SubmitField('Save')


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(), Length(4)])

    password = PasswordField("Password", validators=[DataRequired(), Length(8)])

    submit = SubmitField('Save')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(4)])

    password = PasswordField("Password", validators=[DataRequired(), Length(8)])

    remember = BooleanField("Remember me")

    submit = SubmitField('Save')


class UpdateUserForm(FlaskForm):

    username = StringField("Username: ", validators=[DataRequired(), Length(4, 100)])

    role = SelectField('Role: ', validators=[DataRequired(message='Заповніть поле')])

    submit = SubmitField('Save')
