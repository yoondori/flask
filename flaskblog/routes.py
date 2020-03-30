from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import secrets, os

posts = [
    {'author': 'Yoondor',
     'title': 'what should I eat for dinner',
     'content': 'no more pasta!',
     'date_posted': 'March 12, 2020'
     },
    {'author': 'dummy',
     'title': 'post2 title',
     'content': 'Second post content',
     'date_posted':'March 13, 2020'
     }
]


@app.route("/")
@app.route("/home")
def hello():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, pw=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome to the club, {form.username.data}. Now you can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='register nao', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('hello')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.pw, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('hello'))
            # flash(f'omg welcome back {}')
        else:
            flash('Login unsuccessful, please check your email and password', 'danger')
    return render_template('login.html', title='login nao', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('hello'))

#saving the file itself, returns the file name
def save_pic(form_picture):
    #create random hex
    ran_hex = secrets.token_hex(8)
    # if you're not using the variable, just use underscore
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_fn = ran_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile_pics', pic_fn)
    #resizing before saving
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)
    # form_picture.save(pic_path)
    return pic_fn



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.pic.data:
            pic_file = save_pic(form.pic.data)
            current_user.image_file = pic_file
        #sqlAlchemy lets you just change user variable
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Updated~', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

