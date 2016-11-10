from flask_sqlalchemy import SQLAlchemy
from app.views import app

db = SQLAlchemy(app)


class User(db.Model):
    # Table which stores all the user information during registration
    # Instantiate
    def __init__(self, username, firstname, lastname, email, password):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

    __tablename__ = 'table_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    email = db.Column(db.String(20))
    password = db.Column(db.String(20))

    def __repr__(self):
        return "<User(firstname='%s', lastname = '%s', email = '%s')>"(self.firstname, self.lastname, self.email)


class User_data(db.Model):
    # Table which stores users to-do information

    # Instantiate
    def __init__(self, title, desc):
        self.title = title
        self.desc = desc

    __tablename__ = 'table_users_data'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    desc = db.Column(db.String(20))

    def __repr__(self):
        return "<User_data(title = '%s', desc = '%s')>"(self.title, self.desc)
