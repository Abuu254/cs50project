from flask.helpers import flash
from wtforms.fields.simple import StringField
from sqlalchemy import UniqueConstraint
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def profile_picture(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String(64), db.ForeignKey('user.username'), nullable=False)
    department = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("name", "username", "department", name="_ticket_uc"),
    )


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String(64), db.ForeignKey('user.username'), nullable=False)
    department = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    __table_args__ = (
        UniqueConstraint("name", "username", "department", name="_ticket_uc"),
    )

class Queue():
    def __init__(self, size):
        self.size = size

        self.queue = [None for i in range(size)]
        self.front = self.rear = -1

    def enqueue(self, data):
        if ((self.rear + 1)%self.size==self.front):
            return "Queue is Full"
        elif (self.front == -1):
            self.front = 0
            self.rear = 0
            self.queue[self.rear]=data
        else:
            self.rear = (self.rear + 1) % self.size
            self.queue[self.rear] = data
    def dequeue(self):
        if (self.front == -1):
            return "Nothing to Dequeue"
        elif(self.front==self.rear):
            pos=self.queue[self.front]
            self.front = -1
            self.rear = -1
            return pos
        else:
            pos = self.queue[self.front]
            self.front = (self.front + 1)%self.size
            return pos
    def display(self):
        if (self.front == -1):
            return("Queue is Empty")
        elif (self.rear>= self.front):
            for i in range(self.front, self.rear + 1):
                return self.queue[i]
        else:
            for i in range(self.front, self.size):
                return(self.queue[i])
            for i in range(0, self.rear + 1):
                return(self.queue[i])