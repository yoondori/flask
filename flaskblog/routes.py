import os
import secrets

from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required

from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post


@app.route("/")
@app.route("/home")
def hello():
    posts = Post.query.all()
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


# saving the file itself, returns the file name
def save_pic(form_picture):
    # create random hex
    ran_hex = secrets.token_hex(8)
    # if you're not using the variable, just use underscore
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_fn = ran_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile_pics', pic_fn)
    # resizing before saving
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


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created :3', 'success')
        return redirect(url_for('hello'))
    return render_template('post_create.html', title='글쓰기', legend = '글쓰기', form=form)


@app.route("/post/int:<post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/int:<post_id>/update", methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Posts been updated :D', 'success')
        return redirect(url_for('post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    # note because I keep forgetting: title is what appears on the tab
    return render_template('post_create.html', title='글 고치기', legend='글 고치기', form=form)


@app.route("/post/int:<post_id>/delete", methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your poor post has been murdered!', 'success')
    return redirect(url_for('hello'))