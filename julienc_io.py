# -*- coding: utf-8 -*-

import locale
import random
from flask import Flask, render_template, g
from flask_login import current_user
from flask_principal import identity_loaded, RoleNeed
from views.articles import articles_blueprint
from views.about import about_blueprint
from views.admin import admin_blueprint
from views.users import users_blueprint
from views.contact import contact_blueprint
from views.projects import projects_blueprint
from views.tags import tags_blueprint
from extensions import recaptcha, mail, sqlalchemy, login_manager, principal, misaka

app = Flask(__name__)
app.config.update(
    SECRET_KEY="MY_SECRET_KEY",
    DEBUG=False,
    RECAPTCHA_SITE_KEY="MY_RECAPTCHA_PUBLIC_KEY",
    RECAPTCHA_SECRET_KEY="MY_RECAPTCHA_PRIVATE_KEY",
    MAIL_SERVER="MY_MAIL_SERVER",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME="MY_MAIL_USERNAME",
    MAIL_PASSWORD="MY_MAIL_PASSWORD",
    MAIL_DEFAULT_SENDER="MY_MAIL_DEFAULT_SENDER",
    MAIL_DEFAULT_RECIPIENTS=["MY_MAIL_DEFAULT_RECIPIENT"],
    SQLALCHEMY_DATABASE_URI="MY_DATABASE_URI",
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

recaptcha.init_app(app)
mail.init_app(app)
sqlalchemy.init_app(app)
login_manager.init_app(app)
principal.init_app(app)
misaka.init_app(app)


sqlalchemy.create_all(app=app)

app.register_blueprint(articles_blueprint)
app.register_blueprint(about_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(contact_blueprint)
app.register_blueprint(projects_blueprint)
app.register_blueprint(tags_blueprint)


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
def error_handler(error):
    return render_template("error.html", error=error, code=error.code), error.code


@app.errorhandler(500)
def error_500_handler(error):
    return render_template("error.html", error=error, code=500), 500


@app.before_request
def generate_csp_nonce():
    g.nonce = random.getrandbits(256)


@app.after_request
def apply_csp_headers(response):
    if not response.headers.get("Content-Security-Policy"):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self';"
            "font-src 'self' fonts.gstatic.com;"
            "img-src 'self' https:;"
            "script-src www.google-analytics.com 'nonce-{NONCE}' 'strict-dynamic';"
            "style-src 'self' fonts.googleapis.com;"
            "object-src 'none';").format(NONCE=g.nonce)
    return response


@identity_loaded.connect_via(app)
def on_identity_loaded(_, identity):
    identity.user = current_user
    if current_user.admin:
        identity.provides.add(RoleNeed("admin"))


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'fr_FR')
    app.run(host="0.0.0.0")
