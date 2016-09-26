# -*- coding: utf-8 -*-

import hashlib
from flask import Blueprint, render_template, request, session, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import identity_changed, Identity, AnonymousIdentity, current_app
from models import User
from extensions import login_manager

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return None
    return User.query.get(user_id)


@users_blueprint.route('/login')
def login_form(user_login=""):

    if current_user.is_authenticated:
        flash("Vous êtes déjà authentifié", "warning")
        return redirect("/")

    return render_template("login.html", login=user_login)


@users_blueprint.route('/login', methods=["POST"])
def login():

    if current_user.is_authenticated:
        flash("Vous êtes déjà authentifié", "warning")
        return redirect("/")

    user_login = request.form["login"]
    password = request.form["password"]

    user = User.query.filter_by(login=user_login).first()
    if not user:
        flash("Le login ou le mot de passe est incorrect", "error")
        return login_form(user_login)

    hashed_password = hashlib.sha512((user.salt + password).encode('utf8')).hexdigest()
    if hashed_password != user.password:
        flash("Le login ou le mot de passe est incorrect", "error")
        return login_form()

    login_user(user)
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

    flash("Vous êtes à présent connecté", "success")
    return redirect("/")


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()

    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    identity_changed.send(current_app, identity=AnonymousIdentity())

    flash("Vous êtes déconnecté", "success")
    return redirect("/")
