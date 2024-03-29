from flask import current_app
from datetime import datetime
from flaskFile import db, loginManager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@loginManager.user_loader
def loadUser(userId):
    return User.query.get(int(userId))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    rides = db.relationship('UserRide', backref='rider', lazy=True)
    review = db.relationship('UserReviews', backref="author", lazy=True)

    def getResetToken(self, expiresSec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expiresSec)
        return s.dumps({'userId': self.id}).decode('utf-8')

    @staticmethod
    def verifyToken(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            userId = s.loads(token)['userId']
        except:
            return None
        return User.query.get(userId)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class UserRide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    dateOfRide = db.Column(db.Date, nullable=False)
    preference = db.Column(db.String(100), nullable=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"UserRide('{self.userId}','{self.destination}', '{self.source}', '{self.id}')"

class UserReviews(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(256), nullable=False)
    dateOfReview = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)

    def __repr__(self):
        return f"UserReviews('{self.userId}','{self.id}','{self.content}')"