# create the basic form to store the data and the important validators for the data

import wtforms
from wtforms.validators import length, email, EqualTo, InputRequired
from models import EmailCaptchaModel, UserModel
from flask import session, g


# login form use for storing login information
# validators for each element
# email, password
class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email(message="Wrong format for login email!")])
    password = wtforms.StringField(validators=[length(min=8, max=20, message="Wrong format for password!")])


class EditInfoForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=4, max=20, message="Wrong format for username!")])
    email = wtforms.StringField(validators=[email(message="Wrong format for email!")])


class EditPasswordForm(wtforms.Form):
    password = wtforms.StringField(validators=[length(min=8, max=20, message="Wrong format for password! "
                                                                             "Must more than 8 characters!")])
    confirm_password = wtforms.StringField(validators=[EqualTo("password", message="The Password is not equal "
                                                                                   "to the previous one!")])


# register form use for storing register information
# validators for each element
# username, email, verification code, password
class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=4, max=20, message="Wrong format for username!"
                                                                             "Must be more than 4 characters "
                                                                             "and less than 20 characters!")])
    email = wtforms.StringField(validators=[email(message="Wrong format for email! You must enter the right "
                                                          "email address")])
    verification_code = wtforms.StringField(validators=[length(min=4, max=4,
                                                               message="Wrong format for verification code!")])
    password = wtforms.StringField(validators=[length(min=8, max=20, message="Wrong format for password! Must larger "
                                                                             "than 8 characters and smaller "
                                                                             "than 20 characters!")])
    confirm_password = wtforms.StringField(validators=[EqualTo("password", message="The Password is not equal "
                                                                                   "to the previous one!")])

    # check if the verification code is correct, if not raise error information
    def validate_verification_code(self, field):
        verification_code = field.data
        email = self.email.data
        verification_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not verification_model or verification_model.verification_code.lower() != verification_code.lower():
            raise wtforms.ValidationError("Wrong Verification Code!")

    # check if the email address is registered, if yes raise error
    def validate_email(self, field):
        if not session.get("user_id"):
            email = field.data
            user_model = UserModel.query.filter_by(email=email).first()
            if user_model:
                raise wtforms.ValidationError("The email address has already been registered!")


# todolist form use for storing list information
# validators for each element
# assessment title, module title, deadline, importance, status, description
class PostForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=2, max=30,
                                                   message="Wrong format for title!")])
    category = wtforms.StringField(validators=[length(min=1, message="Category can not be NULL!")])
    popular = wtforms.StringField(validators=[length(min=1, message="You must make a choice!")])
    place = wtforms.StringField(validators=[length(min=1, max=20, message="Place can not be NULL!")])
    time = wtforms.StringField(validators=[length(min=1, max=20, message="Time can not be NULL!")])
    description = wtforms.StringField(validators=[length(min=1, message="Wrong format for description!")])
    # pic = wtforms.StringField


class CommentForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1, message="Can not be empty!")])
    post_id = wtforms.IntegerField(validators=[InputRequired(message="Can not be empty!")])
