from flask import render_template, url_for, flash, redirect, request
import flask
import os
import secrets
from PIL import Image
from flaskFile.forms import RegistrationForm, LoginForm, Ride, UpdateAccountForm, MyFeedback
from flaskFile.models import User,UserRide, UserReviews
from flaskFile import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html', title="Co-Ride")



@app.route("/find-ride", methods=['GET', 'POST'])
@login_required
def findRide():
    form = Ride()
    if form.validate_on_submit():
        try: 
            ride = UserRide(source=form.source.data, destination=form.destination.data, dateOfRide=form.date.data, preference=form.preference.data, userId=current_user.id)
            db.session.add(ride)
            db.session.commit()
        except:
            return redirect(url_for('error'))
        return redirect(url_for('result'))
    return render_template('find-ride.html', title='Find-Ride', form=form)
    
@app.route("/result")
@login_required
def result():
    try:
        myride = UserRide.query.first()
        rides = UserRide.query.all()
    except:
        return redirect(url_for('error'))
    return render_template('result.html', title="Result", rides=rides, myride=myride)



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Welcome to Co-Ride', 'info')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful', 'info')
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(formPicture):
    random_hex = secrets.token_hex(8)
    fileName, fileExt = os.path.splitext(formPicture.filename)
    pictureName = random_hex + fileExt
    picturePath = os.path.join(app.root_path, 'static\profile_pics', pictureName)
    outputSize = (125, 125)
    i = Image.open(formPicture)
    i.thumbnail(outputSize)
    i.save(picturePath)
    return pictureName

@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    imageFile = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title=current_user.username, imageFile=imageFile, form=form)



@app.route('/my-feedback',  methods=['GET', 'POST'])
@login_required
def myFeedback():
    form = MyFeedback()
    if form.validate_on_submit():
        try: 
            userReview = UserReviews(title=form.title.data, content=form.content.data, rider=current_user)
            db.session.add(userReview)
            db.session.commit()
        except:
            return redirect(url_for('error'))
        flash("Thank you for the Feedback!", "info")
        return redirect(url_for('home'))
    return render_template('my-feedback.html', title="My Feedback", form=form)

@app.route('/all-feedback')
def allFeedback():
    try:
        feedbacks = UserReviews.query.all()
    except:
        return redirect(url_for('error'))
    return render_template('all-feedbacks.html', title="All Feedbacks", feedbacks=feedbacks)



@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route("/privacy-policy")
def privacyPolicy():
    return render_template('privacy-policy.html', title='Privacy Policy')

