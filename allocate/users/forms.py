# Standard library imports


# Third party imports
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, Form, IntegerField, FileField
from wtforms.validators import InputRequired, Email, Length, NumberRange, EqualTo, ValidationError
from flask_wtf.file import FileAllowed

# Local application imports
from allocate.models import Company, User


class LoginForm(FlaskForm):
    email = StringField('email',validators=[InputRequired(),Length(min=4,max=80)])
    password = PasswordField('password',validators=[InputRequired(),Length(min=4,max=80)])


class CompanyRegisterForm(FlaskForm):
    company_name = StringField('company_name', validators=[InputRequired(),
                                                           Length(min=2, max=80)])
    company_number = StringField("company_number", validators=[InputRequired(),
                                                               Length(min=10, max=10),
                                                               ])
    email = StringField('email', validators=[InputRequired(),
                                            Length(min=4,max=80),
                                            Email()])
    password = PasswordField('password', validators=[InputRequired(),
                                                    Length(min=4,max=80)])
    confirm_password = PasswordField('confirm_password', validators=[InputRequired(), EqualTo('password')])

    def validate_company_number(self, company_number):
        company = Company.query.filter_by(company_number=company_number.data).first()
        if company:
            raise ValidationError('That company is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already is taken.')


class UserRegisterForm(FlaskForm):
    email = StringField('email',validators=[InputRequired(),
                                            Length(min=4,max=80),
                                            Email()])
    password = PasswordField('password',validators=[InputRequired(),
                                                    Length(min=4,max=80)])
    confirm_password = PasswordField('confirm_password', validators=[InputRequired(), EqualTo('password')])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already is taken.')


class UserUpdateForm(FlaskForm):
    fullname = StringField('Imię i nazwisko', validators=[Length(max=80)])
    occupancy = StringField('Stanowisko', validators=[Length(max=80)])
    phone_number = StringField('Numer telefonu', validators=[Length(max=15)])
    picture = FileField('Zdjęcie', validators=[FileAllowed(['jpg','png'])])

class CompanyUpdateForm(FlaskForm):
    company_name = StringField('Nazwa firmy', validators=[InputRequired(),
                                                           Length(min=2, max=80)])
    company_number = StringField("Numer NIP", validators=[InputRequired(),
                                                               Length(min=10, max=10),
                                                               ])
    logo = FileField('Logo', validators=[FileAllowed(['jpg', 'png'])])

    def validate_company_number(self, company_number):
        company = Company.query.filter_by(company_number=company_number.data).first()
        if company:
            raise ValidationError('That company is taken.')