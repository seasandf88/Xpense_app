from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt
import os, datetime
from helpers import get_quote


# Global variables:
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = "sqlite:///" + os.path.join(PROJECT_ROOT, "instance", "database.db")


# App initiation:
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "HELLO"

login_manager = LoginManager()
login_manager.init_app(app)


# Data models
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
    # color = db.Column(db.Integer, db.ForeignKey("budget.color"))

    def __repr__(self):
        return "<name %r>" % self.name


# Forms and validators:
class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), length(min=3, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    name = StringField(
        validators=[InputRequired(), length(min=3, max=20)],
        render_kw={"placeholder": "e.g. John"},
    )
    username = StringField(
        validators=[InputRequired(), length(min=3, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[
            InputRequired(),
            length(min=4, max=20),
            EqualTo("password_confirm", message="Passwords must match"),
        ],
        render_kw={"placeholder": "Password"},
    )
    password_confirm = PasswordField(
        validators=[InputRequired(), length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Signup")

    # def check_username(self, username):
    #     existing_user = User.query.filter_by(username=username.data).first()
    #     if existing_user:
    #         raise ValidationError(
    #             "The username already exists, please choose another one."
    #         )


# Routes:
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash("Please login first")
    return redirect("/")

@app.route("/")
def index():
    quote = get_quote()
    login_form = LoginForm()
    signup_form = SignupForm()
    return render_template("/index.html", quote=quote, login_form=login_form, signup_form=signup_form)

@app.route("/login", methods=["POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("login successful")
                return redirect("/dashboard")
    flash("Wrong username or password")
    return redirect("/")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("Signup successful")
        return redirect("/dashboard")
    

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", cur_user=current_user)

    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect("/")