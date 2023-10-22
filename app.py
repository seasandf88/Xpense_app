from flask import Flask, render_template, redirect, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_moment import Moment
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt
import os, datetime, random
from helpers import get_quote


# Global variables:
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = "sqlite:///" + os.path.join(PROJECT_ROOT, "instance", "database.db")


# App initiation:
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)

app.config["SECRET_KEY"] = "HELLO"

login_manager = LoginManager(app)
# login_manager.init_app(app)


# Importing Forms and Models
from models import User, Budget, Expense
from forms import LoginForm, SignupForm, BudgetForm, ExpenseForm


# Routes:
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash("Please login first")
    return redirect("/")

@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect('/dashboard')
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
        new_user = User(name=form.name.data.capitalize(), username=form.username.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("Signup successful")
        return redirect("/dashboard")
    return redirect("/")
    

@app.route("/dashboard")
@login_required
def dashboard():
    budget_form = BudgetForm()
    expense_form = ExpenseForm()
    user_expenses = Expense.query.filter_by()
    users = User.query.all()
    user = User.query.get(1)
    return render_template(
        "dashboard.html",
        current_user=current_user,
        budget_form=budget_form,
        expense_form=expense_form,
        users=users,
        user=user
        )

    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successful")
    return redirect("/")


@app.route("/new-budget", methods=["POST"])
@login_required
def new_budget():
    form = BudgetForm()
    rand = random.randint(1, 7)
    color = "accent-" + str(rand)
    if form.validate_on_submit():
        new_budget = Budget(name=form.name.data.capitalize(), amount=form.amount.data, color=color, user=current_user)
        db.session.add(new_budget)
        db.session.commit()
        flash("Budget Created")
        return redirect("/dashboard")
    flash("Something went wrong")
    return redirect("/dashboard")
    

@app.route("/new-expense", methods=["POST"])
@login_required
def new_expense():
    form = ExpenseForm()
    budget_id = int(request.form["budget"])
    budget = Budget.query.get(budget_id)
    spent = budget.spent
    if form.validate_on_submit():
        new_expense = Expense(name=form.name.data.capitalize(), amount=form.amount.data, budget=budget, user=budget.user)
        budget.spent += new_expense.amount
        db.session.add(new_expense)
        db.session.add(budget)
        db.session.commit()
        flash("Expense added")
        return redirect("/dashboard")
    return redirect("/dashboard")

@app.route("/delete-expense", methods=["POST"])
@app.route("/<name>/delete-expense", methods=["POST"])
@login_required
def delete_expense(name = None):
    expense_id = int(request.form["expense-id"])
    expense = Expense.query.get(expense_id)
    expense.budget.spent -= expense.amount
    db.session.delete(expense)
    db.session.commit()
    if name:
        return redirect(f"/budgets/{name}")
    return redirect("/dashboard")


@app.route("/budgets/<name>")
@login_required
def budget_details(name):
    budget = Budget.query.filter_by(name=name).first()
    return render_template("details.html", budget=budget)


@app.route("/delete-budget/<name>")
@login_required
def delete_budget(name):
    budget = Budget.query.filter_by(name=name).first()
    db.session.delete(budget)
    db.session.commit()
    return redirect("/dashboard")


# Creates shell context
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Budget': Budget, 'Expense': Expense}