# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from acacia_server import utils
from acacia_server.extensions import login_manager
from acacia_server.public.forms import LoginForm, CleaningDutyPostForm
from acacia_server.user.forms import RegisterForm
from acacia_server.user.models import User

# from flask_login import login_required, login_user, logout_user


app = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@app.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            utils.flash_errors(form)
    return render_template("public/home.html", form=form)


# @blueprint.route("/logout/")
# @login_required
# def logout():
#     """Logout."""
#     logout_user()
#     flash("You are logged out.", "info")
#     return redirect(url_for("public.home"))


@app.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@app.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


@app.route(rule='/cleaning-duties/', methods=['GET', 'POST'])
def cleaning_duties():
    form = CleaningDutyPostForm(request.form)
    if form.is_submitted():
        utils.post_duties()
    return render_template('public/post_duties.html', form=form)
