from flask import render_template, Blueprint

general = Blueprint('general', __name__)

@general.route("/", methods=['GET', 'POST'])
@general.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('general/home.html', title="Co-Ride")

@general.route("/about")
def about():
    return render_template('general/about.html', title='About')

@general.route("/privacy-policy")
def privacyPolicy():
    return render_template('general/privacy-policy.html', title='Privacy Policy')

@general.app_errorhandler(Exception)
def errorHandler(Exception):
    return render_template ("general/error.html", title="Error")