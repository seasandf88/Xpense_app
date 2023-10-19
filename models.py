import datetime
from flask_login import UserMixin
from app import db



class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    budgets = db.relationship("Budget", backref="user")

    def __repr__(self):
        return "<name %r>" % self.name


class Budget(db.Model, UserMixin):
    __tablename__ = "budget"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    amount = db.Column(db.Float, nullable=False, unique=True)
    color = db.Column(db.String(9), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    expenses = db.relationship("Expense", backref="budget")

    def __repr__(self):
        return "<name %r>" % self.name


class Expense(db.Model, UserMixin):
    __tablename__ = "expense"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    amount = db.Column(db.Float, nullable=False, unique=True)
    budget_id = db.Column(db.Integer, db.ForeignKey("budget.id"))

    def __repr__(self):
        return "<name %r>" % self.name