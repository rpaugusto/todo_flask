from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Boolean
import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(2048))
    add_date = db.Column(db.DateTime(timezone=True), default=func.now())
    is_solution = db.Column(Boolean, default=False)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.String(2048))
    is_complet = db.Column(Boolean, default=False)
    add_date = db.Column(db.DateTime(timezone=True), default=func.now())
    upt_date = db.Column(db.DateTime(timezone=True), onupdate=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        
    #realtionship
    tasks = db.relationship('Task', backref='activity', lazy=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    name = db.Column(db.String(256))
    
    #realtionship
    todos = db.relationship('Todo', backref='owner', lazy=True)
