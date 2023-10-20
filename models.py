from datetime import datetime
from flask_login import UserMixin
from app import db



class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    budgets = db.relationship("Budget", backref="user")

    def __repr__(self):
        return "<name %r>" % self.name


class Budget(db.Model, UserMixin):
    __tablename__ = "budget"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    spent = db.Column(db.Float, nullable=False, default=0)
    color = db.Column(db.String(9), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    expenses = db.relationship("Expense", backref="budget")

    def __repr__(self):
        return "<name %r>" % self.name


class Expense(db.Model, UserMixin):
    __tablename__ = "expense"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    budget_id = db.Column(db.Integer, db.ForeignKey("budget.id"))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<name %r>" % self.name