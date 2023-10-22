from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, length, EqualTo, ValidationError

from models import User

class LoginForm(FlaskForm):
    username = StringField(
        validators=[DataRequired(), length(min=3, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[DataRequired(), length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    name = StringField(
        validators=[DataRequired(), length(min=3, max=20)],
        render_kw={"placeholder": "e.g. John"},
    )
    username = StringField(
        validators=[DataRequired(), length(min=3, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[
            DataRequired(),
            length(min=4, max=20),
            EqualTo("password_confirm", message="Passwords must match"),
        ],
        render_kw={"placeholder": "Password"},
    )
    password_confirm = PasswordField(
        validators=[DataRequired(), length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Signup")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            
            raise ValidationError('Please use a different username.')
        


class BudgetForm(FlaskForm):
    name = StringField(
        "Budget Name",
        validators=[DataRequired(), length(min=3, max=20)],
        render_kw={"placeholder": "e.g. Groceries"},
    )
    amount = FloatField(
        "Amount",
        validators=[DataRequired()],
        render_kw={"placeholder": "e.g. 100"},
    )
    submit = SubmitField("Create Budget")

    
class ExpenseForm(FlaskForm):
    name = StringField(
        "Expense Name",
        validators=[DataRequired(), length(min=3, max=20)],
        render_kw={"placeholder": "e.g. Bananas"},
    )
    amount = FloatField(
        "Amount",
        validators=[DataRequired()],
        render_kw={"placeholder": "e.g. 10"},
    )
    submit = SubmitField("Add Expense")