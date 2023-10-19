from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import InputRequired, length, ValidationError, EqualTo



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

class BudgetForm(FlaskForm):
    name = StringField(
        "Budget Name",
        validators=[InputRequired(), length(min=3, max=20)],
        render_kw={"placeholder": "e.g. Groceries"},
    )
    amount = FloatField(
        "Amount",
        validators=[InputRequired()],
        render_kw={"placeholder": "e.g. 100"},
    )
    submit = SubmitField("Create")

    
class ExpenseForm(FlaskForm):
    name = StringField(
        "Expense Name",
        validators=[InputRequired(), length(min=3, max=20)],
        render_kw={"placeholder": "e.g. Bananas"},
    )
    amount = FloatField(
        "Amount",
        validators=[InputRequired()],
        render_kw={"placeholder": "e.g. 10"},
    )
    submit = SubmitField("Add")