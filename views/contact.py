# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, flash, current_app, make_response, g
from flask_mail import Message
from extensions import recaptcha, mail
from validate_email import validate_email

contact_blueprint = Blueprint('contact', __name__, template_folder='templates')


@contact_blueprint.route('/contact', strict_slashes=False)
def contact(name="", email="", subject="", content=""):
    r = make_response(render_template("contact.html", name=name, email=email,
                                      subject=subject, content=content))

    # specific CSP configuration for reCAPTCHA: style-src unsafe-inline is disabled everywhere else
    r.headers["Content-Security-Policy"] = (
        "default-src 'self';"
        "font-src 'self' fonts.gstatic.com;"
        "img-src 'self' https:;"
        "script-src 'nonce-{NONCE}' 'strict-dynamic';"
        "style-src 'self' 'unsafe-inline' fonts.googleapis.com;"
        "child-src www.google.com;"
        "object-src none;").format(NONCE=g.nonce)
    return r


@contact_blueprint.route('/contact', methods=['POST'])
def contact_send_message():
    name = request.form["name"].strip()
    email = request.form["email"].strip()
    subject = request.form["subject"].strip()
    content = request.form["content"].strip()

    if not recaptcha.verify():
        flash("Le captcha est invalide", "error")
        return contact(name, email, subject, content)

    if not validate_email(email):
        flash("L'adresse mail n'est pas valide", "error")
        return contact(name, email, subject, content)

    if not subject or len(subject) > 60:
        flash("Le sujet du message n'est pas valide", "error")
        return contact(name, email, subject, content)

    if not name or len(name) > 60:
        flash("Le nom saisi n'est pas valide", "error")
        return contact(name, email, subject, content)

    if len(content) < 30 or len(content) > 2000:
        flash("Le contenu du message n'est pas valide", "error")
        return contact(name, email, subject, content)

    body = "Message de {} ({} - {}):\n{}".format(name, email, request.remote_addr, content)
    content = Message(subject, recipients=current_app.config["MAIL_DEFAULT_RECIPIENTS"], reply_to=email, body=body)

    mail.send(content)
    flash("Votre message a été envoyé", "success")
    return redirect("/")
