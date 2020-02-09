from flask import render_template, send_file # Render templates
from flask import url_for # So we dont need to worry to import which file
from flask import flash, abort
from flask import redirect
from flask import request # Obtain the route in the url, check what type the request is, the page of post the user requests

from flask import jsonify, make_response

from shopyP import app, db, bcrypt, mail
from shopyP.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, addForm, updateForm, CheckoutForm, PostForm
from shopyP.models import User, Admin, CartItem, HackingProduct, purchaseRecord, Post


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
    posts = Post.query.filter(Post.user_id == current_user.id)
    from shopyP.models import purchaseRecord # This is needed, or the purchaseRecord is not defined, confusing
    purchaseRecords = purchaseRecord.query.filter(purchaseRecord.buyerId == current_user.id)
    
    if cartItems:
        for cartItem in cartItems:
            db.session.delete(cartItem)
            db.session.commit()
    if purchaseRecords:
        for purchaseRecord in purchaseRecords:
            db.session.delete(purchaseRecord)
            db.session.commit()
    if posts:
        for post in posts:
            db.session.delete(post)
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

@app.route("/addToCart/item", methods=["POST"])
@login_required
def addItem():
    if current_user.id >= 10000000000:
        return redirect(url_for('account'))

    req = request.get_json()

    itemInfo = HackingProduct.query.filter_by(title=req["title"]).first()
    cartItem = CartItem.query.filter(and_(CartItem.title == itemInfo.title, CartItem.owner_id == current_user.id)).first()

    if cartItem:
        cartItem.itemNum += 1
        db.session.commit()
    else:
        cartItem = CartItem(title=itemInfo.title, price=itemInfo.price, image_file=itemInfo.image_file, owner=current_user, itemNum=1)
        db.session.add(cartItem)
        db.session.commit()
    res = make_response(jsonify({"message": "JSON received"}), 200)
    return res

@app.route("/manageUser", methods=['GET', 'POST'])
def manageUser():
    if current_user.is_authenticated:
        if current_user.id >= 10000000000:
            users = User.query.all()
            return render_template('admin/manageUser.html', title='manageUser', users=users)
        else:
            flash('Authorized Access Only!', 'warning')
            return redirect(url_for('account'))
    else:
        flash('Authorized Access Only!', 'warning')
        return redirect(url_for('admin_login'))

@app.route("/manageUser/delete", methods=["POST"])
def deleteUserA():
    if current_user.is_authenticated:
        if current_user.id >= 10000000000:
            req = request.get_json()

            user = User.query.filter(User.username == req["username"]).first()

            cartItems = CartItem.query.filter(CartItem.owner_id == user.id)
            posts = Post.query.filter(Post.user_id == user.id)
            from shopyP.models import purchaseRecord # This is needed, or the purchaseRecord is not defined, confusing
            purchaseRecords = purchaseRecord.query.filter(purchaseRecord.buyerId == user.id)
            
            if cartItems:
                for cartItem in cartItems:
                    db.session.delete(cartItem)
                    db.session.commit()
            if purchaseRecords:
                for purchaseRecord in purchaseRecords:
                    db.session.delete(purchaseRecord)
                    db.session.commit()
            if posts:
                for post in posts:
                    db.session.delete(post)
                    db.session.commit()
            
            

            db.session.delete(user)
            db.session.commit()
            res = make_response(jsonify({"message": "JSON received"}), 200)
            return res
        else:
            flash('Authorized Access Only!', 'warning')
            return redirect(url_for('account'))
    else:
        flash('Authorized Access Only!', 'warning')
        return redirect(url_for('admin_login'))


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


# ZiMing
def save_Ppicture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # Underscore is used to throw away a no useful variable
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/shop', picture_fn) # Get the absolute path in order to save

    # Compress the picture before saving it
    output_size =(125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path) # Save the user picture locally
    return picture_fn

@app.route("/inventory", methods=['GET', 'POST'])
def inventory():
    if current_user.is_authenticated:
        if current_user.id >= 10000000000:
            hackingProducts = HackingProduct.query.all()
            return render_template('inventory.html', title='inventory', hackingProducts=hackingProducts)
        else:
            flash('Authorized Access Only!', 'warning')
            return redirect(url_for('account'))
    else:
        flash('Authorized Access Only!', 'warning')
        return redirect(url_for('admin_login'))


@app.route("/inventory/new", methods=['GET', 'POST'])
def new_inventory():
    if current_user.is_authenticated:
        if current_user.id >= 10000000000:
            form = addForm()
            if form.validate_on_submit():
                addProduct = HackingProduct(title=form.title.data, price=form.price.data, category=form.category.data, description=form.description.data, itemNum=form.itemNum.data)
                db.session.add(addProduct)
                db.session.commit()
                if form.picture.data:
                    picture_file = save_Ppicture(form.picture.data)
                    current = HackingProduct.query.filter_by(title=form.title.data).first()
                    current.image_file = picture_file
                    db.session.commit()
                flash('Your Product has been added!', 'success')
            return render_template('add_inventory.html', title='inventory', form=form, legend='Add Product')
        else:
            flash('Authorized Access Only!', 'warning')
            return redirect(url_for('account'))
    else:
        flash('Authorized Access Only!', 'warning')
        return redirect(url_for('admin_login'))


@app.route("/inventory/<int:Product_id>", methods=['GET', 'POST'])
def product(Product_id):
    if current_user.is_authenticated:
        if current_user.id >= 10000000000:
            Product = HackingProduct.query.get_or_404(Product_id)
            form = updateForm()
            if form.validate_on_submit():
                Product.title = form.title.data
                Product.price = form.price.data
                Product.itemNum = form.itemNum.data
                Product.category = form.category.data
                Product.description = form.description.data
                db.session.commit()
                if form.picture.data:
                    picture_file = save_Ppicture(form.picture.data)
                    current = HackingProduct.query.filter_by(title=form.title.data).first()
                    current.image_file = picture_file
                    db.session.commit()
                flash('Product has been updated!', 'success')
                return redirect(url_for('inventory', Product_id=Product.id))
            elif request.method == 'GET':
                form.title.data = Product.title
                form.price.data = Product.price
                form.itemNum.data = Product.itemNum
                form.category.data = Product.category
                form.description.data = Product.description
            image_file = url_for('static', filename='shop/'+HackingProduct.query.filter_by(title=form.title.data).first().image_file)
            return render_template('change_inventory.html', title='inventory', hackingProduct=Product, form=form, legend='Update Product')
        else:
            flash('Authorized Access Only!', 'warning')
            return redirect(url_for('account'))
    else:
        flash('Authorized Access Only!', 'warning')
        return redirect(url_for('admin_login'))

@app.route("/inventory/<int:Product_id>/delete", methods=['GET', 'POST'])
def delete_product(Product_id):
    if current_user.is_authenticated:
        if current_user.id >= 10000000000:
            Product = HackingProduct.query.get_or_404(Product_id)
            db.session.delete(Product)
            db.session.commit()
            flash('Product has been deleted!', 'success')
            return redirect(url_for('inventory'))
        else:
            flash('Authorized Access Only!', 'warning')
            return redirect(url_for('account'))
    else:
        flash('Authorized Access Only!', 'warning')
        return redirect(url_for('admin_login'))
# ZiMing

# Jas
@app.route("/aboutUs")
def aboutUs():
    return render_template('aboutUs.html',title='about')
# Jas


# JT

@app.route("/comments", methods=['GET', 'POST'])
def comments():
     posts = Post.query.all()
     return render_template('comments.html',title="comment" , posts=posts)



@app.route("/comments/create" , methods=['GET','POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        print('User', current_user)
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('comments'))
    return render_template('create_comments.html', form=form, title="comment", legend="Comments")

@app.route("/comments/<int:post_id>" , methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post, title="comment")


@app.route("/comments<int:post_id>/update" , methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('comments', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_comments.html', title='comment',
                           form=form, legend='Update Post')

@app.route("/comments<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('comments'))

#have to import abort and Post
# JT
#


# Ken
#Redirect Check (Kenneth)
@app.route("/cart/redirect")
@login_required
def redirectCheckout():
    list = []
    cartItems = CartItem.query.filter(CartItem.owner_id == current_user.id)
    for item in cartItems:
        list.append(item)
    if len(list) != 0:
        return redirect(url_for('checkout'))
    else:
        return redirect(url_for('cart'))
#Checkout (Kenneth)
@app.route("/checkout", methods=['GET', 'POST'])
@login_required
def checkout():
    if current_user.id >= 10000000000:
        return redirect(url_for('account'))
    req = request.get_json()

    sum = 0
    cartItems = CartItem.query.filter(CartItem.owner_id == current_user.id)
    hackingProducts = HackingProduct.query.all()
    for item in cartItems:
        price = item.price * item.itemNum
        sum += price
    checkoutForm = CheckoutForm(request.form)
    if checkoutForm.validate_on_submit():
        current_user.deliveryInfo = checkoutForm.address.data
        for item in cartItems:
            purchase = purchaseRecord(title=item.title, itemNum=item.itemNum, buyerId = current_user.id)
            db.session.add(purchase)
            db.session.commit()

        for cartItem in cartItems:
            for product in hackingProducts:
                if cartItem.title == product.title:
                    product.itemNum -= cartItem.itemNum

        if cartItems:
            for cartItem in cartItems:
                db.session.delete(cartItem)
                db.session.commit()


        flash('Your order has been successfully submitted!', 'success')
        return redirect(url_for('cart'))
    return render_template('checkout.html', title='Checkout', form=checkoutForm, cartItems=cartItems, sum=sum)

#Orderlist (Kenneth)
@app.route('/orders')
@login_required
def history():
    check = []
    purchases = purchaseRecord.query.filter(purchaseRecord.buyerId == current_user.id)
    for purchase in purchases:
        check.append(purchase)
    chk = len(check)
    address = current_user.deliveryInfo
    product = HackingProduct.query.all()

    return render_template('orders.html', title='Orders', purchases=purchases, address=address, product=product, check=chk)
#Delete (Kenneth)
@app.route('/orders/delete/<int:id>/', methods=['POST'])
def deleteOrder(id):
    purchases = purchaseRecord.query.filter(purchaseRecord.buyerId == current_user.id)
    for item in purchases:
        if item.id == id:
            db.session.delete(item)
            db.session.commit()
            flash('Your order has been deleted!', 'success')
            return redirect(url_for('history'))
    return redirect(url_for('history'))
# Ken

@app.route('/.well-known/brave-rewards-verification.txt')
def braveBAT():
    return send_file('/home/ubuntu/shopy/.well-known/brave-rewards-verification.txt')