from flask import Flask, render_template, url_for, flash, redirect
#An ORM converts data between incompatible systems (object structure in Python, table structure in SQL database)
#SQLAlchemy gives you a skill set that can be applied to any SQL database system.
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
#config is a sub class of dictionary 
#To implement CSRF protection, Flask-WTF needs the application to configure an en‐cryption key
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# Flask-SQLAlchemy, a database is specified as a URL.
#SQLite (Windows) sqlite:///c:/absolute/path/to/database
db_name = 'site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
#SQLAlchemy is a class constructor with app as parameter
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flaskFile import routes