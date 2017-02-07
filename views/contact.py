# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, flash, current_app, make_response, g, Response
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
        "script-src www.google-analytics.com 'nonce-{NONCE}' 'strict-dynamic';"
        "style-src 'self' 'unsafe-inline' fonts.googleapis.com;"
        "child-src www.google.com;"
        "object-src 'none';").format(NONCE=g.nonce)
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


@contact_blueprint.route('/pgp', methods=['GET'])
def pgp_key():
    key = """-----BEGIN PGP PUBLIC KEY BLOCK-----

mQINBFiaDSsBEADAB2UmD/cfLKicVpqEO+ha4Bg3ZlASuFPAmDWimWjJ6EWZN3tB
SMjhhkzVMa7fsu8uiwKc22SpL0C9fxfcGjT27BSKo2yzs4S2LyKgZdzAaqf+yhEq
E9fniYrcgb/cmgvUXoAK3jj5ngQxDVOKWmkLntZSSWfoE+LiaGunCG7P4KMyjsW/
TDVXyzQeykQ2sG8F0w6awyyTrpWq+F17EgthaeEnTsTZW4spjQrnOGrP1My2yR9s
p6fcov8zs23LFspM3TJZlD9FAb9apHrLyHnAm+KifVtSYpZiXjV2FGkVESUpG9KI
+V1nONBazm3u9jtNMiALEFIyq6id8CAiI3GNyiLn8p399BzOlB87xXhngw5zMz8C
9NojrEFnDLIVLoJd1mtJ1bJnlpaVfbdfweJcQvXCbX3m6KQ6VRBut+LvP2k8y3b7
125oMQDNaNOpaIl06mR6cFDR+tj/tAHnP2Egp1ugxxD0bLakDmOrjb0GA+d7MXNi
GGjghhlVi7NYNU17JXBO38BWyl55yzUojC11WB3kFWwIAa52RWCpr1sqk8aNX0yg
/seeOki+aFiPMPmNIrj8rPgauEdS3juSR6A/z5Mu9JYNeIrWPOdxuSLJ6UMsU8co
Eznd5Zkhuj2jNUu+EnfnNKjaODx2pNbDjGHsuByb2hMB8s/+j/ydA+Q4cwARAQAB
tCNKdWxpZW4gQ2hhdW1vbnQgPGp1bGllbkBqdWxpZW5jLmlvPokCNwQTAQgAIQUC
WJoNKwIbAwULCQgHAgYVCAkKCwIEFgIDAQIeAQIXgAAKCRDvTZmtsqGCPFwzEACc
RwuqHb0VEjuPGXLIkH/NcwYQj6GaUWLQbrSH05Bq3plfOBJHsta/aW8a/ZnpqJLV
mMsZCUgiAf4EmPI/RzZyW5AiQ6LfLf7vtdbawqUyK5FsbmGQfRfKFUguckI5jco0
VafERdHxTYiWZwwbX9Z57VewlPmqLJpO639qjCXpjI7BWVvvAKZcTSITWGJ7ZRWC
IXM1/9ON99u0y6EJpAvnkEsq136/PiYuTjum0zVXW5N7klHE2+GvEoVrgsK0l9GQ
vYYhdqb6IeaqeDjsGULWwW3rXIOUJlUCDW5XNQuzOtKIs5aAdodMn1AmqyyjeRiG
RTkMrKhdbJLUmCBBJgQPHamOT/73pD2J6g6IMjh9ybvzzPsie+K6aIm5+7zJRq6f
Fyylzpg9cCSoMs7YjpNBAzO/vcjFoTAKT7dYCoJhEHbshE1LdrecKa/UCnaXGIKS
9q09gqDlE9si/+occBr9xDXXuqUXfLjF5XOKv0Et0ibh+vIJqROPbB75D0BdEjxq
kywuG27aC0PdE1RWdC8zuEugHnI7yaNM1hVW9T8C6a03/pv12pGHEVvuZANuaIl7
ZCw4Lnl95STBG3WUFqXFP+0l2epYRwV+lMDltddPyQRVo5f8astY540IEbtAk7uZ
66VOTQ4NW6fHfeIa3cOhXS9qti+MekTGwq6+ObZgadH/AAAzW/8AADNWARAAAQEA
AAAAAAAAAAAAAAD/2P/gABBKRklGAAEBAAABAAEAAP/bAEMAAQEBAQEBAQEBAQEB
AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB
AQEBAf/bAEMBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB
AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AABEIAJYAeAMBIgACEQEDEQH/xAAf
AAABBQEBAQEBAQAAAAAAAAAAAQIDBAUGBwgJCgv/xAC1EAACAQMDAgQDBQUEBAAA
AX0BAgMABBEFEiExQQYTUWEHInEUMoGRoQgjQrHBFVLR8CQzYnKCCQoWFxgZGiUm
JygpKjQ1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoOEhYaH
iImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna
4eLj5OXm5+jp6vHy8/T19vf4+fr/xAAfAQADAQEBAQEBAQEBAAAAAAAAAQIDBAUG
BwgJCgv/xAC1EQACAQIEBAMEBwUEBAABAncAAQIDEQQFITEGEkFRB2FxEyIygQgU
QpGhscEJIzNS8BVictEKFiQ04SXxFxgZGiYnKCkqNTY3ODk6Q0RFRkdISUpTVFVW
V1hZWmNkZWZnaGlqc3R1dnd4eXqCg4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqy
s7S1tre4ubrCw8TFxsfIycrS09TV1tfY2dri4+Tl5ufo6ery8/T19vf4+fr/2gAM
AwEAAhEDEQA/AP6TkgOTkZ49MfyArSit+mOP8Onp7/4DHWcQAHp9eR+fGKsAYGB2
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
89rB/rXuLeWRILhp1KAP8e+Nfh/8XPAd3JqPhO5uNc0ndLMBbQFLlUlJxLM8ASdS
yRxPKp2xZKuB5chRfisZk0nzUMTR9hUlZLmfuOzi7xmrRab13310PtcNns044vDV
ni4RXLeCvVhflTjKF5SjJO2rXW+1z+0L4ceM/gV4p8CQ638UvCvgnxXaXlpbiO3l
ttJu4ovPCi3hWzj867uJI7h2S5N3JJFbzRb7q583CJxHxK+M/wAKPhH4bTVvhb4e
8HeGvDuuXssHiKy06SCwJtraC3kSa0eyjnNrK0BEN6qSS20jvZ+ZLK85RP43/C3x
/wD2nYLw6Noz+JLx55VjaxmS+uNqGb57dZJU8lI3cbvu/M7YRSTHX64/BP4DftBf
EL4dfE74s/tL67c6d4F+EPw48SeNrbwVb39yser6tpmiz6loKa4sSi3is5TCtw1j
aSRNdlFd5PLleObwMRw9HD+zdTEUpQlUUVBJObnN2XKl761d3qkoq1+/12H4zrYy
hVw2HwdSFSnTlKdVx5YqEIptzlpFqy8/eastrfu5/wAE2vB99+0J4k8S/tK67qEb
fD7TdX/4RnwboAuo7i41zU/D9tDDBq2s20M5TT7LQ1mSfS7OdJbq81GSC/WcW1lb
vdfuOWCjA5I/z7fhzgevr/Mp/wAEFvHHiDSvEHxC+FV3dyS6LqfhZ/FX2MtJJFb6
vo2uQ2X2mIACOF57fWJopyQHmihtGZpFhURf0zA5APrX6lk+X4bLsDSoYaKSaUqk
0mpTm4q7lfstFpt1Z+HZ7j8XmGZVa2KqyqSilGEW7xp03rGMFoldaya1b+LZDJCf
z5/Hn/Gqz9R9P8/zqdmyfpn8aqyEnOCRjPf0x/h+tetHdeq/M8Byb36f8D/Ipzgn
IHqf5iimzHj3HOc88kf5/GitxHTH/P8An/P49K8n8e/HX4PfC+Od/HnxH8JeG5bd
Vd9PvtZs21dg5wnk6PbyzapcFm+UCC0k55OF5r8e/wBqf/god458azXvgr9n9b7w
t4biDDVPFvmWY8V6xZnck39mQQXc8+hWw2uVIVb+QqPtFzYI72tfkFfT65Nf6pda
s+o6hdahcXOo3dxqBvBJdXFykjS3EkzJHLeXBeVWmZby4m2wom+V5cS6qmurfy7O
3R/h/wAE6D97PjN/wVN8A6dD/YnwYsLzWdWu40VfFfinSrjTtB06WUxGPy9NuJ7S
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
=A2aS
-----END PGP PUBLIC KEY BLOCK-----"""
    return Response(key, content_type="text")
