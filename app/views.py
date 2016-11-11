import flask
from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.wtf import Form
from app.forms import indexForm, todoForm, loginForm
import os
basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.secret_key = 'Development_key'

from app.models import db, User_data, User
u_userdata = User_data('title', 'desc')
u_user = User('username', 'firstname', 'lastname', 'email', 'password')

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'


@login_required
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        todolist = db.session.query(User_data).all()
        if todolist is False:
            db.create_all()
        return render_template('index.html', todolist=todolist)
    else:
        todo = User_data.query.all()
        print(todo.title)
        print(todo.desc)
    return render_template('index.html')


@app.route('/todo', methods=['POST', 'GET'])
def todo():
    form = todoForm(request.form)
    if request.method == 'GET':
        return render_template('/todo.html', form=form)
    elif request.method == 'POST':
        title = form.title.data
        desc = form.desc.data
        u_data = User_data(title=title, desc=desc)
        db.session.add(u_data)
        db.session.commit()
        return redirect(url_for('index'))


@login_manager.user_loader
def load_user(email):
    return User.query.get(email)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(u_user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        if not next_is_valid(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


@login_required
@app.route('/logout')
def logout():
    db.drop_all()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('/signup.html')
    user = User(request.form['username'], request.form['lastname'], request.form['lastname'], request.form[
        'email'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))
