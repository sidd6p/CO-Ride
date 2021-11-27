from flask import render_template, Blueprint

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html', title="Co-Ride")

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route('/error')
def error():
    return render_template('error.html')

@main.route("/privacy-policy")
def privacyPolicy():
    return render_template('privacy-policy.html', title='Privacy Policy')

