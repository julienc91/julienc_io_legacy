# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

about_blueprint = Blueprint('about', __name__, template_folder='templates')


@about_blueprint.route('/about', strict_slashes=False)
def about():
    return render_template("about.html")
