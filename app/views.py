from flask import Flask, render_template, request, redirect, url_for
from app.forms import indexForm, todoForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.secret_key = 'Development_key'

from app.models import db, User_data


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        todolist = db.session.query(User_data).all()
        return render_template('/index.html', todolist=todolist)
    else:
        todo = User_data.query.all()
        print(todo.title)
        print(todo.desc)
    return render_template('/index')


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

    return render_template('/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    return render_template('/signup.html')
