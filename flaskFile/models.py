from datetime import datetime
from flaskFile import db
from flaskFile import loginManager
from flask_login import UserMixin

@loginManager.user_loader
def loadUser(userId):
    return User.query.get(int(userId))

#a model is typically a Python class with attributes that match the columns of a corresponding database table.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    rides = db.relationship('UserRide', backref='rider', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class UserRide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    dateOfRide = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    preference = db.Column(db.String(100), nullable=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"UserRide('{self.userId}','{self.destination}', '{self.source}', '{self.id}')"