from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

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


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

