import os

class Config:
    SECRET_KEY = '5791628bb0b130c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('co_user')
    MAIl_PASSWORD = os.environ.get('co_pswd')
