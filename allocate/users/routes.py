# Standard library imports
import os

# Third party imports
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Local application imports
from allocate.users.forms import LoginForm, CompanyRegisterForm, UserRegisterForm, UserUpdateForm, CompanyUpdateForm, RequestResetForm, ResetPasswordForm
from allocate.models import User, Company, Role, UserRoles
from allocate import db
from allocate.users.utils import save_picture, send_reset_mail

users =  Blueprint('users', __name__)


@users.route("/register")
def register():
    return render_template("register.html")

@users.route("/register/comapny", methods=["GET","POST"])
def register_company():
    form = CompanyRegisterForm()

    if form.validate_on_submit():
        new_company = Company(company_name=form.company_name.data,
                              company_number=form.company_number.data)
        db.session.add(new_company)

        company = Company.query.filter_by(company_number=form.company_number.data).first()
        new_role = Role.query.filter_by(name=UserRoles.ADMIN).first()

        hashed_password = generate_password_hash(form.password.data, method='sha256')

        new_user = User(email=form.email.data,
                        password = hashed_password,
                        company_id=company.id,
                        role_id=new_role.id)

        db.session.add(new_user)
        db.session.commit()
        flash("Konto zostało stworzone! Możesz się zalogować", "success")
        return redirect(url_for('users.login'))
    return render_template("register_company.html", form=form)

@users.route("/register/user", methods=["GET","POST"])
def register_user():
    form = UserRegisterForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data, method='sha256')

        new_role = Role.query.filter_by(name=UserRoles.USER).first()

        new_user = User(email=form.email.data,
                        password = hashed_password,
                        role_id=new_role.id)

        db.session.add(new_user)
        db.session.commit()
        flash("Konto zostało stworzone! Możez się zalogować", "success")
        return redirect(url_for('users.login'))

    return render_template("register_user.html", form=form)

@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Na wskazany adres email wysłano instrukcje do resetu hasła", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Token wygasł lub jest niepoprawny", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Twoje hasło zostało zmienione")
        return redirect(url_for('users.login'))
    return redirect('reset_token.html', form=form)



@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            if user.company is None:
                return redirect(url_for('main.index'))

            return redirect(url_for('invoices.invoices_list'))
        else:
            flash('Logowanie nieudane. Spróbuj ponownie', 'danger')

    return render_template('login.html',form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route("/company/profile", methods=["GET", "POST"])
@login_required
def company_profile():
    form = CompanyUpdateForm()
    user_roles = UserRoles

    if form.validate_on_submit():
        if form.logo.data:
            picture_file = save_picture(form.logo.data, 'company')
            current_user.company.logo_filename = picture_file
        current_user.company.company_name = form.company_name.data
        current_user.company.company_number = form.company_number.data
        db.session.commit()
        return redirect(url_for('users.company_profile'))
    elif request.method == "GET":
        form.company_name.data = current_user.company.company_name
        form.company_number.data = current_user.company.company_number
    return render_template("company_profile.html", user_roles=user_roles, form=form)

@users.route("/company/add/<email>", methods=["POST"])
@login_required
def add_to_company(email):

    user = User.query.filter_by(email=email).first()

    if user:
        if user.company:
            flash("user has a company you moron", 'error')
        else:
            company = Company.query.get_or_404(current_user.company.id)
            company.users.append(user)
            db.session.commit()

    return redirect(url_for("users.company_profile"))

@users.route("/company/remove/<id>")
def remove_from_company(id):
    company = Company.query.get_or_404(current_user.company.id)
    user = User.query.get_or_404(id)
    print(user)

    if user.role.name in [UserRoles.ADMIN, UserRoles.SUPER_ADMIN]:
        return redirect(url_for('users.company_profile'))
    else:
        company.users.remove(user)
        db.session.commit()
        return redirect(url_for('users.company_profile'))


@users.route("/user/profile", methods=['GET', 'POST'])
@login_required
def user_profile():
    form = UserUpdateForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'user')
            current_user.avatar_filename = picture_file
        current_user.fullname = form.fullname.data
        current_user.occupancy = form.occupancy.data
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        return redirect(url_for('users.user_profile'))
    elif request.method == "GET":
        form.fullname.data = current_user.fullname
        form.occupancy.data = current_user.occupancy
        form.phone_number.data = current_user.phone_number

    return render_template("user_profile.html", form=form)