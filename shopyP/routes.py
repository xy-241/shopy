from flask import render_template # Render templates
from flask import url_for # So we dont need to worry to import which file
from flask import flash
from flask import redirect
from flask import request # Obtain the route in the url, check what type the request is, the page of post the user requests

from flask import jsonify, make_response

from shopyP import app, db, bcrypt, mail
from shopyP.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from shopyP.models import User, Admin, CartItem, HackingProduct

from flask_mail import Message # To reset password
from flask_login import login_user, current_user, logout_user, login_required # Login Users in, to indicate users already login in, log user out, making sure users cant access certain pages before they login

from sqlalchemy import and_

import secrets # Give the picture a random index
import os # To get the extension of the picture
from PIL import Image # TO compress the pic

@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        if current_user.id >= 10000000000:
            return redirect(url_for('account'))
        hackingProducts = HackingProduct.query.all()
        return render_template('home.html', title='Home', hackingProducts=hackingProducts)
    hackingProducts = HackingProduct.query.all()
    return render_template('home.html', title='Home', hackingProducts=hackingProducts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # For Going back to account page after login
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', form=form, title='Login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# Save picture locally
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # Underscore is used to throw away a no useful variable
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) # Get the absolute path in order to save

    # Compress the picture before saving it
    output_size =(125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path) # Save the user picture locally
    return picture_fn # SO user can use the filename outside the function, one function for one purpose

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/deleteUser", methods=['POST'])
@login_required
def delete_user():
    if current_user.id >= 10000000000:
        user = Admin.query.filter_by(id=current_user.id).first()
    else:
        user = User.query.filter_by(id=current_user.id).first()

    cartItems = CartItem.query.filter(CartItem.owner_id == current_user.id)
    if cartItems:
        for cartItem in cartItems:
            db.session.delete(cartItem)
            db.session.commit()

    db.session.delete(user)
    db.session.commit()

    flash("You account has been deleted!", 'success')
    return redirect(url_for('register'))

@app.route("/admin", methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            next_page = request.args.get('next') # For Going back to account page after login
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('admin/login.html', form=form, title='Login')


@app.route("/cart")
@login_required
def cart():
    if current_user.id >= 10000000000:
        return redirect(url_for('account'))
    cartItems = CartItem.query.filter(CartItem.owner_id == current_user.id)
    return render_template('user/cart.html', title="Cart", cartItems=cartItems)

@app.route("/cart/valueUpdate", methods=["POST"])
@login_required
def itemValueUpdate():
    if current_user.id >= 10000000000:
        return redirect(url_for('account'))

    req = request.get_json()

    cartItem = CartItem.query.filter(and_(CartItem.title == req["title"], CartItem.owner_id == current_user.id)).first()
    cartItem.itemNum = req["value"]
    db.session.commit()
    res = make_response(jsonify({"message": "JSON received"}), 200)
    return res
@app.route("/cart/removeItem", methods=["POST"])
@login_required
def removeItem():
    if current_user.id >= 10000000000:
        return redirect(url_for('account'))

    req = request.get_json()

    cartItem = CartItem.query.filter(and_(CartItem.title == req["title"], CartItem.owner_id == current_user.id)).first()
    db.session.delete(cartItem)
    db.session.commit()
    res = make_response(jsonify({"message": "JSON received"}), 200)
    return res

@app.route("/addToCart/<int:item_id>")
@login_required
def addToCart(item_id):
    if current_user.id >= 10000000000:
        return redirect(url_for('account'))

    itemInfo = HackingProduct.query.filter_by(id=item_id).first()

    cartItem = CartItem.query.filter(and_(CartItem.title == itemInfo.title, CartItem.owner_id == current_user.id)).first()

    if cartItem:
        cartItem.itemNum += 1
        db.session.commit()
    else:
        cartItem = CartItem(title=itemInfo.title, price=itemInfo.price, image_file=itemInfo.image_file, owner=current_user, itemNum=1)
        db.session.add(cartItem)
        db.session.commit()

    hackingProducts = HackingProduct.query.all()
    return render_template('user/itemAddedModel.html', title='Item Added', hackingProducts=hackingProducts)

# To reset password
def send_reset_email(user):
    # Get the token, using the method from the model
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='yu.xin.yang.yxy@gmail.com',
                  recipients=[user.email]) # A message instance
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
''' # _external=True to get an absolute path
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('user/reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('user/reset_token.html', title='Reset Password', form=form)
# To reset password
