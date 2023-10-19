from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
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

    def check_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError(
                "The username already exists, please choose another one."
            )