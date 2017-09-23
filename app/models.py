from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    #Model to store user emails
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(25))
    email = db.Column(db.String(40), nullable=False)


class Todo(db.Model):

    #Model to store tasks
    __tablename__ = "Todo"

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(25), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.task_name

