from flask import url_for, redirect, render_template, flash, request, Blueprint
from flask_login import login_required, current_user, login_user, logout_user
from flaskFile.models import User
from flaskFile import db, bcrypt
from flaskFile.user.utils import save_picture, sendEmail
from flaskFile.user.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                    PasswordResetRequest, PasswordResetForm) 

user = Blueprint('user', __name__)

@user.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Welcome to Co-Ride', 'info')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)

@user.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful', 'info')
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@user.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pictureFile = save_picture(form.picture.data)
            current_user.image_file = pictureFile
        if form.username.data:
            current_user.username = form.username.data
        if form.email.data:
            current_user.email = form.email.data 
        db.session.commit()
        flash("Updated successfully", "info")
        return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    imageFile = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title=current_user.username, imageFile=imageFile, form=form)

@user.route('/reset-password-request', methods=['POST', 'GET'])
def resetPasswordRequest():
    # if current_user.is_authenticated:
    #     flash('You must log out first', 'warning')
    #     return redirect(url_for('main.home'))
    form = PasswordResetRequest()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        sendEmail(user)
        flash("An Email has been sent to your regestired Email to reset your password", 'info')
        return redirect(url_for('user.login'))
    return render_template('reset-password-request.html', title = 'Reset Password Request', form=form)

@user.route('/reset-password/<token>', methods=['POST', 'GET'])
def resetPassword(token):
    user = User.verifyToken(token)
    if not user:
        flash('Invalid or Expired Link', 'danger')
        return redirect(url_for('user.resetPasswordRequest'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Password reset Successfully', 'info')
        return redirect(url_for('user.login'))
    return render_template('reset-password.html', title = 'Reset Password', form=form)

