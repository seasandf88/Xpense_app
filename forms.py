from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import InputRequired, length, EqualTo, ValidationError, Regexp
from flask_login import current_user

from models import User, Budget

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
        validators=[
            InputRequired(),
            length(min=3, max=20),
            Regexp("^[a-zA-Z0-9]*$",
            message="Username should not contain whitespaces or special characters.")
        ],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[
            InputRequired(),
            length(min=4, max=20),
            EqualTo("password_confirmation", message="Passwords must match"),
        ],
        render_kw={"placeholder": "Password"},
    )
    password_confirmation = PasswordField(
        validators=[InputRequired(), length(min=4, max=20)],
        render_kw={"placeholder": "Password "},
    )
    submit = SubmitField("Signup")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
class ChangePassword(FlaskForm):
    password = PasswordField(
        validators=[
            InputRequired(),
            length(min=4, max=20),
            EqualTo("password_confirmation", message="Passwords must match"),
        ],
        render_kw={"placeholder": "Password"},
    )
    password_confirmation = PasswordField(
        validators=[InputRequired(), length(min=4, max=20)],
        render_kw={"placeholder": "Confirm Password "},
    )
    submit = SubmitField("Change Password")


class BudgetForm(FlaskForm):
    name = StringField(
        "Budget Name",
        validators=[InputRequired(), length(min=3, max=20)],
        render_kw={"placeholder": "e.g., Groceries"},
    )
    amount = FloatField(
        "Amount",
        validators=[InputRequired()],
        render_kw={"placeholder": "e.g., 100"},
    )
    submit = SubmitField("Create Budget")

    def validate_name(self, name):
        budget = Budget.query.filter_by(user_id=current_user.id).filter_by(name=name.data.capitalize()).first()
        if budget is not None:
            raise ValidationError('Budget already exists.')

    
class ExpenseForm(FlaskForm):
    expense_name = StringField(
        "Expense Name",
        validators=[InputRequired(), length(min=3, max=20)],
        render_kw={"placeholder": "e.g. Bananas"},
    )
    expense_amount = FloatField(
        "Amount",
        validators=[InputRequired()],
        render_kw={"placeholder": "e.g. 10"},
    )
    expense_submit = SubmitField("Add Expense")