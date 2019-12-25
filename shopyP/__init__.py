from flask import Flask # Basic config
from flask_sqlalchemy import SQLAlchemy # Import the database

# For Login-Auth
from flask_bcrypt import Bcrypt # Used to hash passwords
from flask_login import LoginManager
# For Login-Auth
#
app = Flask(__name__)
app.config['SECRET_KEY'] = '3a932a420ff2da48766d5c5040468bf0'

# Create an instance of SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# For Login-Auth
bcrypt = Bcrypt(app) # Creating a hashing instance
# Creating a logging instance
login_manager = LoginManager(app) # Instance
login_manager.login_view = 'login' # So user can be redirected back to the login page when they try to access unathorised page
login_manager.login_message_category = 'info' # Bootstrap class, so the end result looks better
# For Login-Auth
from shopyP import routes
# from flask_login import UserMixin # used for login-auth, To satisfy the login_manager requirements
# from datetime import  datetime
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     cart = db.relationship('CartItem', backref='owner')
#
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"
# # Cart item
# class CartItem(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float)
#     date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# # Hacking products to sell
# class HackingProduct(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     description = db.Column(db.Text, nullable=False)
#     category = db.Column(db.String(100), nullable=False)
#
#
#     def __repr__(self):
#         return f"CartItem('{self.title}', 'S${self.price}', 'Date added:{self.date_added}')"
# # Class format for admin
# class Admin(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"
