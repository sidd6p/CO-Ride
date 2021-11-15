from flask import render_template, url_for, flash, redirect, request
import flask
#An ORM converts data between incompatible systems (object structure in Python, table structure in SQL database)
#SQLAlchemy gives you a skill set that can be applied to any SQL database system.
from flaskFile.forms import RegistrationForm, LoginForm, Ride, UpdateAccountForm
from flaskFile.models import User, Post
from flaskFile import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and  ref_url.netloc == test_url.netloc


posts = [
    {
        'Username': 'Sidp6',
        'Email': 'Sidp6@gmail.com',
        'Rating': '4/5',
        'Verify': 'true'
    },
    {
        'Username': 'Sidp12',
        'Email': 'Sidp12@gmail.com',
        'Rating': '3.8/5',
        'Verify': ''
    }
]

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html', title="Co-Ride")

@app.route("/find_ride", methods=['GET', 'POST'])
@login_required
def find_ride():
    """
    if not current_user.is_authenticated:
        flash('Login Required to access Account page', 'warning')
        return redirect(url_for('login'))
    """
    form = Ride()
    if form.validate_on_submit():
        return redirect(url_for('result'))
    return render_template('find_ride.html', title='Find-Ride', form=form)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/privacy_policy")
def privacy_policy():
    return render_template('privacy_policy.html', title='Privacy-Policy')

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
        return redirect(url_for('/home'))
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
            if not is_safe_url(nextPage):
                return flash.abort(400)
            return redirect(nextPage) if nextPage else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/result")
def result():
    return render_template('result.html', title='Result', posts=posts)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """
    if current_user.is_authenticated:
        return render_template('account.html', title=current_user.username)
    else:
        flash('Login Required to access Account page', 'warning')
        return redirect(url_for('login'))
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated Successfully', 'info')
    imageFile = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title=current_user.username, imageFile=imageFile, form=form)