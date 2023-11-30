from app_main import db
from datetime import datetime
from flask import request, redirect, url_for
from flask_login import current_user, UserMixin
from flask_security import RoleMixin
import os.path as op
from flask_admin.form.upload import FileUploadField, secure_filename
import os

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
    extend_existing=True
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255)),
    extend_existing = True  # Добавьте этот параметр

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(25), nullable=False, unique=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    verification = db.Column(db.Boolean, default=None)
    passport_image = db.Column(db.String, nullable=False)
    passport_seria = db.Column(db.Integer, nullable=False)
    passport_number = db.Column(db.Integer, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    orders = db.relationship('Orders', backref='users')
    transactions = db.relationship('Block_txn', backref='users')

    def __repr__(self):
        return '<User %r>' % self.id

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self):
        return redirect(url_for('login', next=request.url))

    @property
    def is_authenticated(self):
        return True

    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})


class Block_txn(db.Model, UserMixin):
    __tablename__ = 'Block'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    txn = db.Column(db.JSON)
    user = db.relationship('User', backref='Block')


class Orders(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_info = db.Column(db.JSON, nullable=False)
    user = db.relationship('User', backref='Orders')


class Contracts(db.Model):
    __tablename__ = 'Contracts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    path = db.Column(db.String)


class Cars(db.Model):
    __tablename__ = 'Cars'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image = db.Column(db.String(50), nullable=False)
    mark = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user = db.relationship('User', backref='Cars')
