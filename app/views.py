from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
from flask.ext.login import LoginManager
from flask.ext.login import login_user, logout_user, current_user, login_required
import os
from app.forms import indexForm, todoForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.secret_key = 'Development_key'

from app.models import db, User_data, User

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        todolist = db.session.query(User_data).all()
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(username=username).first()
    if registered_user and registered_user.check_password(password):
        flash('Username is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user, remember=remember_me)
    flash('Logged in successfully')
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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
