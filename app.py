from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    request,
    jsonify,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_moment import Moment
from flask_bcrypt import Bcrypt
import random

from helpers import get_quote, currency_formatter



# App initiation and configuration:
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
moment = Moment(app)

app.config["SECRET_KEY"] = "HELLO"

login_manager = LoginManager(app)
# Importing Forms and Models
from models import User, Budget, Expense
from forms import (
    LoginForm,
    SignupForm,
    BudgetForm,
    ExpenseForm,
    ChangePassword,
)


# Views:
@app.route("/")
@app.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    quote = get_quote()
    return render_template("/index.html", quote=quote)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login Successful")
            return redirect("/dashboard")
        else:
            flash("Wrong Username or Password")
    return render_template("/login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    form = SignupForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        new_user = User(
            name=form.name.data.capitalize(),
            username=form.username.data.lower(),
            password=hashed_pw,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("Signup Successful")
        return redirect("/dashboard")
    return render_template("/signup.html", form=form)


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    budget_form = BudgetForm()
    expense_form = ExpenseForm()
    return render_template(
        "dashboard.html",
        current_user=current_user,
        budget_form=budget_form,
        expense_form=expense_form,
        curr_f=currency_formatter,
    )


@app.route("/budgets/<name>")
@login_required
def budget_details(name):
    budget_form = BudgetForm()
    budget = (
        Budget.query.filter_by(user_id=current_user.id)
        .filter_by(name=name)
        .first_or_404()
    )
    return render_template(
        "details.html",
        budget=budget,
        budget_form=budget_form,
        curr_f=currency_formatter,
    )


@app.route("/account")
@login_required
def account():
    form = ChangePassword()
    return render_template("account.html", form=form)


# Utility routes
@app.route("/new-budget", methods=["POST"])
@login_required
def new_budget():
    budget_form = BudgetForm()
    rand = random.randint(1, 7)
    color = "accent-" + str(rand)
    if budget_form.validate_on_submit():
        new_budget = Budget(
            name=budget_form.name.data.capitalize(),
            amount=budget_form.amount.data,
            color=color,
            user=current_user,
        )
        db.session.add(new_budget)
        db.session.commit()
        flash("Budget Created")
        return redirect("/dashboard")
    return render_template(
        "dashboard.html",
        current_user=current_user,
        budget_form=budget_form,
        expense_form=ExpenseForm(),
        curr_f=currency_formatter,
    )


@app.route("/delete-budget/<name>")
@login_required
def delete_budget(name):
    budget = (
        Budget.query.filter_by(user_id=current_user.id)
        .filter_by(name=name).first()
    )
    for expense in budget.expenses:
        db.session.delete(expense)
    db.session.delete(budget)
    db.session.commit()
    return redirect("/dashboard")


@app.route("/edit-budget", methods=["GET", "POST"])
@login_required
def edit_budget():
    budget_id = int(request.form["budget_id"])
    budget = Budget.query.get(budget_id)
    budget_form = BudgetForm()
    if budget_form.validate_on_submit():
        budget.name = budget_form.name.data.capitalize()
        budget.amount = budget_form.amount.data
        db.session.commit()
        return redirect(f"/budgets/{budget.name}")
    return render_template(
        "details.html",
        budget=budget,
        budget_form=budget_form,
        curr_f=currency_formatter,
    )


@app.route("/new-expense", methods=["POST"])
@login_required
def new_expense():
    form = ExpenseForm()
    budget_id = int(request.form["budget"])
    budget = Budget.query.get(budget_id)
    if form.validate_on_submit():
        new_expense = Expense(
            name=form.expense_name.data.capitalize(),
            amount=form.expense_amount.data,
            budget=budget,
            user=budget.user,
        )
        budget.spent += new_expense.amount
        db.session.add(new_expense)
        db.session.commit()
        flash("Expense added")
        return redirect("/dashboard")
    return redirect("/dashboard")


@app.route("/delete-expense", methods=["POST"])
@app.route("/<name>/delete-expense", methods=["POST"])
@login_required
def delete_expense(name=None):
    expense_id = int(request.form["expense-id"])
    expense = Expense.query.get(expense_id)
    expense.budget.spent -= expense.amount
    db.session.delete(expense)
    db.session.commit()
    if name:
        return redirect(f"/budgets/{name}")
    return redirect("/dashboard")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout Successful")
    return redirect("/")


@app.route("/duplicate-user/<user_name>")
def duplicate(user_name):
    user = User.query.filter_by(username=user_name).first()
    print(user)
    if user:
        return jsonify("true")
    return jsonify("false")


@app.route("/change-password", methods=["POST"])
@login_required
def change_password():
    form = ChangePassword()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        current_user.password = hashed_pw
        db.session.commit()
        flash("Password changed successfully")
        return redirect("/account")
    return render_template("account.html", form=form)


@app.route("/delete_user", methods=["POST"])
@login_required
def delete_user():
    for budget in current_user.budgets:
        db.session.delete(budget)
    for expense in current_user.expenses:
        db.session.delete(expense)
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    flash("Account deleted successfully")
    return redirect(url_for("index"))


# Returns user id from session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Redirect unauthorized attempts to the index page
@login_manager.unauthorized_handler
def unauthorized():
    flash("Please login first")
    return redirect("/")


# Temp admin route to clear the database
@app.route("/clear")
def clear():
    with app.app_context():
        db.drop_all()
        db.create_all()
    return redirect("/")
