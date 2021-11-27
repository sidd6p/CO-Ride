from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskFile.config import Config

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()
loginManager.login_view = 'user.login'
loginManager.login_message_category = 'warning'

def createApp(configClass=Config):
    app = Flask(__name__)
    app.config.from_object(configClass)

    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)

    from flaskFile.user.routes import user
    app.register_blueprint(user)
    from flaskFile.feedback.routes import feedback
    app.register_blueprint(feedback)
    from flaskFile.main.routes import main
    app.register_blueprint(main)
    from flaskFile.ride.routes import ride
    app.register_blueprint(ride)

    return app




