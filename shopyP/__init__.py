from flask import Flask # Basic config
from flask_sqlalchemy import SQLAlchemy # Import the database

# For Login-Auth
from flask_bcrypt import Bcrypt # Used to hash passwords
from flask_login import LoginManager
# For Login-Auth

from flask_mail import Mail # To reset email
import os # To reset email
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

# To reset password
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
mail = Mail(app)
#To reset password
from shopyP import routes
#from flask_login import UserMixin # used for login-auth, To satisfy the login_manager requirements
#from datetime import datetime
# class Person():
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#
#
#
#     def __repr__(self):
#         return f"Person('{self.username}', '{self.email}', '{self.image_file}')"
# # Class format for user
# class User(db.Model, Person, UserMixin):
#     deliveryInfo = db.Column(db.Text)
#     cart = db.relationship('CartItem', backref='owner')
#
#
#
#
#     def get_reset_token(self, expires_sec=1800):
#         s = Serializer(app.config['SECRET_KEY'], expires_sec)
#         return s.dumps({'user_id': self.id}).decode('utf-8')
#
#     @staticmethod # Telling the python not to take self as a paramenter
#     def verify_reset_token(token):
#         s = Serializer(app.config['SECRET_KEY'])
#         # Incase the token is expired
#         try:
#             user_id = s.loads(token)['user_id']
#         except:
#             return None
#         return User.query.get(user_id)
#
#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"
# # Class format for admin
# class Admin(db.Model, Person, UserMixin):
#     def __repr__(self):
#         return f"Admin('{self.username}', '{self.email}', '{self.image_file}')"
#
# class purchaseRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#
#     title = db.Column(db.String(100), nullable=False)
#     itemNum = db.Column(db.Integer, nullable=False)
#     date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     review = db.Column(db.Text, default="User didt give any review, 5 stars by default")
#     rating = db.Column(db.Integer, default=5)
#
#     buyerId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
# # Parent Class for the CartItem, HackingProduct
# class GeneralGoods():
#     id = db.Column(db.Integer, primary_key=True)
#
#     price = db.Column(db.Float)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#
#     def __repr__(self):
#         return f"GeneralGoods('{self.title}', 'S${self.price}', 'Date added:{self.date_added}')"
# # Cart item
# class CartItem(db.Model, GeneralGoods):
#     title = db.Column(db.String(100), nullable=False)
#     itemNum = db.Column(db.Integer, nullable=False)
#     owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
#     def __repr__(self):
#         return f"CartItem('{self.title}', 'S${self.price}', 'Date added:{self.date_added}')"
#
# # Hacking products to sell
# class HackingProduct(db.Model, GeneralGoods):
#     title = db.Column(db.String(100), nullable=False, unique=True)
#     description = db.Column(db.Text, nullable=False)
#     category = db.Column(db.String(100), nullable=False)
#
#     itemNum = db.Column(db.Integer, nullable=False)
#
#
#     def __repr__(self):
#         return f"HackingProduct('{self.title}', 'S${self.price}', 'Date added:{self.date_added}')"


# class Person():
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)



#     def __repr__(self):
#         return f"Person('{self.username}', '{self.email}', '{self.image_file}')"
# # Class format for user
# class User(db.Model, Person, UserMixin):
#     deliveryInfo = db.Column(db.Text)
#     cart = db.relationship('CartItem', backref='owner')

#     #JT
#     posts = db.relationship('Post', backref='author', lazy=True)
#     #JT
#     # Ken
#     purchaseRecords = db.relationship('purchaseRecord', backref='buyer')
#     # Ken


#     def get_reset_token(self, expires_sec=1800):
#         s = Serializer(app.config['SECRET_KEY'], expires_sec)
#         return s.dumps({'user_id': self.id}).decode('utf-8')

#     @staticmethod # Telling the python not to take self as a paramenter
#     def verify_reset_token(token):
#         s = Serializer(app.config['SECRET_KEY'])
#         # Incase the token is expired
#         try:
#             user_id = s.loads(token)['user_id']
#         except:
#             return None
#         return User.query.get(user_id)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"
# # Class format for admin
# class Admin(db.Model, Person, UserMixin):
#     def __repr__(self):
#         return f"Admin('{self.username}', '{self.email}', '{self.image_file}')"

# class purchaseRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True)

#     title = db.Column(db.String(100), nullable=False)
#     itemNum = db.Column(db.Integer, nullable=False)
#     date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     review = db.Column(db.Text, default="User did't give any review, 5 stars by default")
#     rating = db.Column(db.Integer, default=5)
#     buyerId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# # Parent Class for the CartItem, HackingProduct
# class GeneralGoods():
#     id = db.Column(db.Integer, primary_key=True)

#     price = db.Column(db.Float)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     def __repr__(self):
#         return f"GeneralGoods('{self.title}', 'S${self.price}', 'Date added:{self.date_added}')"
# # Cart item
# class CartItem(db.Model, GeneralGoods):
#     title = db.Column(db.String(100), nullable=False)
#     itemNum = db.Column(db.Integer, nullable=False)
#     owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"CartItem('{self.title}', 'S${self.price}', 'Date added:{self.date_added}')"

# # Hacking products to sell
# class HackingProduct(db.Model, GeneralGoods):
#     title = db.Column(db.String(100), nullable=False, unique=True)
#     description = db.Column(db.Text, nullable=False)
#     category = db.Column(db.String(100), nullable=False)

#     itemNum = db.Column(db.Integer, nullable=False)


#     def __repr__(self):
#         return f"HackingProduct('{self.title}', 'S${self.price}', 'Date added:{self.date_added}')"


# #Jt
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"
# #Jt
