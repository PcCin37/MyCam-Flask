from flask import (
    Blueprint,
    g,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    flash,
    current_app
)
from dec import login_required
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel, PostModel
import string
import random
from datetime import datetime
from .forms import LoginForm, RegisterForm, EditInfoForm, EditPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("user", __name__, url_prefix="/user")


# verify login information, get the data and check if validate
@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        current_app.logger.warning("Wrong methods 'GET'!")
        return render_template("sign-in.html")
    else:
        form = LoginForm(request.form)
        # # test for empty email and password
        # if not form.email.data or not form.password.data:
        #     result = {
        #         "errcode": -2,
        #         "errmsg": "Empty email and password"
        #     }
        #     return jsonify(result)
        # # test for the length of the password
        # if len(form.password.data) < 8:
        #     result = {
        #         "errcode": -3,
        #         "errmsg": "Password shorter than 8 characters"
        #     }
        #     return jsonify(result)
        # elif len(form.password.data) > 20:
        #     result = {
        #         "errcode": -4,
        #         "errmsg": "Password longer than 20 characters"
        #     }
        #     return jsonify(result)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            current_app.logger.info("Validate login form input.")
            # test for empty email
            if user and check_password_hash(user.password, password):
                # cookie: little data
                # cookie use for store login information
                # session in flask: encrypted and stored in cookie
                session['user_id'] = user.id
                current_app.logger.info("%s Login successful." % user.username)
                return redirect("/")
            else:
                # # test for wrong email or password
                # result = {
                #     "errcode": -1,
                #     "errmsg": "Wrong email or password"
                # }
                # return jsonify(result)
                # username and password does not match
                flash("Password does not match the Email!")
                current_app.logger.error("Error: Login failed! Something Wrong!")
                return render_template("sign-in.html", login_fail=1)
        else:
            # format incorrect
            flash("Email or Password format is incorrect!")
            current_app.logger.error("Error: Login form input invalid!")
            return render_template("sign-in.html", form=form)


@bp.route("/my")
@login_required
def my_info():
    if g.user:
        current_app.logger.info("Visit 'My' page successful.")
        return render_template("my.html")
    else:
        current_app.logger.warning("Warning: No login info, can not visit 'My' page!")
        return redirect(url_for("user.login"))


# edit the chosen user information according to the id
# update the change in the database
@bp.route("/edit_user", methods=['GET', 'POST'])
@login_required
def edit_user():
    # whether the user have logged, if not, jump to login page
    if request.method == 'GET':
        user = UserModel.query.get(g.user.id)
        current_app.logger.warning("Wrong methods 'GET'!")
        return render_template("edit_user.html", user=user)
    else:
        form = EditInfoForm(request.form)
        # # test for empty input
        # if not form.email.data or not form.username.data:
        #     result = {
        #         "errcode": -2,
        #         "errmsg": "Empty email or username"
        #     }
        #     return jsonify(result)
        # # test for the length of the username
        # if len(form.username.data) < 4:
        #     result = {
        #         "errcode": -3,
        #         "errmsg": "Username must be longer than 4 characters"
        #     }
        #     return jsonify(result)
        # elif len(form.username.data) > 20:
        #     result = {
        #         "errcode": -4,
        #         "errmsg": "Username must be shorter than 20 characters"
        #     }
        #     return jsonify(result)
        user = UserModel.query.get(g.user.id)
        if form.validate():
            user.username = form.username.data
            user.email = form.email.data
            # user.password = generate_password_hash(form.password.data)
            db.session.commit()
            current_app.logger.info("Validate edit form input.")
            return render_template("my.html", change=1)
        else:
            current_app.logger.error("Error: Edit failed! Something Wrong!")
            return render_template("edit_user.html", form=form)


# edit the chosen user password according to the id
# update the change in the database
@bp.route("/edit_password", methods=['GET', 'POST'])
@login_required
def edit_password():
    # whether the user have logged, if not, jump to login page
    if request.method == 'GET':
        user = UserModel.query.get(g.user.id)
        current_app.logger.warning("Wrong methods 'GET'!")
        return render_template("edit_password.html", user=user)
    else:
        form = EditPasswordForm(request.form)
        # # test for empty input
        # if not form.password.data:
        #     result = {
        #         "errcode": -2,
        #         "errmsg": "Empty password"
        #     }
        #     return jsonify(result)
        # # test for the length of the password
        # if len(form.password.data) < 8:
        #     result = {
        #         "errcode": -3,
        #         "errmsg": "Password shorter than 8 characters"
        #     }
        #     return jsonify(result)
        # elif len(form.password.data) > 20:
        #     result = {
        #         "errcode": -4,
        #         "errmsg": "Password longer than 20 characters"
        #     }
        #     return jsonify(result)
        user = UserModel.query.get(g.user.id)
        if form.validate():
            user.password = generate_password_hash(form.password.data)
            db.session.commit()
            session.clear()
            current_app.logger.info("Validate change password form input.")
            return render_template("sign-in.html", change_password=1)
        else:
            current_app.logger.error("Error: Change failed! Something Wrong!")
            return render_template("edit_password.html", form=form)


# get the register data and stor into the database
# table user, email, username, password
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        current_app.logger.warning("Wrong methods 'GET'!")
        return render_template("sign-up.html")
    else:
        form = RegisterForm(request.form)
        # # test for empty input
        # if not form.email.data or not form.username.data or not form.password.data or not form.verification_code.data:
        #     result = {
        #         "errcode": -2,
        #         "errmsg": "All the block can not be empty"
        #     }
        #     return jsonify(result)
        # # test for the length of the username
        # if len(form.username.data) < 4:
        #     result = {
        #         "errcode": -3,
        #         "errmsg": "Username must be longer than 4 characters"
        #     }
        #     return jsonify(result)
        # elif len(form.username.data) > 20:
        #     result = {
        #         "errcode": -4,
        #         "errmsg": "Username must be shorter than 20 characters"
        #     }
        #     return jsonify(result)
        # # test for the length of the password
        # if len(form.password.data) < 8:
        #     result = {
        #         "errcode": -5,
        #         "errmsg": "Password shorter than 8 characters"
        #     }
        #     return jsonify(result)
        # elif len(form.password.data) > 20:
        #     result = {
        #         "errcode": -6,
        #         "errmsg": "Password longer than 20 characters"
        #     }
        #     return jsonify(result)
        # # test for the length of the verification code
        # if len(form.verification_code.data) != 4:
        #     result = {
        #         "errcode": -7,
        #         "errmsg": "Verification code must be 4 characters"
        #     }
        #     return jsonify(result)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            verification_code = form.verification_code.data

            # password encryption processing
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password,
                             verification_code=verification_code)
            db.session.add(user)
            db.session.commit()
            current_app.logger.info("Validate register form input.")
            return redirect(url_for("user.login"))
        else:
            # # test for wrong input
            # result = {
            #     "errcode": -1,
            #     "errmsg": "Confirm password not correct or format of input incorrect"
            # }
            # return jsonify(result)
            current_app.logger.error("Error: Register failed! Something Wrong!")
            return render_template("sign-up.html", form=form)


# log out function, clear session, return to login page
@bp.route("/logout")
def logout():
    # clear all the data in session
    session.clear()
    current_app.logger.info("%s logout successful." % g.user.username)
    return redirect(url_for("user.login"))


# post the verification code to the input email
@bp.route("/verification", methods=['POST'])
def get_verification():
    # GET, POST to get the email input
    email = request.form.get("email")
    veri_letters = string.ascii_letters + string.digits
    verification_code = "".join(random.sample(veri_letters, 4))
    if email:
        # verification code message
        message = Message(
            subject="Verification Code for My Cam",
            recipients=[email],
            body=f"[My Cam] Your verification code for the registration is: {verification_code}, "
                 f"please do not tell anyone else."
        )
        mail.send(message)
        current_app.logger.info("Send verification code successful.")
        verification_model = EmailCaptchaModel.query.filter_by(email=email).first()
        # if exists, replace the code for specific email
        if verification_model:
            verification_model.verification_code = verification_code
            verification_model.create_time = datetime.now()
            db.session.commit()
        # if not, add a verification_model and commit to the database
        else:
            verification_model = EmailCaptchaModel(email=email, verification_code=verification_code)
            db.session.add(verification_model)
            db.session.commit()
        # print("verification_code:", verification_code)
        # RESTful API
        # {code: 200/400/500, message:"", data:{}}
        # return a successful request code: 200
        return jsonify({"code": 200, "message": "", "data": None})
    else:
        # return a client error code: 400
        current_app.logger.warning("Warning: No valid email address get!")
        return jsonify({"code": 400, "message": "Please enter the email first!"})
