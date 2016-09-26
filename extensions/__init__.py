# -*- coding: utf-8 -*-

from flask_recaptcha import ReCaptcha
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_principal import Principal
from flask_misaka import Misaka

recaptcha = ReCaptcha()
mail = Mail()
sqlalchemy = SQLAlchemy()
login_manager = LoginManager()
principal = Principal()
misaka = Misaka()
