from flask import render_template, url_for, flash, redirect
#An ORM converts data between incompatible systems (object structure in Python, table structure in SQL database)
#SQLAlchemy gives you a skill set that can be applied to any SQL database system.
from flaskFile.forms import RegistrationForm, LoginForm, Ride
from flaskFile.models import User, Post
from flaskFile import app, db, bcrypt

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
def find_ride():
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
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flash('Login successful', 'info')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/result")
def result():
    return render_template('result.html', title='Result', posts=posts)
