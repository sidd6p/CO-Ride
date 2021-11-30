from flask import render_template, url_for, flash, redirect, request
import flask
import os
import secrets
from PIL import Image
from flaskFile.forms import (RegistrationForm, LoginForm,
                            Ride, UpdateAccountForm, MyFeedback,
                            PasswordResetRequest, PasswordResetForm)
from flaskFile.models import User,UserRide, UserReviews
from flaskFile import app, bcrypt, db, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


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
            rideId = ride.id
        except:
            return redirect(url_for('error'))
        return redirect(url_for('result', rideId=rideId))
    return render_template('find-ride.html', title='Find-Ride', form=form)

@app.route("/update-rides/<int:rideId>", methods=['GET', 'POST']) 
def updateRide(rideId):
    ride = UserRide.query.get(rideId)
    form = Ride()
    if form.validate_on_submit() and request.method == 'POST':
        ride.destination = form.destination.data or ride.destination
        ride.source = form.source.data or ride.source
        ride.dateOfRide = form.date.data or ride.dateOfRide
        ride.preference = form.preference.data or ride.preference
        db.session.commit()
        return redirect(url_for('result', rideId=ride.id))
    elif request.method == 'GET':
        form.destination.data = ride.destination
        form.source.data = ride.source
        form.date.data = ride.dateOfRide
        form.preference.data = ride.preference
    return render_template("update-ride.html", title="Update Ride", form=form, rideId=rideId)

@app.route("/delete-ride/<int:rideId>", methods=['POST', 'GET'])
@login_required
def deleteRide(rideId):
    ride = UserRide.query.get(rideId)
    if request.method == 'POST':
        if current_user == ride.rider:
            db.session.delete(ride)
            db.session.commit()
            flash("Delete successfully", "warning")
            return redirect(url_for("allRides"))
        else:
            flash("Delele fail due to linvalid user")
            return redirect(url_for("allRides"))
    else:
        return "SHIT"

@app.route("/all-rides")
@login_required
def allRides():
    pageNum = request.args.get('page', 1, type = int)
    rides = UserRide.query.filter(UserRide.rider == current_user)\
    .order_by(UserRide.dateOfRide.desc())\
    .paginate(per_page = 4, page = pageNum)
    return render_template("your-rides.html", title="My Rides", rides=rides, curPage = pageNum)

@app.route("/result/<int:rideId>")
@login_required
def result(rideId):
    try:
        pageNum = request.args.get('page', 1, type = int)
        myRide = UserRide.query.filter(UserRide.id == rideId).first()
        avalRide = UserRide.query.filter(UserRide.rider != myRide.rider)\
            .filter(UserRide.destination == myRide.destination)\
            .filter(UserRide.source == myRide.source)\
            .filter(UserRide.dateOfRide == myRide.dateOfRide)
        avalRide = avalRide.paginate(per_page = 4, page = pageNum)
    except:
        return redirect(url_for('error'))
    return render_template('result.html', title="Result", avalRide = avalRide, rideId=myRide.id, curPage = pageNum)



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

def sendEmail(user):
    token = user.getResetToken()
    msg = Message('Password Reset', sender='this.corride@gmail.com', recipients=[user.email])
    msg.body = "To reset Your password, visit the following link {}".format(url_for('resetPassword', token=token, _external=True))
    mail.send(msg)

@app.route('/reset-password-request', methods=['POST', 'GET'])
def resetPasswordRequest():
    # if current_user.is_authenticated:
    #     flash('You must log out first', 'warning')
    #     return redirect(url_for('home'))
    form = PasswordResetRequest()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        sendEmail(user)
        flash("An Email has been sent to your regestired Email to reset your password", 'info')
        return redirect(url_for('login'))
    return render_template('reset-password-request.html', title = 'Reset Password Request', form=form)

@app.route('/reset-password/<token>', methods=['POST', 'GET'])
def resetPassword(token):
    user = User.verifyToken(token)
    if not user:
        flash('Invalid or Expired Link', 'danger')
        return redirect(url_for('resetPasswordRequest'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Password reset Successfully', 'info')
        return redirect(url_for('login'))
    return render_template('reset-password.html', title = 'Reset Password', form=form)



@app.route('/my-feedback',  methods=['GET', 'POST'])
@login_required
def myFeedback():
    return redirect(url_for("error"))
    # form = MyFeedback()
    # userFeedback = UserReviews.query.filter_by(author = current_user).first()
    # if form.validate_on_submit():
    #     if userFeedback != None:
    #         userFeedback.title = form.title.data
    #         userFeedback.content = form.title.data
    #         userFeedback.dateOfReview = form.date.data
    #         db.session.commit()
    #         flash("Thank you for the Feedback!", "info")
    #     else:      
    #         userReview = UserReviews(title=form.title.data, content=form.content.data, author=current_user)
    #         db.session.add(userReview)
    #         db.session.commit()
    #         flash("Thank you for the Feedback!", "info")
    #     return redirect(url_for('allFeedback'))
    # elif request.method == 'GET' and userFeedback:
    #     form.title.data = userFeedback.title
    #     form.content.data = userFeedback.content
    # return render_template('my-feedback.html', title="My Feedback", form=form)

@app.route('/all-feedback')
def allFeedback():
    feedbacks = UserReviews.query.all()
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

