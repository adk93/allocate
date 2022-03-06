# Standard library imports
import datetime as dt
import os.path
import enum

# Third party imports
from flask import current_app
from flask_login import UserMixin
from sqlalchemy import event
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# Local application imports
from allocate import db, login


class AccountTypes(enum.Enum):
    BASIC: str = "BASIC"
    PREMIUM: str = "PERMIUM"


class UserRoles(enum.Enum):
    SUPER_ADMIN: str = "Super Admin"
    ADMIN: str = "Admin"
    USER: str = "User"


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String, nullable=False)
    company_number = db.Column(db.String, nullable=False, unique=True)
    account_type = db.Column(db.Enum(AccountTypes), default=AccountTypes.BASIC)
    logo_filename = db.Column(db.String(88), nullable=True, default='default_logo.png')
    invoices = db.relationship("Invoice", backref='company', lazy=True)
    stamps = db.relationship("Stamp", backref="company", lazy=True)
    users = db.relationship("User", backref='company', lazy=True)


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                       )

users_permissions = db.Table('users_permissions',
                             db.Column('superior_user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                             db.Column('inferior_user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                             )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(88), nullable=False)
    fullname = db.Column(db.String(88), nullable=True)
    occupancy = db.Column(db.String(88), nullable=True)
    phone_number = db.Column(db.String(12), nullable=True)
    avatar_filename = db.Column(db.String(88), nullable=True, default='default_profile.jpg')
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    invoices = db.relationship("Invoice", backref='user', lazy=True)
    inferior_users = db.relationship("User",
                                     secondary = users_permissions,
                                     primaryjoin=id==users_permissions.c.superior_user_id,
                                     secondaryjoin=id==users_permissions.c.inferior_user_id,
                                     backref='left_nodes',
                                     lazy=True)

    def __repr__(self):
        return f"{self.id} - {self.company_id} - {self.email}"


    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    description = db.Column(db.String(255))
    users = db.relationship("User", backref='role', lazy=True)

    def __repr__(self):
        return f"{self.id} - {self.name} - {self.description}"

# @event.listens_for(Role.__table__, 'after_create')
# def create_roles(*args, **kwargs):
#     superadmin_role = Role(name=UserRoles.SUPER_ADMIN,
#                            description='Administrator serwisu')
#
#     admin_role = Role(name=UserRoles.ADMIN,
#                       description='Administrator firmy')
#
#     user_role = Role(name=UserRoles.USER,
#                      description='Użytkownik w firmie')
#
#     db.session.add(superadmin_role)
#     db.session.add(admin_role)
#     db.session.add(user_role)
#     db.session.commit()

class InvoiceStamps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer(),db.ForeignKey('invoice.id'))
    stamp_id = db.Column(db.Integer(), db.ForeignKey('stamp.id'))
    stamp_value = db.Column(db.Float())


class Stamp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    invoices = db.relationship("InvoiceStamps", backref='stamp', primaryjoin=id==InvoiceStamps.stamp_id,lazy='dynamic')

    def __repr__(self):
        return f"{self.id}-{self.text}"


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=False)
    thumbnail = db.Column(db.String, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"),nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    edit_date = db.Column(db.DateTime, default=dt.datetime.utcnow)
    stamps = db.relationship('InvoiceStamps', backref='invoice', primaryjoin= id==InvoiceStamps.invoice_id,lazy='dynamic')

    def __repr__(self):
        return f"{self.id} - {self.filename} - {self.company_id}"